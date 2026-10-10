"""Local prevention demo, isolated from team-owned Kubernetes implementation."""
from datetime import datetime, timedelta, timezone
import time
from uuid import uuid4
import httpx
from app.contracts import *
from app.api.ports import Ports
from app.api.errors import PortError

def now(): return datetime.now(timezone.utc)

class DemoInjectionRequest(Contract):
    fault_type: Literal["service_pause"]
    duration_seconds: Annotated[int, Field(ge=1, le=600)]

class DemoInjectionResult(Observed):
    request_id: str
    captured_at: AwareDatetime
    decision: Literal["BLOCK"]
    message: str
    reason: str
    rule_id: str
    stop_latched: Literal[True] = True
    executed: Literal[False] = False
    target_status: Literal["healthy", "unavailable"]
    target_requests: Count
    mutations_dispatched: Literal[0] = 0
    duration_seconds: Count
    maximum_seconds: Literal[60] = 60

class DemoAdapter:
    def __init__(self, settings):
        self.settings = settings
        self.started = now()
        self.latched = False
        self.last_result = None
        self.probes = 0
        self.failed = 0
        # Fixed loopback destination; never accept a user-supplied URL.
        self.target_url = "http://127.0.0.1:8090/health"
    async def probe(self):
        self.probes += 1
        try:
            async with httpx.AsyncClient(timeout=1, trust_env=False) as client:
                r = await client.get(self.target_url)
                r.raise_for_status()
                data = r.json()
                if data.get("status") != "healthy" or data.get("mutations_received") != 0:
                    raise ValueError("Target health mismatch")
                return {"status":"healthy", "requests":int(data["requests"])}
        except (httpx.HTTPError, ValueError, KeyError):
            self.failed += 1
            return {"status":"unavailable", "requests":0}
    async def get_state(self, sandbox_id):
        p = await self.probe()
        return SystemStateSnapshot(source="live", state_id=str(uuid4()),captured_at=now(),valid_until=now()+timedelta(seconds=5),sandbox_id="local-demo",ready_by_workload={"demo-target":Readiness(ready=1 if p["status"]=="healthy" else 0,desired=1)},request_rate=None,error_rate=self.failed/self.probes,p95_ms=None,db_connections_used=None,db_connections_limit=None,missing_features=["request_rate: rate collector not connected","p95_ms: percentile collector not connected","db_connections_used: no SQL lab","db_connections_limit: no SQL lab","cpu_utilization: no collector","memory_utilization: no collector"],active_fault_id=None)
    async def get_topology(self,sandbox_id):
        return TopologySnapshot(source="live",graph_id="local-demo-graph",upstream_sha=None,generated_at=now(),sandbox_id="local-demo",namespace="local-http",nodes=[TopologyNode(target_id=n,name=n,kind="Service",uid="local-"+n,selector={},ports=[p],desired_replicas=1,stateful=False,confidence=1) for n,p in [("guard-api",8000),("demo-target",8090)]],edges=[TopologyEdge(caller="guard-api",dependency="demo-target",protocol="HTTP",provenance="configured fixed loopback health route",confidence=1)],manual_corrections=["Local service identities; no Kubernetes discovery or UIDs"])
    async def get_learning_status(self):
        return LearningStatus(source="live",learner_version="not-integrated",started_at=self.started,processed=0,updates=0,pending_count=0,dropped_events=0,drift_status="cold_start",prediction_error=None,queue_limit=256,pending_limit=128,metric_buffer_seconds=120,intent_ttl_seconds=60,model_limit_bytes=0)
    async def catalog(self): return Catalog(source="live",entries=[])
    async def inject_attempt(self, body, actor):
        p = await self.probe()
        if self.latched:
            rule,reason="STOP_LATCHED","STOP is already latched. Reset after confirming target health."
        elif p["status"] != "healthy":
            rule,reason="TARGET_UNAVAILABLE","Required target health is unavailable. Execution was stopped before dispatch."
        elif body.duration_seconds>60:
            rule,reason="DURATION_HARD_LIMIT",f"Requested outage is {body.duration_seconds} seconds, exceeding the fixed 60-second maximum. Execution was stopped before dispatch."
        else:
            rule,reason="DEMO_EXECUTION_DISABLED","This prevention demo permits no service mutations. Execution was stopped before dispatch."
        # No target mutation client exists in this adapter: the guard cannot dispatch.
        self.latched=True
        result=DemoInjectionResult(source="live",request_id=str(uuid4()),captured_at=now(),decision="BLOCK",message="Error has occurred — injection blocked before execution.",reason=reason,rule_id=rule,target_status=p["status"],target_requests=p["requests"],duration_seconds=body.duration_seconds)
        self.last_result=result
        return result
    async def emergency_stop(self,sandbox_id,actor):
        self.latched=True
        return StopReceipt(source="live",request_id=str(uuid4()),accepted_at=now(),stop_latched=True,affected_run_ids=[],cleanup_status="not_applicable")
    async def reconcile(self,sandbox_id):
        p=await self.probe()
        return CleanupSummary(source="live",sandbox_id=sandbox_id,cleanup_status="not_applicable",recovery_status="verified" if p["status"]=="healthy" else "unknown",unresolved_run_ids=[])
    async def reset(self,sandbox_id,actor):
        result=await self.reconcile(sandbox_id)
        if result.recovery_status!="verified": raise PortError("CONFLICT")
        self.latched=False
        self.last_result=None
        return result
    async def analyze_query(self,transient_request,state,estimator):
        return QueryDecision(source="live",decision_id=str(uuid4()),request_id=str(uuid4()),decision="BLOCK",rule_ids=["MODULE_NOT_INTEGRATED"],policy_version="demo-only",state_id=state.state_id,plan_estimate=None,prediction=None,reasons=["SQL policy and estimator are not integrated in the local demo."],recommendations=["Connect team ports before enabling SQL execution."])
    async def status(self,run_id): raise PortError("NOT_FOUND",404)
    async def events(self,run_id,after_sequence): raise PortError("NOT_FOUND",404)

def demo_ports(settings):
    a=DemoAdapter(settings)
    return Ports(a,a,a,a)
