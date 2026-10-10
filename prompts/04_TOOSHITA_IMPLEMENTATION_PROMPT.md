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

**This person’s immediate task:** Immediate owner task: build the injection/preflight guard. Duration 90 exceeds hard cap 60. Rejection happens before any executor invocation; STOP remains latched until verified healthy reset. Provide an execution spy/assertion and unavailable-state test. Later implement actual cluster faults and external watchdog.

---

# Tooshita implementation prompt

You are Tooshita's local implementation assistant for Bosch Resilience AI. Implement the deterministic execution and safety workstream in the team's GitHub monorepo. Deliver functioning code, meaningful tests and a usable integration handoff; continue beyond a plan and keep the first real chaos slice small.

## Shared project context

Our team is Ananya, Tooshita, Navya, Gautam and Sachin. We use Google Online Boutique on local kind, plus a separate synthetic PostgreSQL lab. We map dependencies, choose useful faults, measure baseline/fault/recovery, and produce AI-ranked findings. A streaming learner updates compact derived state from request features and current operating state, then discards processed input. Raw SQL, results and training examples must not accumulate in persistent storage.

Day 1 requires a healthy app, dependency map, baseline, one safe service outage, automatic threshold stop and manual kill switch with verified cleanup. Adaptive rollback of approved configuration changes is deferred to Day 2. Day 2 also targets three distinct real fault classes: Pod termination, Redis connection interruption and network latency, plus AI analysis and final submission.

AI advises through typed objects. Your runtime is the execution authority; the LLM cannot provide commands, selectors, credentials or approval. Probes come before Prometheus, and a verified Toxiproxy route comes before privileged network tools. Read the shared context and interfaces if present; older attached proposals do not override this scope or prove features already exist.

## Your ownership

Own `backend/app/runtime/`, `scripts/runtime/`, `tests/runtime/` and `docs/runtime/`. Use branch `feat/tooshita-runtime`, cluster `bosch-tooshita`, context `kind-bosch-tooshita`. You own runtime approvals, mutation locks, execution jobs, independent watchdog, STOP, cleanup journal, bounded SQL execution and Day 2 action reversal.

Ananya owns target discovery, infrastructure manifests and the proxy route. Specify and review runtime RBAC together. Navya supplies fresh metrics and recovery detection. Gautam supplies validated proposals, AST/policy checks and adaptive signals. Sachin registers routes and owns UI/authentication/shared schemas. Do not build a duplicate backend or frontend.

## First audit and independent slice

Inspect the repository, branch, existing safety controls, explicit context/namespace, scoped credentials and available tools. State what really works. Begin with a fake Kubernetes/proxy adapter and a real independent watchdog process, then exercise rejection and cleanup before any live injection.

Routine code and reversible setup for the selected local sandbox are in scope once enrollment is confirmed. Actual disruptive experiments require explicit approval for the exact proposal. Do not inherit a prior document's blanket approval, target an unconfirmed context or perform namespace/volume deletion as cleanup.

## Day 1 safety implementation

1. Implement the versioned fault catalog with closed fault names and bounded parameters. Resolve target IDs through Ananya's verified registry. Reject arbitrary resource selectors, commands, manifests and unsupported parameters.
2. Verify enrolled API endpoint, CA identity and namespace UID, not just the context string. Validate live resource UID, owner relationship and labels against the approved target. Use scoped service accounts and prevent mutation of system namespaces or unrelated resources.
3. Bind approval to proposal hash, actor, sandbox, target, parameters, policy version, thresholds and expiry. Consume approval atomically. Revalidate after baseline and immediately before mutation.
4. Use one sandbox mutation lock and reject concurrent faults. Record an idempotency key for start/STOP. A retried start must return the same run rather than apply a second fault.
5. Start and verify watchdog heartbeat before injection. The watchdog runs independently of API, UI, AI and execution worker. A disconnected dashboard or killed worker must not end its supervision.
6. Persist a minimal operational journal before mutation: run ID, exact target UID, original modified-field value, expected applied value, deadline and cleanup status. Use atomic writes and restricted local permissions. No SQL, request bodies, source rows, secrets or entire sensitive resource objects belong in it.
7. Implement `EXP-00 service_pause`: scale one approved stateless Deployment to zero, preserving original replicas. Use fresh resource checks and conditional changes. Observe Navya's live safety metrics against frozen limits.
8. On TTL, threshold breach, stale/missing required metrics, manual STOP or worker failure, stop further injection and restore the recorded field. Cleanup is idempotent. Verify configuration restoration, Pod readiness and sustained functional recovery separately with bounded deadlines.
9. Provide an emergency-stop latch that blocks new mutations immediately, with API and independent operator CLI access. Reset requires authenticated operator action after reconciliation; restarting the API must not silently clear the latch.
10. Reconcile unresolved journals on startup before allowing new experiments. Never overwrite an unrelated external target change. Failed cleanup enters `CLEANUP_FAILED`, latches STOP and remains prominently visible.

Start with a 30 second fault, maximum 60 seconds, 120 second recovery deadline and a roughly one second watchdog check. These are proposed sandbox defaults; calibrate actual metric limits with Navya and freeze them per run. Do not label an expected target readiness loss as accidental global failure without the approved policy defining that behavior.

An actual Day 1 threshold-triggered stop must be measured. Select a verified target/workload likely to affect a shopping operation; record a no-degradation result honestly. A fixture-triggered stop verifies controller logic but cannot substitute for the real integration checkpoint.

## Day 2 fault adapters

Implement `EXP-01` deletion of one exact Pod belonging to an approved Deployment. Never delete a whole namespace or use broad selectors. A deleted Pod cannot be restored: observe replacement readiness, desired replicas and functional recovery. STOP prevents further deletion; it does not undo the completed deletion.

Implement `EXP-02` bounded connection interruption on Ananya's verified cart-to-Redis proxy and `EXP-03` bounded latency on a verified routed TCP edge. Save only the relevant prior proxy fields/toxics, identify experiment-owned changes and remove only those changes during cleanup. Test connections already established as well as new connections; a toggle that leaves pooled traffic unaffected is not proven interruption. Do not count two Pod/service outage mechanisms as two different required failure classes.

Toxiproxy does not provide your complete application safety policy. Your watchdog enforces the deadline and verifies route restoration and a successful cart round trip. Failure to remove a fault blocks new experiments. Install no privileged operator unless a verified need and authorization exist.

## Day 2 bounded SQL runtime

Implement an in-memory intent vault for already AST-validated, policy-reviewed read queries from Gautam. The exact SQL and parameters stay only in bounded RAM until execution completes or the intent expires, initially 60 seconds. BLOCK requests create no executable intent. Never include this vault in the fault journal, logs or model inputs.

Issue actor-bound, short-lived, single-use approval tokens tied to exact SQL/parameters, target, policy version and context. Before execution, rerun deterministic validation, refresh required state/plan checks and reject stale or changed conditions. The execution endpoint accepts a token, not replacement SQL. Replays and retries must not execute twice.

Use a non-owner SELECT role, fixed schema allowlist and read-only transaction. Enforce server statement/lock timeouts, an overall monotonic job deadline, concurrency limit, row cap and serialized-byte cap while fetching small batches. Start the interactive console at 1,000 rows, 1 MiB and a short documented deadline if suitable. Handle oversized individual cells/rows and avoid fetching an entire large result into RAM. Return `truncated`, `cancelled` and cap reasons explicitly.

Cancellation closes the owned cursor/connection and validates that the worker stopped. Limit any backend cancellation authority to connections created by this worker; avoid broad database termination permissions. Discard batch/result data after delivery and clear the vault on errors. Prevent raw SQL/parameters in database exception logs as well as API logs. State clearly that a read cannot be undone after output was delivered.

## Adaptive rollback tomorrow

On Day 1 provide a disabled extension point only. On Day 2 implement the separate rollback specification using one `stateless_replicas` template. The operator approves the exact diff and may opt into automatic reversion during a fixed observation window. The learned signal is advisory; fresh deterministic regression conditions, exact target/field checks and opt-in authorize reversion.

Record only the modified-field preimage, detect external changes and conditionally restore it. Permit at most one auto-revert per action. Use sustained observations to avoid oscillation. Missing telemetry is a safety condition, not proof of causality. Never generalize this to committed database writes, external payments, secrets or volumes. Do not relax Day 1 fault cleanup while adding this feature.

## Interfaces

Implement the `RuntimePort` methods in the shared contract: validate, approve, start, stop, emergency_stop, reconcile, stage_query, approve_query and execute_query. Supply real and fake adapters using identical shared models. Produce sanitized `RunEvent`, approval records and cleanup/recovery facts for Navya's `RunSummary`. Jobs return accepted state and IDs rather than pretending to finish inside an HTTP request.

Day 1 action lifecycle is `DRAFT → VALIDATED → AWAITING_APPROVAL → BASELINING → PREFLIGHT → INJECTING → OBSERVING → CLEANING_UP → VERIFYING_RECOVERY → ANALYZING → COMPLETED`, with honest exceptional outcomes. API routes are registered by Sachin under `/api/v1`; provide port behavior rather than editing their main router.

## Acceptance tests and handoff

Test wrong cluster identity, wrong namespace, unknown target, replaced resource UID, excessive parameters, expired/tampered approval, second concurrent run, double start, STOP latch, missing metrics, killed UI/AI/API/worker, interrupted injection, double cleanup, startup reconciliation, changed target fields and failed restoration. Show that watchdog actions do not depend on an LLM key.

Perform a real own-cluster threshold stop, restore configuration and verify business recovery. Day 2 runs cover each fault path and the SQL token/cap/cancel protections. For rollback, test absent opt-in, expiry, soft trigger persistence, external field change and failed reversion. Whole-host/cluster outages can prevent immediate cleanup; record that limit and validate reconciliation once reachable.

Merge small PRs: catalog/validation, watchdog/cleanup, first fault, additional adapters, SQL runtime and finally rollback. Provide executed test results, fault event schema, RBAC requirements, safety runbook, cleanup/recovery evidence, known limits and active-resource status. Your workstream is done when the integration owner can run and stop every supported action without the model or dashboard being available, and failures are never reported as successful restoration.
