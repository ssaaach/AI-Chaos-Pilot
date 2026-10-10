"""Regenerate the full prompt pack with the user's immediate demo priority."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
shared="""## Latest user priority — local prevention demo within two hours

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

"""
roles={
 '03_ANANYA_IMPLEMENTATION_PROMPT.md':'Immediate owner task: supply/reproduce the separate loopback demo target; its health response includes status, request count and zero mutation count. Do not claim local HTTP service identity is an enrolled Kubernetes resource.',
 '04_TOOSHITA_IMPLEMENTATION_PROMPT.md':'Immediate owner task: build the injection/preflight guard. Duration 90 exceeds hard cap 60. Rejection happens before any executor invocation; STOP remains latched until verified healthy reset. Provide an execution spy/assertion and unavailable-state test. Later implement actual cluster faults and external watchdog.',
 '05_NAVYA_IMPLEMENTATION_PROMPT.md':'Immediate owner task: independently verify healthy target before/after the rejected attempt and executor invocation count zero. Capture sanitized local evidence, distinguish mock checks from real HTTP observations and do not assign a resilience score to a prevented fault.',
 '06_GAUTAM_IMPLEMENTATION_PROMPT.md':'Immediate owner task: explain the deterministic DURATION_HARD_LIMIT rejection from actual configured/requested duration and health evidence. A blocked attempt has no observed fault duration or crash label and must not update a duration model as a completed execution.',
 '07_SACHIN_IMPLEMENTATION_PROMPT.md':'Immediate owner task: deliver the working local demo API/dashboard, Inject test error button, STOP state, and accessible popup heading Error has occurred with body Injection blocked before execution. Validate with the real separate HTTP target; update all prompts and provide a runnable bundle and truthful testing status.'
}
dest=root/'outputs/revised-prompt-pack';dest.mkdir(parents=True,exist_ok=True)
for path in sorted((root/'prompts').glob('*.md')):
    old=path.read_text(encoding='utf-8')
    marker='<!-- immediate-demo-update -->'
    if marker not in old:
        addition=marker+'\n\n'+shared
        if path.name in roles: addition+='**This person’s immediate task:** '+roles[path.name]+'\n\n'
        old=addition+'---\n\n'+old
        path.write_text(old,encoding='utf-8')
    (dest/path.name).write_text(old,encoding='utf-8')
(root/'CONTEXT.md').write_text((root/'prompts/01_SHARED_PROJECT_CONTEXT.md').read_text(encoding='utf-8'),encoding='utf-8')
(root/'contracts/INTERFACES.md').write_text((root/'prompts/02_SHARED_INTERFACES.md').read_text(encoding='utf-8'),encoding='utf-8')
with zipfile.ZipFile(root/'outputs/Bosch_Resilience_AI_Updated_Prompt_Pack.zip','w',zipfile.ZIP_DEFLATED) as z:
    for path in dest.glob('*.md'): z.write(path,path.name)
