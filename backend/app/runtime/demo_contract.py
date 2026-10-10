from typing import Annotated, Literal
from pydantic import AwareDatetime, Field
from app.contracts import Contract, Observed, Count
from .constants import EVIDENCE_LABEL, MAX_FAULT_DURATION_SECONDS, POPUP_BODY, POPUP_HEADING


class DemoInjectionRequest(Contract):
    fault_type: Literal["service_pause"]
    target_id: Literal["demo-target"] = "demo-target"
    duration_seconds: Annotated[int, Field(ge=1, le=600)]


class DemoInjectionResult(Observed):
    request_id: str
    captured_at: AwareDatetime
    decision: Literal["BLOCK"]
    evidence_label: Literal["LOCAL DEMO"] = EVIDENCE_LABEL
    popup_heading: Literal["Error has occurred"] = POPUP_HEADING
    popup_body: Literal["Injection blocked before execution"] = POPUP_BODY
    message: str
    reason: str
    rule_id: str
    stop_latched: Literal[True] = True
    executed: Literal[False] = False
    target_status: Literal["healthy", "unavailable"]
    target_requests: Count
    mutations_dispatched: Literal[0] = 0
    duration_seconds: Count
    maximum_seconds: Literal[60] = MAX_FAULT_DURATION_SECONDS


class DemoSafetyStatus(Observed):
    stop_latched: bool
    last_result: DemoInjectionResult | None
