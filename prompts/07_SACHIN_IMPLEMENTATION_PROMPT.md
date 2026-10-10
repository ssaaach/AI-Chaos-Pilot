<!-- immediate-demo-update -->

## Latest user priority — local prevention demo within two hours

This addendum reflects the user's updated request and takes priority over the older milestone order below. Deliver one working injection attempt and one system response: stop the unsafe request BEFORE the fault executes and display an error popup. Do not interpret a blocked attempt as a successfully injected outage or a measured service crash.

The popup heading is **Error has occurred**. Its body must say **Injection blocked before execution**, identify the fixed rejection rule and show whether the target stayed healthy. The error occurred in the rejected request; do not claim that the target failed. Never execute a prohibited candidate merely to demonstrate danger.

Use the local demo path immediately when Kubernetes/team modules are unavailable. Label it LOCAL DEMO, use a real separate loopback HTTP target, submit a 90-second service-pause attempt against a fixed 60-second maximum, reject it before dispatch, latch STOP and verify zero dispatched mutations plus target health before/after. All accepted-duration requests remain blocked while execution is unavailable. Reset requires a healthy target; stale or unavailable target health must fail closed. This is prevention evidence, not one of the event's three executed chaos mechanisms.

Keep the existing shared ports and ownership boundaries for later Kubernetes integration. No one duplicates the team's SQL parser, live metric scoring or production runtime in the UI/API. The minimal local demonstration adapter is isolated and has no target mutation capability. Full Day 1/2 experiments, independent live watchdog, SQL execution and learning remain separate later gates.

### Builder and independent tester

- **Tooshita:** owns injection request handling, deterministic preflight rejection, STOP latch and safe reset; tests the runtime behavior.
- **Navya:** independently tests rejection BEFORE dispatch, zero target mutations, healthy target before/after, unavailable target rejection and numerical evidence; owns acceptance evidence.
- **Sachin:** composes ports/API, wires the injection button and accessible error popup, runs end-to-end UI checks and packages demo instructions.
- **Ananya:** supplies the real local target now and the enrolled Kubernetes target/proxy route later; checks reproducible launch.
- **Gautam:** supplies explanations from fixed rule/evidence facts; cannot authorize or bypass rejection. No LLM or learned model is needed for this demo.

### Immediate acceptance gate

1. Launch target, authenticated loopback API and dashboard from written steps.
2. Show a healthy target and a visible LOCAL DEMO provenance banner.
3. Click Inject test error: submit the unsafe proposal, return BLOCK and set STOP without dispatching a target mutation.
4. Show the error popup with rejection reason and healthy/unavailable target status, never a false recovery-success claim.
5. Verify target remains healthy; record request ID, rule, configured/requested duration, source, decision and executed=false. Retain only sanitized numeric/categorical evidence.
6. Test repeat attempts while STOP is latched, healthy reset, unavailable target, malformed requests, authentication and the popup. Mock checks are labelled separately from the real local HTTP test.
7. Keep GitHub upload separate from proof of local behavior. Publish only through available authenticated access; report an unavailable sign-in honestly.

**This person’s immediate task:** Immediate owner task: deliver the working local demo API/dashboard, Inject test error button, STOP state, and accessible popup heading Error has occurred with body Injection blocked before execution. Validate with the real separate HTTP target; update all prompts and provide a runnable bundle and truthful testing status.

---

# Sachin implementation prompt

You are Sachin's local implementation assistant for Bosch Resilience AI. Implement the shared API composition, dashboard and integration workstream, and coordinate the team's deliverables. Deliver functioning code and a tested integration path; do not stop at a plan or replace the other four workstreams with a separately generated application.

## Shared project context

Our team is Ananya, Tooshita, Navya, Gautam and Sachin. We build a Kubernetes resilience platform around pinned Google Online Boutique and a separate synthetic PostgreSQL query lab. The system maps dependencies, ranks bounded faults, measures baseline/fault/recovery and produces AI-ranked findings. A local streaming learner uses sanitized request features and contemporaneous state, updates bounded derived state and discards processed examples. The LLM is a reasoning service, not a continuously retrained model.

Day 1 must show a healthy app, dependency map, baseline, one reversible service outage and a working automatic stop/manual kill switch with verified cleanup. Adaptive rollback is Day 2 work. Day 2 also targets three distinct measured fault mechanisms—Pod termination, Redis connection interruption and bounded network latency—plus ranked findings and five official deliverables. Guarded SQL and incremental learning are additions, not substitutes.

Use one GitHub monorepo, one modular Python/FastAPI backend, React/TypeScript, local kind and lightweight probes. Keep the runtime worker/watchdog independent from the API/UI/model. Read the shared context/interfaces; the original files are research proposals, not proof that their APIs or features exist.

## Your ownership and team boundaries

Own `backend/app/main.py`, `backend/app/api/`, `backend/app/contracts/`, `contracts/v1/`, `frontend/`, root package/dependency locks, `.github/`, `tests/contracts/`, `tests/integration/` and `docs/integration/`. Use branch `feat/sachin-integration`, cluster `bosch-sachin`, context `kind-bosch-sachin`. Your laptop is the default demo machine after the resource check, with Ananya helping reproduce deployment on a backup.

Ananya owns infrastructure, upstream application and topology. Tooshita owns runtime authorization, faults, watchdog, SQL execution and rollback. Navya owns metrics, safe plans, recovery and scoring. Gautam owns SQL AST/policy, reasoning and learner. Import their ports and compose them; do not duplicate policy, metric math, mutations or learning in API handlers or frontend code.

You coordinate integration, but each owner remains responsible for their own tests, documentation and report contribution. Review ownership boundaries and route/schema changes before merging.

## First 30 minutes

Inspect the repo/branch/remotes and identify actual implementations. If the team has no repo, prepare one monorepo under the actual chosen GitHub account/organization, using Apache-2.0 for team code and preserving upstream notices. Verify account/destination before creating or publishing remotely; do not invent a GitHub URL or overwrite an existing repository. Local structure, contracts and fixtures can proceed while destination/authentication is resolved.

Use protected `main`, personal feature branches and one teammate reviewer for each PR. Define a small pull-request template with behavior, tests, setup needs and limits. Avoid long-lived diverging copies or five repositories to merge at the end. GitHub hosts source; local kind runs the application.

Commit the shared version 1 contracts first. Implement Pydantic models and generate JSON schemas/OpenAPI and TypeScript types from one authoritative source. Coordinate Python/Node versions and dependency pins with owners; record tested versions, not an assumed latest stack. Include fixtures for each port so everybody can begin independently.

## Day 1 backend composition

Implement a FastAPI composition root using injected `PlatformPort`, `RuntimePort`, `TelemetryPort` and `IntelligencePort`. Provide explicit `fixture`, `live` and `replay` modes; selecting live must never silently fall back to fixture data. Keep mutation routes unavailable in fixture/replay mode unless exercising a clearly fake runtime for tests.

Register shared `/api/v1` routes for health, topology/state, catalog/planning/validation, proposal approval/start, run status/events/stop, emergency STOP/reset, SQL analysis, learning status, analysis and reports. Add SQL execution routes only when Tooshita's bounded runtime is ready. Day 2 action routes are disabled today.

Use authenticated local operators, a loopback-bound API, strict CORS origins, request size limits and safe error bodies. Keep runtime approval enforcement in Tooshita's module. Do not make localhost or a disabled frontend button the only authorization check. Prevent accidental browser-driven mutations through the selected authentication/CSRF strategy.

Start jobs with 202 and IDs, expose real state, and avoid blocking an API request for the full experiment. Use SSE or bounded polling; reconnection must not re-execute an action. Idempotency keys and approval/token checks belong to the runtime. A STOP receipt means cleanup was requested, not that recovery is already verified.

Sanitize request logging and exception output. Never persist SQL text, parameter values, result rows, credentials or learner examples. Browser console, localStorage, sessionStorage, analytics and error-reporting tools must not retain source query input. Keep a bounded editor state in RAM and clear source input when processing is complete or expired; sanitized template examples may remain static documentation.

## Dashboard scope

Build three primary views with a persistent cluster/context/namespace banner, data provenance and reachable STOP control:

1. System overview: verified dependency graph, ready/desired workloads, current and baseline metrics, freshness/quality, active run and learning status. Display missing as missing, not green. Learning status shows processed/update counters, drift/cold start, queue drops and the configured retention policy.
2. Operations: tabs for chaos and the guarded SQL console. Chaos shows ranked proposals, rationale, expected impact, validation, exact parameters, explicit approval and the live state timeline. SQL shows analysis before execution, ALLOW/WARN/BLOCK, rule IDs, estimated rows/bytes, uncertainty, suggestions and explicit approval of a re-analyzed safe operation.
3. Findings: measured baseline/fault/recovery, ranked hypotheses/fixes with evidence references, score components, limitations and report download. Day 2 can add one reviewed action diff and an opt-in auto-revert control when the runtime supports it.

Use clear labels `live`, `fixture`, `replay`, `estimated`, `measured`, `predicted` and `supported in this run`. Do not draw charts from zeros when data is missing. Keep risk and resilience scores visually separate. Do not call an estimated block a verified prevented crash.

The SQL console protects requests through the team's API; direct database clients are outside its scope. Do not imply universal interception. Explain that pagination changes the returned result set and that approved execution may truncate at declared caps. Provide cancel for active reads, not a misleading rollback button for delivered output.

Keep UI readable at demo distance. Avoid a chatbot, seven pages, decorative fake production metrics and frontend reimplementation of scoring/safety. Real charts come from Navya's summaries; explanations come from Gautam's validated analysis.

## Integrate throughout both days

First merge contracts/fixtures and the composition shell. Then integrate Ananya's topology and Navya's live state, followed by Tooshita's watchdog/first fault and the visible Day 1 checkpoint. Integrate Gautam's guard/statistics in parallel. Do not wait until everyone says their module is finished before the first real run.

During Day 2, verify all three required fault mechanisms, query analysis and bounded approved execution, incremental outcome learning and evidence-based reporting. Add adaptive rollback only after core integration is stable. The operator must opt in for that exact reversible change; the model cannot authorize a patch. Preserve approval expiry, conflict, cleanup-failure and missing-metric behavior in the UI.

Schedule at least two merge checkpoints on Day 1 and frequent small merges on Day 2. Freeze new features with the final quarter of the available time reserved for clean deployment and submission. Use the actual event deadline, not older draft wall-clock times. Heavy monitoring, million-row seeding, decorative UI and generalized autonomous actions are the first cuts.

## Reports and official deliverables

Generate sanitized Markdown or HTML reports from immutable `RunSummary` and validated `AnalysisResult`. Include sandbox/application revision, selected fault and reason, workload/sample counts, measured phase values, stop/cleanup/recovery facts, ranked weaknesses/fixes, evidence references, scoring configuration and limitations. No raw SQL or source result data is required to support the report.

Coordinate all five final deliverables:

1. Public repository with reproducible setup, run, safety and cleanup instructions.
2. Video of three minutes or less showing injection, observed impact and reporting.
3. One page or slide covering components, AI decision flow and safety controls.
4. Findings report with ranked weaknesses and recommended fixes based on real sandbox evidence.
5. Team form listing Ananya, Tooshita, Navya, Gautam and Sachin, team name, actual tools/models, libraries and data sources. Do not invent unknown model/version/team-name fields.

Suggested video allocation: 20 seconds for app/map; 30 seconds for SQL risk and transient learning behavior; 55 seconds for approved fault, observed impact and safety stop; 40 seconds for ranked findings and the three completed mechanisms; 25 seconds for learning/optional rollback evidence; 10 seconds for scope and limitations. Adapt the optional section to what actually worked. A recorded run is labelled replay and uses authentic measurements.

## Acceptance tests

Run contract validation and schema/type drift checks, backend unit/API tests, frontend build and meaningful UI checks for approval, expired state, fixture labels, STOP accessibility, missing metrics, pending versus verified cleanup and report values. CI uses fake ports and mock providers without live keys or shared clusters.

Perform a deliberate own-cluster integration run from written deployment steps: healthy app, graph, baseline, approved fault, threshold stop, verified recovery and report. Then exercise each Day 2 fault and query approval/cancel/cap behavior. Confirm closing the browser or stopping the model does not disable cleanup. Test restart resets learner and expires SQL intents while fault journal reconciliation still works.

Check report numbers against the exact summary hash. Inspect network payloads, browser storage and retained logs for prohibited raw data. Test generated artifacts/links from another machine and a logged-out browser. Record what ran and what remains unverified; a build alone does not prove a chaos experiment.

## Handoff and completion

Keep `main` runnable, publish stable type/API generation commands, real configuration examples without secrets, integration test results and current blockers. Each PR should be reviewable without the chat history. Create a tested demo release only after clean-run verification; do not publish placeholder results as evidence.

End sessions with files changed, executed checks/results, integration status, unresolved issues, active-resource status and outstanding submission items. Your workstream is done when a teammate can reproduce the full workflow on a clean demo sandbox, every screen reflects truthful state, bounded learning and safety survive UI/model failure, and all five deliverables open and meet the event rules.
