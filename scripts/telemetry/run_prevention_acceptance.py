"""Run the LOCAL DEMO prevention acceptance gate and write sanitized evidence.

Usage:
    python scripts/telemetry/run_prevention_acceptance.py            # spawns the reference target
    python scripts/telemetry/run_prevention_acceptance.py --target http://127.0.0.1:8099

What this does and does not prove
---------------------------------
It observes the target over real HTTP before and after an unsafe attempt, reads
the target's own mutation witness, and checks the runtime's execution spy.

**The BLOCK decision is currently supplied by a stand-in** (``--guard stub``),
because Tooshita's preflight guard is not merged yet. The evidence says so in its
notes. Once her guard lands, replace ``stub_guard`` with a call into it; the
verifier and the evidence format do not change. Until then this run shows the
*verification harness* works against a real socket -- it is not yet proof that
the production guard rejects the request.

Output is numeric and categorical only, and carries no resilience score.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import reference_target  # noqa: E402

from backend.app.telemetry.prevention import (  # noqa: E402
    CountingExecutionSpy,
    PreventionVerifier,
    TargetHealthProbe,
    assert_no_score_for_prevented_attempt,
)

REQUESTED_SECONDS = 90.0
MAX_SECONDS = 60.0
RULE_ID = "max_fault_duration_seconds"


def stub_guard(requested_seconds: float, max_seconds: float) -> tuple[str, bool]:
    """Stand-in for Tooshita's preflight guard. Returns (decision, executed).

    It never touches the spy or the target, mirroring the contract the real
    guard must meet: rejection happens before any executor invocation.
    """
    if requested_seconds > max_seconds:
        return "BLOCK", False
    return "BLOCK", False  # execution is unavailable in the LOCAL DEMO


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", help="existing loopback target URL")
    parser.add_argument("--out", default=str(ROOT / "reports" / "local_demo_prevention.json"))
    args = parser.parse_args()

    server = None
    if args.target:
        base_url = args.target
    else:
        reference_target.reset_state()
        server, _thread, port = reference_target.serve_in_thread()
        base_url = f"http://127.0.0.1:{port}"
        print(f"spawned reference target at {base_url}")

    try:
        probe = TargetHealthProbe(base_url)
        spy = CountingExecutionSpy()
        verifier = PreventionVerifier(
            probe, spy, configured_max_duration_seconds=MAX_SECONDS
        )

        before = probe.read_health()
        spy_before = spy.invocation_count

        decision, executed = stub_guard(REQUESTED_SECONDS, MAX_SECONDS)

        after = probe.read_health()
        evidence = verifier.verify_rejected_attempt(
            request_id="req_localdemo_acceptance",
            rule_id=RULE_ID,
            decision=decision,
            executed=executed,
            requested_duration_seconds=REQUESTED_SECONDS,
            stop_latched=True,
            health_before=before,
            health_after=after,
            spy_count_before=spy_before,
            extra_notes=(
                "BLOCK decision was supplied by a stand-in guard, not Tooshita's "
                "runtime; this run verifies the verification harness, not the "
                "production guard",
            ),
        )
        assert_no_score_for_prevented_attempt(evidence)

        extra = [
            verifier.verify_blocked_while_execution_unavailable(
                requested_duration_seconds=30.0, decision="BLOCK"
            ).as_dict(),
        ]
        payload = evidence.as_dict()
        payload["supplementary_checks"] = extra

        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, sort_keys=True))

        print(f"\nLOCAL DEMO prevention acceptance -> {evidence.verdict}")
        print(f"  observation mode : {evidence.observation_mode.value}")
        print(f"  decision/executed: {evidence.decision} / {evidence.executed}")
        print(f"  duration         : requested {REQUESTED_SECONDS}s vs cap {MAX_SECONDS}s")
        print(f"  executor calls   : {evidence.executor_invocations_reported}")
        print(f"  target mutations : {evidence.target_observed_mutations} (corroborated={evidence.corroborated})")
        print(f"  health           : {evidence.health_before.value} -> {evidence.health_after.value}")
        for c in evidence.checks:
            print(f"  [{'PASS' if c.passed else 'FAIL'}] {c.check_id}: {c.observed}")
        print(f"\nevidence written to {out}")
        return 0 if evidence.verdict == "ACCEPTED" else 1
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
