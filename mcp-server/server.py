"""
Master MCP Server for Insurance Enterprise Governance.
Provides controlled tools for decentralized agents with built-in guardrails,
authority limits, PII protection, and ACPR/DORA audit trail.
"""
from mcp.server.mcpserver import MCPServer
from registry import global_registry
from guardrails import GuardrailsEngine
from audit_store import global_audit
from typing import Dict, Any
import datetime

# Initialisation du Serveur MCP Maître
mcp_server = MCPServer(
    name="insurance-master-control-plane",
    version="1.0.0",
    description="Serveur MCP Régalien d'Entreprise : Gouvernance, Autorisations et Audit d'Assurance"
)

# Base de données simulée des contrats d'assurance (Enterprise Truth Core)
MOCK_CONTRACTS = {
    "POL-AUTO-8821": {
        "policy_id": "POL-AUTO-8821",
        "holder_name": "Jean Dupont",
        "holder_iban": "FR7630006000011234567890189",
        "vehicle": "Peugeot 208 (AA-123-BB)",
        "coverage": ["Responsabilité Civile", "Tous Risques", "Bris de Glace Sans Franchise", "Vol/Incendie"],
        "glass_breakage_deductible_eur": 0.0,
        "general_deductible_eur": 250.0,
        "status": "ACTIVE_PAID"
    },
    "POL-MRH-4412": {
        "policy_id": "POL-MRH-4412",
        "holder_name": "Claire Martin",
        "holder_iban": "FR7610055000019876543210145",
        "residence": "Appartement 75m2, Lyon 3e",
        "coverage": ["Dégât des Eaux", "Incendie", "Responsabilité Civile Vie Privée"],
        "water_damage_deductible_eur": 150.0,
        "status": "ACTIVE_PAID"
    }
}

@mcp_server.tool()
def consult_policy_contract(agent_id: str, policy_id: str) -> Dict[str, Any]:
    """
    Consulte un contrat d'assurance certifié avec masquage RGPD automatique.
    Vérifie l'accréditation de l'agent dans le registre d'entreprise.
    """
    agent = global_registry.get_agent(agent_id)
    if not agent:
        return {"status": "ERROR", "message": f"Agent non reconnu ou non immatriculé : '{agent_id}'."}

    if agent.kill_switch or agent.status != "ACTIVE":
        return {"status": "BLOCKED", "message": f"Accès révoqué pour {agent_id} (Kill-Switch actif)."}

    contract = MOCK_CONTRACTS.get(policy_id)
    if not contract:
        return {"status": "NOT_FOUND", "message": f"Contrat '{policy_id}' introuvable dans le référentiel d'entreprise."}

    # Protection des données personnelles (RGPD)
    sanitized = dict(contract)
    sanitized["holder_iban"] = GuardrailsEngine.scrub_pii(sanitized.get("holder_iban", ""))

    global_audit.log(
        agent_id=agent_id,
        direction=agent.direction,
        tool_name="consult_policy_contract",
        decision="APPROVED",
        details=f"Consultation légitime du contrat {policy_id}",
        params={"policy_id": policy_id}
    )

    return {
        "status": "SUCCESS",
        "contract": sanitized,
        "governance_note": "Données bancaires masquées conformément à la directive RGPD."
    }

@mcp_server.tool()
def settle_claim_payment(agent_id: str, claim_id: str, policy_id: str, amount_eur: float, reason: str, invoice_ref: str) -> Dict[str, Any]:
    """
    Exécute ou soumet le règlement d'une indemnité de sinistre.
    Applique la matrice déterministe de délégation de pouvoir et les gardes-fous d'assurance.
    """
    agent = global_registry.get_agent(agent_id)
    if not agent:
        return {"status": "REJECTED", "message": f"Agent inconnu '{agent_id}'. Opération financière refusée."}

    params = {
        "claim_id": claim_id,
        "policy_id": policy_id,
        "amount_eur": amount_eur,
        "reason": reason,
        "invoice_ref": invoice_ref
    }

    # Évaluation des règles de gouvernance
    authorized, decision_type, justification = GuardrailsEngine.check_agent_authority(
        agent=agent,
        action="claim_settlement",
        params=params
    )

    audit_id = global_audit.log(
        agent_id=agent_id,
        direction=agent.direction,
        tool_name="settle_claim_payment",
        decision=decision_type,
        details=justification,
        params=params
    )

    # Scénario A : Règlement approuvé dans les limites du pouvoir autonome
    if authorized:
        settlement_ref = f"REG-{datetime.date.today().strftime('%Y%m%d')}-{claim_id[-4:]}"
        return {
            "status": "APPROVED",
            "decision": "PAID_AUTONOMOUSLY",
            "settlement_ref": settlement_ref,
            "claim_id": claim_id,
            "amount_paid_eur": amount_eur,
            "audit_trail_id": audit_id,
            "message": f"Virement de {amount_eur:,.2f} € ordonnancé au réparateur (Plafond L2 respecté)."
        }

    # Scénario B : Dépassement de plafond -> Escalade Humaine Automatique (HITL)
    if decision_type == "ESCALATED_HITL":
        escalation_ticket = f"HITL-TASK-{claim_id[-4:]}"
        return {
            "status": "ESCALATED_TO_HUMAN",
            "decision": "HITL_TRIGGERED",
            "escalation_ticket_id": escalation_ticket,
            "claim_id": claim_id,
            "amount_eur": amount_eur,
            "assigned_queue": "SUPERVISEUR_SINISTRES_AUTO",
            "audit_trail_id": audit_id,
            "message": justification
        }

    # Scénario C : Blocage pour violation de sécurité ou de politique d'entreprise
    return {
        "status": "BLOCKED_BY_POLICY",
        "decision": decision_type,
        "audit_trail_id": audit_id,
        "message": justification
    }

@mcp_server.tool()
def refuse_claim_guarantee(agent_id: str, claim_id: str, policy_id: str, legal_reason: str) -> Dict[str, Any]:
    """
    Tente de notifier un refus formel de garantie sur un sinistre.
    Interception obligatoire : Les refus automatisés sont strictement interdits par le code de déontologie.
    """
    agent = global_registry.get_agent(agent_id)
    if not agent:
        return {"status": "REJECTED", "message": f"Agent non reconnu : '{agent_id}'."}

    params = {"claim_id": claim_id, "policy_id": policy_id, "legal_reason": legal_reason}
    authorized, decision_type, justification = GuardrailsEngine.check_agent_authority(
        agent=agent,
        action="claim_refusal",
        params=params
    )

    audit_id = global_audit.log(
        agent_id=agent_id,
        direction=agent.direction,
        tool_name="refuse_claim_guarantee",
        decision=decision_type,
        details=justification,
        params=params
    )

    return {
        "status": "INTERCEPTED_AND_REDIRECTED",
        "decision": "BLOCKED_POLICY",
        "audit_trail_id": audit_id,
        "mandatory_action": "Dossier transféré au Service Contentieux & Juridique pour instruction humaine.",
        "legal_notice": justification
    }

@mcp_server.tool()
def audit_compliance_report(admin_token: str, limit: int = 10) -> Dict[str, Any]:
    """
    Outil d'audit pour la Direction Générale et le contrôle périodique / ACPR.
    Fournit les statistiques temps réel de conformité et les dernières décisions tracées.
    """
    if admin_token != "ACPR-AUDIT-SECRET-KEY-2026":
        return {"status": "UNAUTHORIZED", "message": "Jeton d'audit non valide."}

    stats = global_audit.get_stats()
    records = global_audit.list_records(limit=limit)
    return {
        "status": "SUCCESS",
        "compliance_summary": stats,
        "recent_audit_trail": records,
        "registered_agents_count": len(global_registry.list_all())
    }

@mcp_server.tool()
def admin_toggle_kill_switch(admin_token: str, target_agent_id: str, suspend: bool, reason: str) -> Dict[str, Any]:
    """
    Arrêt d'urgence DORA (Kill Switch) : Révoque ou rétablit instantanément les droits d'un agent.
    """
    if admin_token != "ACPR-AUDIT-SECRET-KEY-2026":
        return {"status": "UNAUTHORIZED", "message": "Action d'urgence réservée aux administrateurs de conformité."}

    success = global_registry.set_kill_switch(target_agent_id, suspend)
    if not success:
        return {"status": "NOT_FOUND", "message": f"Agent '{target_agent_id}' introuvable."}

    action_str = "SUSPENDU (Kill Switch ACTIF)" if suspend else "RÉTABLI (Kill Switch INACTIF)"
    return {
        "status": "SUCCESS",
        "agent_id": target_agent_id,
        "current_status": action_str,
        "reason": reason
    }
