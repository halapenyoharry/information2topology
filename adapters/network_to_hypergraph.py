#!/usr/bin/env python3
"""Adapter: harold's home-network JSON → TopoThink hypergraph.

Framing (the picker-equivalent, hard-coded for this source shape):
    V (vertices)   = computers (each entry under .computers)
    E (edges)      = anything that happens between them — subnet membership
                     and routing relations, expressed as hyperedges
    I (incidences) = how each computer (or subnet) participates — interface
                     name, IP on this subnet, role on this route, MTU, etc.
    attrs          = everything else (config, os, services, notes, ...)

Subnet membership: each subnet becomes one hyperedge connecting all hosts
that have a non-null IP on it. The subnet's own attrs (media, router, notes)
ride on the edge; each host's incidence carries the IP and the ip-key
that placed the host on this subnet.

Routes: each named route becomes a reified hyperedge (its id appears in
both `nodes` and `edges`). Hops are folded into the route node's attrs;
incidences derived from the hops give roles `source_host` / `router` /
`destination_host` and `source_subnet` / `destination_subnet`.

Hosts with all-null IPs (laptops not yet attached) appear as isolated
nodes — they participate in zero edges. That's faithful to the data.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


# Map of "ip key on a host's network section" → "subnet CIDR"
IP_KEY_TO_SUBNET = {
    "ip_10gbe":     "192.168.1.0/24",
    "ip_wifi":      "192.168.3.0/24",
    "ip_tailscale": "100.64.0.0/10",
    "ip_tb_bridge": "10.0.0.0/24",
}


def adapt(net: dict) -> dict:
    out = {
        "metadata": {
            "topothink-version": "0.1",
            "adapter": "network_to_hypergraph.py",
            "framing": "hosts-as-V; subnet-membership and routes as hyperedges; interface+IP as incidence attrs",
            "source-meta": net.get("_meta", {}),
        },
        "nodes": [],
        "edges": [],
        "incidences": [],
    }

    computers = net.get("computers", {}) or {}
    subnets   = net.get("subnets", {}) or {}
    routing   = net.get("routing", {}) or {}

    # ---------------- 1. Hosts as vertices ----------------
    for name, host in computers.items():
        attrs = {"i2t:type": "host"}
        for k in ("type", "config", "os", "use", "services", "ollama",
                  "ip_forwarding", "firewall", "notes"):
            if k in host:
                attrs[k] = host[k]
        out["nodes"].append({"id": f"host:{name}", "attrs": attrs})

    # ---------------- 2. Subnets as hyperedges (containers, not lines) ----------------
    # Subnets are categorical group-membership relations. They have many arity-≥-3
    # incidences and no other entity ever points AT them, so they don't earn
    # reification (no node duplicate). render_hint="container" tells renderers
    # that support it to draw these as Venn-style enclosing regions, with member
    # hosts inside, rather than as a synthetic node with dyadic links to each member.
    # Multi-subnet hosts (like lothal, which sits in all four) become
    # overlapping-region members. Renderers that don't support container
    # rendering can fall back to the synthetic-node dyadic-projection
    # via hypergraph_to_dyadic.py — render_hint travels through automatically.
    for cidr, subnet in subnets.items():
        edge_id = f"subnet:{cidr}"
        edge_attrs = {
            "i2t:predicate": "subnet_membership",
            "render_hint": "container",
            "cidr": cidr,
        }
        for k in ("media", "router", "notes"):
            if k in subnet:
                edge_attrs[k] = subnet[k]
        out["edges"].append({"id": edge_id, "directed": False, "attrs": edge_attrs})

        for name, host in computers.items():
            net_section = host.get("network", {}) or {}
            for ip_key, mapped_cidr in IP_KEY_TO_SUBNET.items():
                if mapped_cidr == cidr and net_section.get(ip_key):
                    out["incidences"].append({
                        "edge": edge_id,
                        "node": f"host:{name}",
                        "role": "member",
                        "attrs": {
                            "ip": net_section[ip_key],
                            "ip_key": ip_key,
                        },
                    })

    # ---------------- 3. Routes as reified hyperedges ----------------
    for route_name, route in routing.items():
        edge_id = f"route:{route_name}"

        # As a node (reification — other things can talk about this route)
        node_attrs = {"i2t:type": "route", "i2t:reified": True}
        for k in ("purpose", "applied", "status",
                  "observed_path_latency_ms", "observed_ttl_at_dest",
                  "verified_2026_04_22", "notes"):
            if k in route:
                node_attrs[k] = route[k]
        if "hops" in route:
            node_attrs["hops"] = route["hops"]
        out["nodes"].append({"id": edge_id, "attrs": node_attrs})

        # As an edge — three host participants, drawn as a directed line.
        # Subnet refs ride as attrs on the route and on each host's incidence
        # (rather than as separate participants), since the subnet is contextual
        # to the route, not a thing the route asserts statements ABOUT.
        subnets_involved = sorted({
            h.get("destination")
            for h in (route.get("hops") or {}).values()
            if isinstance(h, dict) and h.get("destination")
        })
        edge_attrs = {
            "i2t:predicate": "routes_via",
            "render_hint": "line",
            "applied": route.get("applied"),
            "status":  route.get("status"),
            "subnets_involved": subnets_involved,
        }
        out["edges"].append({"id": edge_id, "directed": True, "attrs": edge_attrs})

        hops = route.get("hops", {}) or {}

        if "forwarding" in hops and hops["forwarding"].get("host"):
            f = hops["forwarding"]
            out["incidences"].append({
                "edge": edge_id,
                "node": f"host:{f['host']}",
                "role": "router",
                "attrs": {
                    "sysctl": f.get("sysctl"),
                    "live":   f.get("live"),
                },
            })

        if "route_on_tropy" in hops:
            h = hops["route_on_tropy"]
            out["incidences"].append({
                "edge": edge_id,
                "node": "host:tropy",
                "role": "source_host",
                "attrs": {
                    "interface": h.get("interface"),
                    "gateway":   h.get("gateway"),
                    "destination_subnet": h.get("destination"),
                    "live":      h.get("live"),
                },
            })

        if "route_on_lumen" in hops:
            h = hops["route_on_lumen"]
            out["incidences"].append({
                "edge": edge_id,
                "node": "host:lumen",
                "role": "destination_host",
                "attrs": {
                    "interface": h.get("interface"),
                    "gateway":   h.get("gateway"),
                    "mtu":       h.get("mtu"),
                    "advmss":    h.get("advmss"),
                    "destination_subnet": h.get("destination"),
                    "live":      h.get("live"),
                },
            })

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", help="Input network JSON (harold's home-network shape)")
    ap.add_argument("-o", "--output",
                    help="Output hypergraph JSON (default: derived from input filename)")
    args = ap.parse_args()

    inpath = Path(args.input)
    with open(inpath) as f:
        net = json.load(f)

    hypergraph = adapt(net)

    if args.output:
        outpath = Path(args.output)
    else:
        outpath = inpath.with_name(inpath.stem + ".hypergraph.topothink.json")

    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(hypergraph, f, indent=2)

    print(f"wrote {outpath}", file=sys.stderr)
    print(f"  nodes: {len(hypergraph['nodes']):>4}  "
          f"edges: {len(hypergraph['edges']):>4}  "
          f"incidences: {len(hypergraph['incidences']):>4}", file=sys.stderr)

    # Predicate breakdown
    from collections import Counter
    preds = Counter((e.get("attrs") or {}).get("i2t:predicate", "(none)")
                    for e in hypergraph["edges"])
    print("  predicates:", dict(preds), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
