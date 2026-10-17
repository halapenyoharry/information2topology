"""Regression tests for adapters/hypergraph_to_dyadic.py.

The reified-edge case (an edge whose id is also a node id, spec S4) was first
exercised by a real file on 2026-10-17 and exposed that the adapter dropped the
edge's own attrs from the `edge-as-node` row, so every renderer drew the
reified edge as a category-less entity. See correspondence/json-visual-viewer.md,
decision log, 2026-10-17.
"""
import copy
import unittest

from adapters.hypergraph_to_dyadic import normalize


def fixture():
    """Three entities, one reified arity-2 edge that another edge points at,
    one plain arity-2 edge, one 3-member containment edge."""
    return {
        "metadata": {"topothink-version": "0.1", "schema:name": "fixture"},
        "nodes": [
            {"id": "a", "attrs": {"schema:name": "A"}},
            {"id": "b", "attrs": {"schema:name": "B"}},
            {"id": "s", "attrs": {"schema:name": "Source"}},
            {"id": "box", "attrs": {"schema:name": "Box"}},
            # Reified: the edge id appears here as a node too.
            {
                "id": "edge:a-builds-b",
                "attrs": {"schema:name": "a-builds-b (reified)", "i2t:reified": True},
            },
        ],
        "edges": [
            {
                "id": "edge:a-builds-b",
                "directed": True,
                "attrs": {
                    "i2t:predicate": "builds",
                    "i2t:edge_category": "state_change",
                    "i2t:edge_category_secondary": None,
                    "i2t:note": "the write rule",
                },
            },
            {
                "id": "edge:s-grounds-rule",
                "directed": True,
                "attrs": {"i2t:predicate": "grounds", "i2t:edge_category": "reference"},
            },
            {
                "id": "edge:box-contains",
                "directed": False,
                "attrs": {"i2t:predicate": "contains", "i2t:edge_category": "containment"},
            },
        ],
        "incidences": [
            {"edge": "edge:a-builds-b", "node": "a", "role": "source"},
            {"edge": "edge:a-builds-b", "node": "b", "role": "target"},
            {"edge": "edge:s-grounds-rule", "node": "s", "role": "source"},
            {"edge": "edge:s-grounds-rule", "node": "edge:a-builds-b", "role": "target"},
            {"edge": "edge:box-contains", "node": "box", "role": "container"},
            {"edge": "edge:box-contains", "node": "a", "role": "member"},
            {"edge": "edge:box-contains", "node": "b", "role": "member"},
        ],
    }


class TestHypergraphToDyadic(unittest.TestCase):
    def setUp(self):
        self.doc = fixture()
        self.out = normalize(copy.deepcopy(self.doc))
        self.nodes = {n["id"]: n for n in self.out["nodes"]}

    def test_metadata_marks_projection(self):
        self.assertEqual(self.out["metadata"]["i2t:relation_to_canonical"], "dyadic-projection")
        self.assertEqual(self.out["metadata"]["originalCounts"], {"nodes": 5, "edges": 3, "incidences": 7})

    def test_reified_edge_row_carries_edge_attrs(self):
        row = self.nodes["edge:a-builds-b"]
        self.assertEqual(row["kind"], "edge-as-node")
        attrs = row["attrs"]
        # The node row's own keys survive untouched.
        self.assertEqual(attrs["schema:name"], "a-builds-b (reified)")
        self.assertTrue(attrs["i2t:reified"])
        self.assertEqual(row["label"], "a-builds-b (reified)")
        # The edge row's keys are merged in, so the row is still legible as a relation.
        self.assertEqual(attrs["i2t:predicate"], "builds")
        self.assertEqual(attrs["i2t:edge_category"], "state_change")
        self.assertEqual(attrs["i2t:note"], "the write rule")

    def test_node_row_wins_on_collision(self):
        doc = fixture()
        doc["nodes"][4]["attrs"]["i2t:predicate"] = "author-wrote-this"
        out = normalize(doc)
        row = {n["id"]: n for n in out["nodes"]}["edge:a-builds-b"]
        self.assertEqual(row["attrs"]["i2t:predicate"], "author-wrote-this")

    def test_reified_edge_incidence_links(self):
        links = [l for l in self.out["links"] if "edge:a-builds-b" in (l["source"], l["target"])]
        incidence = [l for l in links if l.get("layer") == "builds"]
        self.assertEqual(len(incidence), 2)
        self.assertEqual({(l["source"], l["target"], l["role"]) for l in incidence},
                         {("a", "edge:a-builds-b", "source"), ("edge:a-builds-b", "b", "target")})
        # The edge that points AT the reified edge is a plain link with its own attrs.
        pointing = [l for l in links if l.get("layer") == "grounds"]
        self.assertEqual(len(pointing), 1)
        self.assertEqual(pointing[0]["source"], "s")
        self.assertEqual(pointing[0]["attrs"]["i2t:edge_category"], "reference")

    def test_nary_edge_becomes_hyperedge_row(self):
        row = self.nodes["edge:box-contains"]
        self.assertEqual(row["kind"], "hyperedge")
        self.assertEqual(row["attrs"]["i2t:edge_category"], "containment")
        spokes = [l for l in self.out["links"] if l["source"] == "edge:box-contains"]
        self.assertEqual(sorted(l["role"] for l in spokes), ["container", "member", "member"])

    def test_entities_stay_plain_nodes(self):
        for nid in ("a", "b", "s", "box"):
            self.assertEqual(self.nodes[nid]["kind"], "node")

    def test_input_document_is_not_mutated(self):
        doc = fixture()
        before = copy.deepcopy(doc)
        normalize(doc)
        self.assertEqual(doc, before)


if __name__ == "__main__":
    unittest.main()
