#!/usr/bin/env python3
"""Export a fixture or UID-enrolled, read-only Kubernetes topology snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.platform.adapter import KubectlPlatform, load_fixture  # noqa: E402
from backend.app.platform.models import SandboxIdentity  # noqa: E402


def mermaid(snapshot: dict) -> str:
    lines = ["flowchart LR"]
    for node in snapshot["nodes"]:
        node_id = node["resource_id"].replace("/", "_").replace("-", "_")
        lines.append(f'  {node_id}["{node["kind"]}: {node["name"]}"]')
    known = {n["resource_id"] for n in snapshot["nodes"]}
    for edge in snapshot["edges"]:
        if edge["caller"] not in known or edge["dependency"] not in known:
            continue
        caller = edge["caller"].replace("/", "_").replace("-", "_")
        dependency = edge["dependency"].replace("/", "_").replace("-", "_")
        lines.append(f"  {caller} -->|{edge['protocol'] or 'dependency'}| {dependency}")
    if not snapshot["edges"]:
        lines.append("  note[No dependency edges were verified]")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture", type=Path, help="explicit synthetic fixture JSON")
    source.add_argument("--identity", type=Path, help="sandbox.identity.json from enroll.ps1")
    parser.add_argument("--context", help="must equal the enrolled Kubernetes context")
    parser.add_argument("--namespace", default="boutique")
    parser.add_argument("--out", type=Path, default=Path("topology.json"))
    parser.add_argument("--diagram", type=Path, default=Path("topology.mmd"))
    args = parser.parse_args()

    try:
        if args.fixture:
            platform = load_fixture(args.fixture)
            sandbox_id = platform.snapshot.sandbox_id
        else:
            if not args.context:
                parser.error("--context is required with --identity")
            identity_data = json.loads(args.identity.read_text(encoding="utf-8"))
            if identity_data.get("schema_version") != "1.0":
                raise ValueError("unsupported sandbox identity schema")
            identity_data.pop("schema_version", None)
            identity = SandboxIdentity(**identity_data)
            platform = KubectlPlatform(identity, args.context, args.namespace)
            sandbox_id = identity.sandbox_id
        snapshot = platform.get_topology(sandbox_id).to_dict()
        args.out.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
        args.diagram.write_text(mermaid(snapshot), encoding="utf-8")
        print(f"Wrote {snapshot['source']} topology to {args.out} and {args.diagram}")
        return 0
    except Exception as exc:  # errors contain no candidate SQL, credentials, or query data
        print(f"Topology export failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
