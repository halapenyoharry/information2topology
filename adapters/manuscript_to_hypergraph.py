#!/usr/bin/env python3
"""Adapter: novel manuscript (markdown chapter files) → TopoThink hypergraph.

Implements the paragraph-as-node architecture sketched in
research/paragraph-as-nodes.md:

  V (vertices) = paragraphs + characters + places + chapters + acts + scenes
  E (edges):
      paragraph next_paragraph paragraph    (sequence)
      paragraph member_of      scene        (containment)
      scene     member_of      chapter      (containment)
      chapter   member_of      act          (containment)
      paragraph mentions       character    (extracted)
      paragraph mentions       place        (extracted)
  I (incidences) carry per-mention detail (first_mention, raw_form, etc.)
  attrs:
      paragraph: { word_count, sentence_count, position_in_chapter,
                   slug, has_dialogue, has_ai_dialogue }
      character/place: { aliases }
      chapter: { title, file }
      act: { number }

Hyperedges used:
  - scene as a hyperedge with paragraphs as members
  - chapter as a hyperedge with scenes as members
  - act as a hyperedge with chapters as members
  These are reified — same id in nodes + edges, so they can be referenced
  AND have their own attrs.

Splitting rules:
  - One file = one chapter
  - `## ` line = scene break (hard) ; produces a new scene
  - Blank line between non-heading text = paragraph break
  - `# ` line = chapter title (consumed into chapter attrs, not a paragraph)
  - Italic-only first paragraph after title is treated as the editor's-note
    epigraph, not a story paragraph (matches '_..._' wrapper).

Character / place / theme detection is by case-sensitive alias matching
against a hard-coded list seeded from the manuscript's TOC + character
notes. See ENTITY_TABLE below.

Usage:
    python3 adapters/manuscript_to_hypergraph.py FILE [FILE ...] -o OUT.json
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable
from collections import Counter


# ---------------------------------------------------------------------------
# Entity table — characters, places, themes that should be NODES.
# Each entry: canonical_id → (display label, type, [aliases for substring match])
# ---------------------------------------------------------------------------
ENTITY_TABLE: dict[str, tuple[str, str, list[str]]] = {
    # Characters
    "eli":          ("Eli (Elinor Jones)",   "Character", ["Elinor", " Eli ", " Eli,", " Eli.", " Eli'", "Eli\n", "Sysiphé", "Sisephe", "Eli Jones"]),
    "rook":         ("Rook",                  "Character", ["Rook"]),
    "zayne":        ("Zayne",                 "Character", ["Zayne", "GhostInTheML"]),
    "lumen":        ("Lumen (AI)",            "Character", ["Lumen"]),
    "schpongle":    ("Schpongle (system)",    "Character", ["Schpongle"]),
    "samara":       ("Samara Wexler",         "Character", ["Samara", "Wexler"]),
    "lyle":         ("Lyle Shwarmy",          "Character", ["Lyle", "Shwarmy"]),
    "lillian":      ("Lillian",               "Character", ["Lillian"]),
    "ctx":          ("CTX",                   "Character", ["CTX"]),
    "astra":        ("Astra (formerly CTX)",  "Character", ["Astra"]),
    "mandy":        ("ManDy",                 "Character", ["ManDy"]),
    "diane":        ("Diane",                 "Character", ["Diane"]),
    "dick":         ("Dick",                  "Character", ["Dick"]),
    "lookout":      ("Lookout",               "Character", ["Lookout"]),
    "veritas":      ("Veritas",               "Character", ["Veritas"]),
    "isaac":        ("Isaac",                 "Character", ["Isaac"]),
    "chief_joseph": ("Chief Joseph",          "Character", ["Chief Joseph"]),
    "walter_gable": ("Walter Gable",          "Character", ["Walter Gable"]),
    "kavalia":      ("Kavalia",               "Character", ["Kavalia"]),
    "patricia":     ("Patricia (Eli's mom)",  "Character", ["Patricia", "patricia"]),
    "rick":         ("Rick (Eli's dad)",      "Character", ["Rick Conrads", "rick", " Rick "]),
    "gramma_eli":   ("Great-grandmother Eli", "Character", ["gramma eli", "gramma Eli", "great grandmother Eli"]),
    # Places
    "apartment":    ("Eli's apartment",       "Place",     ["apartment", "plant kingdom"]),
    "ebrain":       ("eBrain",                "Place",     ["eBrain"]),
    "coffee_shop":  ("the coffee shop",       "Place",     ["coffee shop"]),
    "abq":          ("Albuquerque",           "Place",     ["ABQ", "Albuquerque"]),
    "cheyenne_mtn": ("Cheyenne Mountain",     "Place",     ["Cheyenne Mountain"]),
    "kansas":       ("Kansas",                "Place",     ["Kansas", "I-70"]),
    "austin":       ("Austin",                "Place",     ["Austin"]),
    "jemez":        ("Jemez / Los Alamos",    "Place",     ["Jemez", "Los Alamos"]),
    # Themes / motifs
    "sisyphus":     ("Sisyphus motif",        "Theme",     ["push your rock", "rolling the rock", "Sisyphé", "Sisyphus", "Le Mythe De Sisyphe", "myth of sysyphus", "Sysiphé"]),
    "ai_hate":      ("AI hate",               "Theme",     ["AI hate"]),
    "free_will":    ("free will",             "Theme",     ["free will"]),
    "promethean":   ("Promethean Reversal",   "Theme",     ["Promethean Reversal", "Promethean reversal"]),
    "comfort_economy": ("comfort economy",    "Theme",     ["comfort economy"]),
}


COLOR = {
    "Paragraph":  "#FFE9C8",
    "Scene":      "#FCD9B5",
    "Chapter":    "#F8C8A0",
    "Act":        "#E8A075",
    "Character":  "#F8C8DC",
    "Place":      "#C8F8DC",
    "Theme":      "#F8F0C8",
}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

CHAPTER_RE   = re.compile(r"ch(\d+)", re.IGNORECASE)
ACT_HINT_RE  = re.compile(r"act\s*([1-3IVXivx]+)", re.IGNORECASE)
SCENE_BREAK  = re.compile(r"^#{2,3}\s*$")
H1_TITLE     = re.compile(r"^#\s+(.+)$")
ITALIC_ONLY  = re.compile(r"^_[^_]+_\s*$")


def parse_act_from_text(text: str, filename: str) -> int:
    """Return 1/2/3 — preferring the file's own header."""
    head = text[:400].lower()
    if "act iii" in head or "act 3" in head:
        return 3
    if "act ii" in head or "act 2" in head:
        return 2
    if "act i" in head or "act 1" in head:
        return 1
    # Fallback: filename hints
    fname = filename.lower()
    if "act3" in fname:
        return 3
    if "act2" in fname:
        return 2
    return 1  # default


def chapter_num_from_filename(path: Path) -> int | None:
    m = CHAPTER_RE.search(path.name)
    return int(m.group(1)) if m else None


def split_paragraphs(scene_text: str, line_base: int = 1,
                     char_base: int = 0) -> list[tuple[str, int, int]]:
    """Blank-line-separated paragraphs, dropping headings and empty lines.

    Returns list of (text, source_line, source_char_offset) tuples.
    line_base and char_base are the 1-indexed line number and 0-indexed
    character offset of the first character of scene_text within the
    original file, so returned positions are file-absolute.
    """
    out: list[tuple[str, int, int]] = []
    # Walk by character to track positions precisely
    pos = 0  # cursor within scene_text
    lines_consumed = 0  # newlines seen so far
    while pos < len(scene_text):
        # Skip blank lines (paragraph separators)
        while pos < len(scene_text) and scene_text[pos] in ' \t\n\r':
            if scene_text[pos] == '\n':
                lines_consumed += 1
            pos += 1
        if pos >= len(scene_text):
            break
        # Found start of a paragraph
        para_start = pos
        para_line = line_base + lines_consumed
        para_char = char_base + pos
        # Scan to next blank line (two newlines with optional whitespace between)
        end = scene_text.find('\n\n', pos)
        if end == -1:
            end = len(scene_text)
        p = scene_text[pos:end].strip()
        # Advance past the paragraph text
        lines_consumed += scene_text[pos:end].count('\n')
        pos = end
        if not p:
            continue
        if p.startswith("#"):  # heading lingered, skip
            continue
        out.append((p, para_line, para_char))
    return out


def split_scenes(body_text: str, line_base: int = 1,
                 char_base: int = 0) -> list[tuple[str, int, int]]:
    """Split chapter body on `##`/`###` lines.

    Returns list of (scene_text, scene_start_line, scene_start_char) tuples.
    line_base / char_base locate body_text within the original file.
    """
    scenes: list[tuple[str, int, int]] = []
    current_lines: list[str] = []
    current_start_line = line_base
    current_start_char = char_base
    line_num = line_base
    char_pos = char_base
    for line in body_text.split("\n"):
        if SCENE_BREAK.match(line.strip()):
            if current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    scenes.append((text, current_start_line, current_start_char))
                current_lines = []
            line_num += 1
            char_pos += len(line) + 1  # +1 for the newline
            current_start_line = line_num
            current_start_char = char_pos
            continue
        if not current_lines:
            current_start_line = line_num
            current_start_char = char_pos
        current_lines.append(line)
        line_num += 1
        char_pos += len(line) + 1
    if current_lines:
        text = "\n".join(current_lines).strip()
        if text:
            scenes.append((text, current_start_line, current_start_char))
    return scenes


def slug_for_paragraph(text: str, max_words: int = 6) -> str:
    """Slug = first ~6 content words, lowercased, hyphenated."""
    # Strip markdown punctuation, keep word characters
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    words = [w for w in cleaned.split() if w and not w.startswith("'")]
    slug = "-".join(w.lower() for w in words[:max_words])
    slug = re.sub(r"[^\w-]", "", slug)
    return slug[:80] or "paragraph"


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w[\w'-]*\b", text))


def sentence_count(text: str) -> int:
    # Approx — periods/?/! followed by space or end
    return max(1, len(re.findall(r"[.!?](?:\s|$)", text)))


def detect_entities(text: str) -> dict[str, list[str]]:
    """Return {entity_id: [alias_forms_found]} for any entity seen in text."""
    found: dict[str, list[str]] = {}
    for eid, (_label, _type, aliases) in ENTITY_TABLE.items():
        hits: list[str] = []
        for alias in aliases:
            if alias in text:
                hits.append(alias.strip())
        if hits:
            found[eid] = sorted(set(hits))
    return found


def has_dialogue(text: str) -> bool:
    return '"' in text or '“' in text


def has_ai_dialogue(text: str) -> bool:
    return "«" in text or "»" in text


# ---------------------------------------------------------------------------
# Text-evidence helpers — for the editorial-discipline convention
# (see research/editorial-discipline.md). Edge labels are excerpts of the
# prose that justifies the edge, so every edge in the graph points back at
# the passage that brought it into being.
# ---------------------------------------------------------------------------

def _flatten_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def text_excerpt(text: str, target: str, window: int = 100) -> str:
    """Return ~window characters of `text` centered on the first occurrence
    of `target`. Trim to nearest word boundary; mark elision with `...`.
    """
    flat = _flatten_ws(text)
    idx = flat.find(target.strip())
    if idx == -1:
        return _flatten_ws(flat[: min(len(flat), window)] + ("..." if len(flat) > window else ""))
    half = window // 2
    start = max(0, idx - half)
    end = min(len(flat), idx + len(target) + half)
    chunk = flat[start:end]
    if start > 0:
        space = chunk.find(" ")
        if 0 < space < 25:
            chunk = chunk[space + 1:]
        chunk = "..." + chunk
    if end < len(flat):
        space = chunk.rfind(" ")
        if 0 < (len(chunk) - space) < 25:
            chunk = chunk[:space]
        chunk = chunk + "..."
    return chunk


def seam_excerpt(prev_text: str, next_text: str, window: int = 35) -> str:
    """Last ~window chars of prev + ' ¶ ' + first ~window chars of next."""
    p = _flatten_ws(prev_text)
    n = _flatten_ws(next_text)
    tail = p[-window:] if len(p) > window else p
    head = n[:window] if len(n) > window else n
    # Trim to word boundaries
    if len(p) > window:
        space = tail.find(" ")
        if 0 < space < 15:
            tail = tail[space + 1:]
        tail = "..." + tail
    if len(n) > window:
        space = head.rfind(" ")
        if 0 < (len(head) - space) < 15:
            head = head[:space]
        head = head + "..."
    return f"{tail} ¶ {head}"


# ---------------------------------------------------------------------------
# Predicate classification — "mentions" is too thin; classify per-mention.
# ---------------------------------------------------------------------------

SPEECH_VERBS = [
    "said", "asked", "replied", "muttered", "exclaimed", "whispered",
    "typed", "answered", "continued", "added", "called", "shouted",
    "screamed", "spoke", "mumbled", "snapped", "told", "noted",
    "responded", "explained", "commented", "remarked", "hissed",
    "yelled", "interrupted", "interjected", "began", "stammered",
    "laughed", "joked", "demanded", "agreed", "objected",
]
SPEECH_VERBS_GROUP = "(?:" + "|".join(SPEECH_VERBS) + ")"


def detect_speakers(text: str, entity_aliases: dict[str, list[str]]) -> set[str]:
    """Return entity_ids that appear to SPEAK quoted text in this paragraph.

    Patterns:
      "..." Alias verb         (e.g., "Hi" Eli said)
      Alias verb, "..."        (e.g., Eli said, "Hi")
      "..." verb Alias         (less common; e.g., "Hi," said Eli)
    """
    speakers: set[str] = set()
    for eid, aliases in entity_aliases.items():
        for alias in aliases:
            a = re.escape(alias.strip().rstrip(",.;:!?'"))
            patterns = [
                rf'["»][\s,]*{a}\s+{SPEECH_VERBS_GROUP}\b',
                rf'\b{a}\s+{SPEECH_VERBS_GROUP},?\s*["«]',
                rf'["»][\s,]*{SPEECH_VERBS_GROUP}\s+{a}\b',
            ]
            if any(re.search(p, text) for p in patterns):
                speakers.add(eid)
                break
    return speakers


def has_pronoun_speech(text: str) -> bool:
    """True if the paragraph contains 'she/he VERB_SPEECH' near dialogue."""
    if not (has_dialogue(text) or has_ai_dialogue(text)):
        return False
    return bool(re.search(rf'\b(?:she|he)\s+{SPEECH_VERBS_GROUP}\b', text, re.IGNORECASE))


def detect_addressees(text: str, entity_aliases: dict[str, list[str]]) -> set[str]:
    """Return entity_ids that appear as direct addressees inside dialogue.

    Looks for vocative position: name at the very start or end of a dialogue
    chunk, possibly preceded by a greeting word. Conservative on purpose.
    """
    addressees: set[str] = set()
    # Both straight and AI-style dialogue chunks
    chunks = re.findall(r'"([^"]+)"', text) + re.findall(r'«([^»]+)»', text)
    for chunk in chunks:
        for eid, aliases in entity_aliases.items():
            for alias in aliases:
                a = re.escape(alias.strip().rstrip(",.;:!?'"))
                # Start: optionally after greeting; "Name, ..." / "Hey Name, ..."
                start_pat = rf'^\s*(?:hey|listen|look|yo|hi|hello|okay|so)?[\s,]*{a}[\s,!?:]'
                # End: "..., Name" / "...Name?"
                end_pat = rf'[\s,]{a}[?.!]?\s*$'
                if (re.search(start_pat, chunk, re.IGNORECASE)
                        or re.search(end_pat, chunk)):
                    addressees.add(eid)
                    break
    return addressees


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------

def build(files: list[Path]) -> dict:
    nodes: list[dict] = []
    edges: list[dict] = []

    seen_node_ids: set[str] = set()

    def add_node(nid: str, label: str, ntype: str, **props):
        if nid in seen_node_ids:
            return
        seen_node_ids.add(nid)
        nodes.append({
            "id": nid,
            "label": label,
            "type": ntype,
            "color": COLOR.get(ntype, "#CCCCCC"),
            "properties": props,
        })

    # Pre-add entity nodes (characters, places, themes) — they exist independently
    for eid, (label, etype, aliases) in ENTITY_TABLE.items():
        add_node(eid, label, etype, aliases=aliases)

    # Pre-add the three acts
    for act_n in (1, 2, 3):
        add_node(f"act:{act_n}", f"Act {act_n}", "Act", number=act_n)

    prev_paragraph_id: str | None = None  # for next-paragraph edges across chapter
    chapter_order: list[str] = []
    para_counter = Counter()  # per-chapter paragraph counter
    first_mention_seen: set[str] = set()  # corpus-wide first-mention tracking

    # Edge color/predicate registry — keeps layer styling consistent
    PRED_COLORS = {
        "introduces":     "#FF8800",  # orange — narrative debut
        "POV_of":         "#0066CC",  # blue — perspective
        "speaker_of":     "#CC0066",  # magenta — voice
        "addressee_of":   "#9933CC",  # purple — direct address
        "referenced_by":  "#999999",  # grey — talked-about-not-present
        "mentions":       "#26A",     # default fallback (places/themes)
        "next_paragraph": "#CCC",
    }

    # Role-pair vocabulary per predicate (see research/editorial-discipline.md).
    # Each entry maps a predicate to (paragraph_side_role, entity_side_role).
    ROLES_FOR = {
        "introduces":     ("debut_passage",     "new_arrival"),
        "POV_of":         ("perspective_lens",  "perspective_holder"),
        "speaker_of":     ("voice_carrier",     "speaker"),
        "addressee_of":   ("utterance",         "addressee"),
        "referenced_by":  ("mention_passage",   "referent"),
        "mentions":       ("mention_passage",   "mentioned"),
        "next_paragraph": ("predecessor",       "successor"),
    }

    def evidence_edge(eid: str, predicate: str, label: str,
                      paragraph_id: str, target_id: str,
                      paragraph_attrs: dict | None = None,
                      target_attrs: dict | None = None) -> dict:
        """Build an edge in the editorial-discipline shape: members-form with
        explicit role pair, text-evidence label on the edge."""
        p_role, t_role = ROLES_FOR[predicate]
        return {
            "id": eid,
            "label": label,
            "relationship": predicate,
            "direction": "directed",
            "color": PRED_COLORS[predicate],
            "members": [
                {"node": paragraph_id, "role": p_role, "attrs": paragraph_attrs or {}},
                {"node": target_id,    "role": t_role, "attrs": target_attrs    or {}},
            ],
        }

    for file_pos, path in enumerate(files):
        text = path.read_text(encoding="utf-8")
        source_filename = path.name
        ch_num = chapter_num_from_filename(path) or (file_pos + 1)
        act_n = parse_act_from_text(text, path.name)
        ch_id = f"ch:{path.stem}"

        # Pull chapter title from first H1 (fall back to filename)
        title = path.stem
        for line in text.split("\n"):
            m = H1_TITLE.match(line.strip())
            if m:
                title = m.group(1).strip().rstrip("`")
                break

        add_node(ch_id, f"Ch {ch_num}: {title}", "Chapter",
                 file=path.name, file_position=file_pos, chapter_number=ch_num,
                 act=act_n)
        chapter_order.append(ch_id)

        # Edge: chapter member_of act (as dyadic edge for clarity)
        edges.append({
            "from": ch_id,
            "to": f"act:{act_n}",
            "relationship": "member_of_act",
            "direction": "directed",
            "color": "#888",
        })

        # Strip everything before the first H1 line of body,
        # tracking where the body starts in the file.
        body_lines = []
        seen_h1 = False
        body_start_line = 1
        body_start_char = 0
        char_cursor = 0
        for line_idx, line in enumerate(text.split("\n"), start=1):
            if not seen_h1 and H1_TITLE.match(line.strip()):
                seen_h1 = True
                char_cursor += len(line) + 1
                body_start_line = line_idx + 1
                body_start_char = char_cursor
                continue
            if seen_h1:
                body_lines.append(line)
            char_cursor += len(line) + 1
        body = "\n".join(body_lines).strip() if seen_h1 else text
        if not seen_h1:
            body_start_line = 1
            body_start_char = 0

        scenes = split_scenes(body, line_base=body_start_line, char_base=body_start_char)
        ch_scenes: list[str] = []
        prev_para_in_chapter: str | None = None

        # ---- First pass: collect paragraphs + mentions per scene
        # Structure: list of (scene_id, scene_idx, [(para_text, source_line, source_char, mentions_dict), ...])
        chapter_scene_data: list[tuple[str, int, list[tuple[str, int, int, dict[str, list[str]]]]]] = []
        chapter_character_mentions: Counter = Counter()
        for scene_idx, (scene_text, scene_start_line, scene_start_char) in enumerate(scenes):
            scene_id = f"{ch_id}:s{scene_idx + 1}"
            paragraphs_in_scene: list[tuple[str, int, int, dict[str, list[str]]]] = []
            for p_idx, (p_text, p_line, p_char) in enumerate(
                split_paragraphs(scene_text, line_base=scene_start_line, char_base=scene_start_char)
            ):
                if scene_idx == 0 and p_idx == 0 and ITALIC_ONLY.match(p_text):
                    continue
                mentions = detect_entities(p_text)
                paragraphs_in_scene.append((p_text, p_line, p_char, mentions))
                # Count character mentions for chapter-POV detection
                for eid in mentions:
                    if ENTITY_TABLE[eid][1] == "Character":
                        chapter_character_mentions[eid] += 1
            chapter_scene_data.append((scene_id, scene_idx, paragraphs_in_scene))

        # Determine chapter POV: most-mentioned character in this chapter.
        # Skip very common multi-chapter anchors? No — accept the heuristic.
        ch_pov: str | None = None
        if chapter_character_mentions:
            ch_pov = chapter_character_mentions.most_common(1)[0][0]

        # ---- Second pass: emit nodes + predicate-classified edges
        prev_para_text: str | None = None  # for seam-excerpt on next_paragraph edges
        for scene_id, scene_idx, paragraphs_in_scene in chapter_scene_data:
            add_node(scene_id, f"{title} — scene {scene_idx + 1}", "Scene",
                     chapter=ch_id, position=scene_idx + 1, chapter_pov=ch_pov)
            ch_scenes.append(scene_id)
            scene_para_ids: list[str] = []

            for p_text, p_line, p_char, mentions in paragraphs_in_scene:
                para_counter[ch_id] += 1
                para_id = f"p:{path.stem}:{para_counter[ch_id]:03d}"
                slug = slug_for_paragraph(p_text)
                add_node(para_id, slug, "Paragraph",
                         chapter=ch_id, scene=scene_id,
                         position_in_chapter=para_counter[ch_id],
                         word_count=word_count(p_text),
                         sentence_count=sentence_count(p_text),
                         has_dialogue=has_dialogue(p_text),
                         has_ai_dialogue=has_ai_dialogue(p_text),
                         text=p_text,  # full paragraph prose; the node IS the paragraph
                         source_file=source_filename,
                         source_line=p_line,
                         source_char_offset=p_char)
                scene_para_ids.append(para_id)

                # next_paragraph edge (within chapter only) — text-seam label
                if prev_para_in_chapter and prev_para_text is not None:
                    seam = seam_excerpt(prev_para_text, p_text)
                    edges.append(evidence_edge(
                        eid=f"edge:next/{prev_para_in_chapter}->{para_id}",
                        predicate="next_paragraph",
                        label=seam,
                        paragraph_id=prev_para_in_chapter,
                        target_id=para_id,
                    ))
                prev_para_in_chapter = para_id
                prev_para_text = p_text

                # ---- Per-mention predicate classification
                speakers = detect_speakers(p_text, mentions)
                if has_pronoun_speech(p_text) and ch_pov is not None:
                    speakers.add(ch_pov)
                addressees = detect_addressees(p_text, mentions)

                for eid, alias_forms in mentions.items():
                    etype = ENTITY_TABLE[eid][1]
                    primary_alias = alias_forms[0] if alias_forms else ""
                    inc_attrs = {"alias_form": alias_forms}
                    excerpt = text_excerpt(p_text, primary_alias, window=120)

                    if etype != "Character":
                        # Places / themes get the simple "mentions" predicate.
                        edges.append(evidence_edge(
                            eid=f"edge:mention/{para_id}->{eid}",
                            predicate="mentions",
                            label=excerpt,
                            paragraph_id=para_id,
                            target_id=eid,
                            paragraph_attrs=inc_attrs,
                            target_attrs=inc_attrs,
                        ))
                        continue

                    # Characters get classified into 1+ specific predicates.
                    classified = False

                    if eid not in first_mention_seen:
                        first_mention_seen.add(eid)
                        edges.append(evidence_edge(
                            eid=f"edge:debut/{para_id}->{eid}",
                            predicate="introduces",
                            label=excerpt,
                            paragraph_id=para_id,
                            target_id=eid,
                            paragraph_attrs=inc_attrs,
                            target_attrs=inc_attrs,
                        ))
                        classified = True

                    if eid == ch_pov:
                        edges.append(evidence_edge(
                            eid=f"edge:pov/{para_id}->{eid}",
                            predicate="POV_of",
                            label=excerpt,
                            paragraph_id=para_id,
                            target_id=eid,
                            paragraph_attrs=inc_attrs,
                            target_attrs=inc_attrs,
                        ))
                        classified = True

                    if eid in speakers:
                        # Wider window for speech excerpts so the dialogue is visible
                        speech_excerpt = text_excerpt(p_text, primary_alias, window=160)
                        edges.append(evidence_edge(
                            eid=f"edge:voice/{para_id}->{eid}",
                            predicate="speaker_of",
                            label=speech_excerpt,
                            paragraph_id=para_id,
                            target_id=eid,
                            paragraph_attrs=inc_attrs,
                            target_attrs=inc_attrs,
                        ))
                        classified = True

                    if eid in addressees:
                        edges.append(evidence_edge(
                            eid=f"edge:address/{para_id}->{eid}",
                            predicate="addressee_of",
                            label=excerpt,
                            paragraph_id=para_id,
                            target_id=eid,
                            paragraph_attrs=inc_attrs,
                            target_attrs=inc_attrs,
                        ))
                        classified = True

                    if not classified:
                        edges.append(evidence_edge(
                            eid=f"edge:ref/{para_id}->{eid}",
                            predicate="referenced_by",
                            label=excerpt,
                            paragraph_id=para_id,
                            target_id=eid,
                            paragraph_attrs=inc_attrs,
                            target_attrs=inc_attrs,
                        ))

            # Reified scene hyperedge: scene as edge containing its paragraphs
            if scene_para_ids:
                edges.append({
                    "id": scene_id,
                    "members": [{"node": pid, "role": "member"}
                                for pid in scene_para_ids],
                    "relationship": "scene_contains",
                    "direction": "undirected",
                    "color": "#FCD9B5",
                })

        # Reified chapter hyperedge: chapter as edge containing its scenes
        if ch_scenes:
            edges.append({
                "id": ch_id,
                "members": [{"node": sid, "role": "member"}
                            for sid in ch_scenes],
                "relationship": "chapter_contains",
                "direction": "undirected",
                "color": "#F8C8A0",
            })

        # Cross-chapter next_paragraph link
        if prev_paragraph_id and prev_para_in_chapter:
            # Already linked within chapter; no inter-chapter link by default
            pass
        prev_paragraph_id = prev_para_in_chapter

    # Reified act hyperedges: act as edge containing its chapters
    for act_n in (1, 2, 3):
        members = [c["id"] for c in nodes
                   if c["type"] == "Chapter" and c["properties"].get("act") == act_n]
        if members:
            edges.append({
                "id": f"act:{act_n}",
                "members": [{"node": cid, "role": "member"} for cid in members],
                "relationship": "act_contains",
                "direction": "undirected",
                "color": "#E8A075",
            })

    # Strip 'type' / 'color' / 'properties' shape into instagraph form
    return {
        "metadata": {
            "createdDate": "2026-04-29",
            "description": "Knowledge graph of The Epic of Elinor Jones (acts 1-3 partial, manuscript). Paragraph-as-node architecture: each paragraph is a vertex; characters/places/themes are vertices; scenes/chapters/acts are reified hyperedges containing their members. Field attrs on paragraphs (word count, has_dialogue, has_ai_dialogue, position).",
            "source": "Harry Tajchman, manuscript files in ~/Writing/the_epic_of_elinor_jones/_final-draft-EoEJ/",
            "extractor": "manuscript_to_hypergraph.py (paragraph splitter + alias-table entity detection); not LLM-based",
        },
        "nodes": nodes,
        "edges": edges,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("inputs", nargs="+", help="Manuscript markdown files (in reading order)")
    ap.add_argument("-o", "--output", required=True, help="Output instagraph JSON file")
    args = ap.parse_args()

    files = [Path(p) for p in args.inputs]
    for f in files:
        if not f.exists():
            print(f"Missing: {f}", file=sys.stderr)
            return 1

    g = build(files)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(g, indent=2), encoding="utf-8")

    print(f"wrote {out}", file=sys.stderr)
    print(f"  nodes: {len(g['nodes']):>4}  edges: {len(g['edges']):>4}", file=sys.stderr)
    type_counts = Counter(n["type"] for n in g["nodes"])
    print(f"  types: {dict(type_counts)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
