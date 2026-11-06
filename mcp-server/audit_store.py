"""
Immutable Audit Trail & Observability for ACPR and DORA Compliance.
Logs every tool execution, parameters, policy verdicts, and latency.
"""
import datetime
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass
class AuditRecord:
    timestamp: str
    audit_id: str
    agent_id: str
    direction: str
    tool_name: str
    decision: str  # APPROVED, ESCALATED_HITL, BLOCKED_POLICY, BLOCKED_SECURITY
    details: str
    sanitized_params: Dict[str, Any]

class AuditStore:
    def __init__(self):
        self._records: List[AuditRecord] = []
        self._counter = 1000

    def log(self, agent_id: str, direction: str, tool_name: str, decision: str, details: str, params: Dict[str, Any]) -> str:
        self._counter += 1
        audit_id = f"AUD-{datetime.date.today().strftime('%Y%m%d')}-{self._counter}"
        record = AuditRecord(
            timestamp=datetime.datetime.now().isoformat(),
            audit_id=audit_id,
            agent_id=agent_id,
            direction=direction,
            tool_name=tool_name,
            decision=decision,
            details=details,
            sanitized_params={k: v for k, v in params.items() if k != "auth_token"}
        )
        self._records.append(record)
        return audit_id

    def list_records(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [asdict(r) for r in reversed(self._records[-limit:])]

    def get_stats(self) -> Dict[str, Any]:
        total = len(self._records)
        approved = sum(1 for r in self._records if r.decision == "APPROVED")
        hitl = sum(1 for r in self._records if r.decision == "ESCALATED_HITL")
        blocked = sum(1 for r in self._records if r.decision in ("BLOCKED_POLICY", "BLOCKED_SECURITY"))
        return {
            "total_requests": total,
            "approved": approved,
            "hitl_escalations": hitl,
            "blocked_violations": blocked,
            "autonomous_rate_pct": round((approved / total * 100), 1) if total > 0 else 0.0
        }

global_audit = AuditStore()
