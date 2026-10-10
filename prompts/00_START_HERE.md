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

---

# Bosch Resilience AI team prompt pack

This pack gives Ananya, Tooshita, Navya, Gautam and Sachin five independently testable implementation workstreams for one Kubernetes resilience platform. It combines the five supplied proposals, the event slides and the new requirement for learning from requests and current system state without retaining a raw training dataset.

The recommended solution has two connected paths: controlled chaos experiments on Google Online Boutique, and a guarded SQL console for a separate synthetic PostgreSQL lab. Both feed a streaming learner and evidence based explanations. Deterministic policy controls execution. Adaptive rollback is Day 2 work; a working safety stop and fault cleanup remain Day 1 requirements.

## Give each person their prompt

| Person | Prompt | Primary responsibility | Branch |
|---|---|---|---|
| Ananya | [Ananya implementation prompt](03_ANANYA_IMPLEMENTATION_PROMPT.md) | Kubernetes, sample application, lab deployment and topology | `feat/ananya-platform` |
| Tooshita | [Tooshita implementation prompt](04_TOOSHITA_IMPLEMENTATION_PROMPT.md) | Chaos execution, watchdog, STOP, bounded SQL runtime and Day 2 rollback | `feat/tooshita-runtime` |
| Navya | [Navya implementation prompt](05_NAVYA_IMPLEMENTATION_PROMPT.md) | Workload, live state, safe plan estimates, evidence and scoring | `feat/navya-telemetry` |
| Gautam | [Gautam implementation prompt](06_GAUTAM_IMPLEMENTATION_PROMPT.md) | SQL guard, AI reasoning, streaming learning and adaptive proposals | `feat/gautam-intelligence` |
| Sachin | [Sachin implementation prompt](07_SACHIN_IMPLEMENTATION_PROMPT.md) | FastAPI composition, shared contracts, dashboard, integration and submission | `feat/sachin-integration` |

The assignments follow the supplied name order; they do not assume particular skills. These are five ownership areas, not a promise of precisely equal engineering hours. Sachin coordinates integration, while each person supplies their own tests, documentation and report contributions.

Each person should clone the same repository, open their own branch, and paste the full text of their prompt into their local coding assistant. Copy [the shared context](01_SHARED_PROJECT_CONTEXT.md) to `CONTEXT.md`, [the interface contract](02_SHARED_INTERFACES.md) to `contracts/INTERFACES.md`, and [the Day 2 rollback specification](08_DAY_2_ROLLBACK_SPECIFICATION.md) to `docs/rollback-specification.md`. Keep the personal prompts in `prompts/`. Each personal prompt also includes enough project context to start independently.

## Start together for the first 30 minutes

1. Sachin creates one public GitHub monorepo named `bosch-resilience-ai`, with Apache-2.0 for team code, preserved upstream notices, protected `main`, and one reviewer per pull request. Use the team's actual GitHub account or organization; no account or remote URL is assumed here.
2. Commit this shared context, interface specification and personal prompts. Sachin implements the first shared models and fixtures with the other four reviewing fields for their area.
3. Ananya selects and pins the upstream application commit and a tested tool/image set. Record actual versions rather than using an unverified list of latest versions.
4. Everyone checks their machine. Use a local kind cluster for live tests when their machine supports it. UI, intelligence and unit tests can begin with fixtures without a full cluster. Choose Sachin's laptop as the default demo machine, subject to the resource check; Ananya is the deployment backup.
5. Merge small foundations early. Integrate once during Day 1 before polishing individual modules. Keep a real end to end path working on `main`.

No repository, Kubernetes cluster or application has been created by this prompt pack. It is a specification for implementation, with proposed acceptance criteria rather than claimed results.

## What ships on each day

| Day | Required working result |
|---|---|
| Day 1 | Healthy Online Boutique, verified dependency map, steady workload and measured baseline, one reversible service outage, automatic stop and verified cleanup, manual STOP, checkpoint demo. In parallel: lightweight SQL analysis, streaming statistics, and UI with fixtures clearly labelled. |
| Day 2 | Three distinct fault classes measured: pod termination, Redis connection interruption and network latency. AI ranks experiments and findings. Guarded safe SQL execution and incremental prediction are integrated. Add one narrowly scoped adaptive rollback demonstration after the core works. Freeze features and finish the five submission deliverables. |

The SQL lab and adaptive rollback strengthen the project, but they must not displace the official chaos deliverables. Start with 10,000 synthetic lab rows; scale toward one million only on a machine that has capacity. Always show the actual row count.

## Understand the learning claim

The system learns from observations by updating bounded statistics and small model weights. It discards raw SQL, parameters, query results and per-request training examples after processing. Derived learning state stays in RAM and resets on restart by default. Short lived request buffers and minimal operational undo records are necessary for correlation and safe cleanup; they are not a retained training corpus.

Avoid claiming zero stored information: a learner needs state to remember anything. Avoid claiming that deleting a Python object securely erases every memory copy. The implementation promise is bounded retention and no durable raw request dataset, verified across application logs, database logs and browser storage.

## Five final deliverables

1. Public source repository and a reproducible README.
2. Demo video of three minutes or less showing injection, observed impact and findings.
3. One page or slide showing architecture, AI decisions and safety controls.
4. Findings report with measured evidence, ranked weaknesses and recommended fixes.
5. Team form listing all five names, actual tools/models, libraries and data sources.

The supplied slides call Day 1 milestones guidance checkpoints. They show automatic stop or rollback on a threshold breach as a Day 1 safety checkpoint. They show three or more failure types for Day 2; this pack targets three distinct mechanisms. Aim to submit 30 minutes before the actual event deadline, without assuming a deadline from the older drafts.
