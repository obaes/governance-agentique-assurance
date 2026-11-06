"""
Master Agentic Governance Registry for Insurance.
Maintains agent identities, passports, autonomy levels, and authority limits.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional, List
from enum import Enum
import datetime

class AutonomyLevel(str, Enum):
    L1_COPILOT = "L1"        # Humain valide 100%
    L2_DELEGATED = "L2"      # Délégué sous plafond
    L3_AUTONOMOUS = "L3"    # Autonome sous liste blanche stricte

@dataclass
class AgentPassport:
    agent_id: str
    name: str
    direction: str
    business_owner: str
    autonomy_level: AutonomyLevel
    max_settlement_eur: float
    max_commercial_discount_pct: float
    health_data_authorized: bool
    status: str = "ACTIVE"   # ACTIVE, SUSPENDED, DECOMMISSIONED
    kill_switch: bool = False
    registered_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, AgentPassport] = {}
        self._seed_default_agents()

    def _seed_default_agents(self):
        # 1. Agent Sinistres Auto (L2 plafonné à 800 €)
        self.register(AgentPassport(
            agent_id="AGT-SIN-001",
            name="ClaimAssist-Auto-QuickSettlement",
            direction="Gestion & Sinistres",
            business_owner="martine.dubois@assurance.fr",
            autonomy_level=AutonomyLevel.L2_DELEGATED,
            max_settlement_eur=800.00,
            max_commercial_discount_pct=0.0,
            health_data_authorized=False,
            status="ACTIVE"
        ))

        # 2. Agent Réseau / Courtage (L1 assistif)
        self.register(AgentPassport(
            agent_id="AGT-DIS-002",
            name="CourtierCopilot-Pro",
            direction="Distribution & Réseau",
            business_owner="sylvain.laurent@assurance.fr",
            autonomy_level=AutonomyLevel.L1_COPILOT,
            max_settlement_eur=0.00,
            max_commercial_discount_pct=5.0,
            health_data_authorized=False,
            status="ACTIVE"
        ))

        # 3. Agent Actuariat (L3 surveillance en lecture seule)
        self.register(AgentPassport(
            agent_id="AGT-ACT-003",
            name="ActuaDrift-Sentinel",
            direction="Actuariat & Data",
            business_owner="claire.moreau@assurance.fr",
            autonomy_level=AutonomyLevel.L3_AUTONOMOUS,
            max_settlement_eur=0.00,
            max_commercial_discount_pct=0.0,
            health_data_authorized=False,
            status="ACTIVE"
        ))

    def register(self, passport: AgentPassport):
        self._agents[passport.agent_id] = passport

    def get_agent(self, agent_id: str) -> Optional[AgentPassport]:
        return self._agents.get(agent_id)

    def set_kill_switch(self, agent_id: str, state: bool) -> bool:
        agent = self.get_agent(agent_id)
        if agent:
            agent.kill_switch = state
            agent.status = "SUSPENDED" if state else "ACTIVE"
            return True
        return False

    def list_all(self) -> List[AgentPassport]:
        return list(self._agents.values())

# Global registry instance
global_registry = AgentRegistry()
