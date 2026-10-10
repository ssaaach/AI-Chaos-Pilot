# Gautam's intelligence workstream: handoff to Sachin

This branch adds the intelligence module, adapted to the authoritative models in `app.contracts` and to the async `IntelligencePort`. It was built and tested on fakes and synthetic data only. No cluster, lab database or live model was used. Full details are in `docs/intelligence/README.md`.

## What this branch changes

| Path | Change |
|---|---|
| `backend/app/intelligence/` | New module. `IntelligenceService` implements `IntelligencePort`. It imports shared types only from `app.contracts`; its internal working types live in `internal.py` and never leave the module. |
| `tests/intelligence/` | Unit, policy, learner, planner, diagnosis and reasoning tests, plus `test_integration_api.py`. That file plugs the service into your real `create_app` with fixture ports and calls `/sql/analyze`, `/experiments/plan`, `/runs/{id}/analysis` and `/learning/status`. |
| `fixtures/v1/intelligence/` | Synthetic fixtures. They are regenerated with `PYTHONPATH=backend python -m app.intelligence.export_fixtures`. |
| `docs/intelligence/README.md` | Grammar, policy rules, features, limits, rubrics, and integration needs. |
| `pyproject.toml` | Adds `pglast==8.5` and `river==0.26.1`. |
| `requirements.lock` | Adds `pglast`, `river`, `numpy`, `scipy` and `narwhals`. |
| `scripts/lock_dependencies.py` | Adds `pglast` and `river` to the roots, so regenerating the lock keeps them. |
| `push-test.txt` | Removed. It came in with PR #1 and was only an access test. |

No file under `contracts/`, `backend/app/contracts/`, `backend/app/api/`, `backend/app/adapters/` or `frontend/` is changed. Fixture and demo modes still use `FixtureIntelligence`.

## Decisions for you

1. **Run target.** `RunSummary` has no `target_id`, so the diagnosis cannot attribute impact to a dependency. Either add `target_id` to `RunSummary`, or have the live factory call `IntelligenceService.note_run_target(run_id, target_id)`. Until then, findings are reported per operation, and the report states that limitation.
2. **Live wiring.** Construct `IntelligenceService(allowlist)` in the `LIVE_PORTS_FACTORY`. The allowlist must come from Ananya's real lab schema; `fakes.LAB_ALLOWLIST_DATA` is a placeholder. No live model transport is registered; that needs an approved provider, model and spend limit.
3. **Estimator parameter shape.** `ports.PlanEstimator` declares `parameters: dict`, but Navya's estimator takes a sequence. I pass a positional list, because `$n` placeholders are positional. The API's `parameters` mapping must use keys `"1".."n"`; any other keys are blocked as SQL-015.

## Not changed, but noticed

- `requirements.txt` (telemetry) pins pydantic 2.12.3, while the lock pins 2.11.5. The intelligence tests pass on 2.11.5.
- `telemetry/learning.py` emits observations from Navya's provisional models. The learner accepts the shared `LearningObservation`, so her channel should switch to `app.contracts` types when its shim does.

## Verification performed

These checks ran locally on Windows with CPython 3.13 and the exact `requirements.lock` versions. CI runs 3.12; Linux cp312 wheels exist for every added pin.

- `python -m pytest -q` (whole repository): all tests passed. The exact count is in the PR description.
- `python scripts/export_contracts.py --check`: passed.
- No generated contract or frontend files changed.
- The frontend build and the Playwright suite were **not** run locally. CI runs them, and no frontend files changed.
