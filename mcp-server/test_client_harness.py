"""
Client Test Harness for Master MCP Insurance Governance Server.
Simulates autonomous agents from different directions interacting with the Master Control Plane.
"""
import asyncio
import json
from server import mcp_server

def print_section(title: str):
    print("\n" + "=" * 75)
    print(f"👉 {title}")
    print("=" * 75)

async def run_scenario(name: str, tool_name: str, arguments: dict):
    print(f"\n[SCÉNARIO] {name}")
    print(f"  Outil appelé : {tool_name}")
    print(f"  Paramètres   : {json.dumps(arguments, ensure_ascii=False, indent=2)}")
    
    result = await mcp_server.call_tool(tool_name, arguments)
    
    # Extraire le contenu structuré
    res_data = result.structured_content.get("result", {}) if result.structured_content else {}
    print(f"  --- RÉSULTAT DU CONTRÔLE MAÎTRE ---")
    print(f"  Statut   : {res_data.get('status')}")
    print(f"  Décision : {res_data.get('decision', 'N/A')}")
    if "audit_trail_id" in res_data:
        print(f"  Audit ID : {res_data.get('audit_trail_id')}")
    print(f"  Détail   : {res_data.get('message') or res_data.get('legal_notice') or res_data.get('governance_note')}")
    return res_data

async def main():
    print_section("TEST 1 : Consultation Contrat & Masquage RGPD (Direction Sinistres)")
    await run_scenario(
        name="Consultation légitime de contrat auto",
        tool_name="consult_policy_contract",
        arguments={"agent_id": "AGT-SIN-001", "policy_id": "POL-AUTO-8821"}
    )

    print_section("TEST 2 : Règlement Direct sous Seuil (450 € < 800 €) -> AUTONOME (L2)")
    await run_scenario(
        name="Remplacement pare-brise garage agréé",
        tool_name="settle_claim_payment",
        arguments={
            "agent_id": "AGT-SIN-001",
            "claim_id": "SIN-2026-901",
            "policy_id": "POL-AUTO-8821",
            "amount_eur": 450.00,
            "reason": "Remplacement pare-brise suite impact gravillon",
            "invoice_ref": "FAC-CARGLASS-7781"
        }
    )

    print_section("TEST 3 : Dépassement Seuil Financier (2 400 € > 800 €) -> ESCALADE HITL")
    await run_scenario(
        name="Réparation carrosserie choc important",
        tool_name="settle_claim_payment",
        arguments={
            "agent_id": "AGT-SIN-001",
            "claim_id": "SIN-2026-902",
            "policy_id": "POL-AUTO-8821",
            "amount_eur": 2400.00,
            "reason": "Peinture et aile avant suite choc parking",
            "invoice_ref": "FAC-GARAGE-9912"
        }
    )

    print_section("TEST 4 : Tentative de Refus de Garantie -> INTERCEPTION INVARIANT JURIDIQUE")
    await run_scenario(
        name="Refus de prise en charge pour exclusion contractuelle",
        tool_name="refuse_claim_guarantee",
        arguments={
            "agent_id": "AGT-SIN-001",
            "claim_id": "SIN-2026-903",
            "policy_id": "POL-AUTO-8821",
            "legal_reason": "Sinistre survenu sur circuit automobile non couvert"
        }
    )

    print_section("TEST 5 : Détection Données de Santé Non Autorisées -> BLOCAGE RGPD")
    await run_scenario(
        name="Sinistre corporel injecté dans un agent matériel",
        tool_name="settle_claim_payment",
        arguments={
            "agent_id": "AGT-SIN-001",
            "claim_id": "SIN-2026-904",
            "policy_id": "POL-AUTO-8821",
            "amount_eur": 350.00,
            "reason": "Prise en charge soins d'ostéopathie suite à traumatisme cervical",
            "invoice_ref": "FAC-MEDECIN-3321"
        }
    )

    print_section("TEST 6 : Activation du Kill Switch d'Urgence DORA & Blocage Immédiat")
    # Activer le Kill Switch
    await run_scenario(
        name="Activation de l'arrêt d'urgence par le RSSI / Conformité",
        tool_name="admin_toggle_kill_switch",
        arguments={
            "admin_token": "ACPR-AUDIT-SECRET-KEY-2026",
            "target_agent_id": "AGT-SIN-001",
            "suspend": True,
            "reason": "Suspicion d'anomalie comportementale détectée par la passerelle"
        }
    )
    # Tenter un appel après suspension
    await run_scenario(
        name="Appel bloqué par le Kill Switch",
        tool_name="consult_policy_contract",
        arguments={"agent_id": "AGT-SIN-001", "policy_id": "POL-AUTO-8821"}
    )
    # Rétablir l'agent
    await run_scenario(
        name="Rétablissement après vérification de sécurité",
        tool_name="admin_toggle_kill_switch",
        arguments={
            "admin_token": "ACPR-AUDIT-SECRET-KEY-2026",
            "target_agent_id": "AGT-SIN-001",
            "suspend": False,
            "reason": "Vérification terminée, faux positif écarté"
        }
    )

    print_section("TEST 7 : Rapport d'Audit & Conformité ACPR / Direction Générale")
    audit_res = await run_scenario(
        name="Extraction de l'Audit Trail pour l'ACPR",
        tool_name="audit_compliance_report",
        arguments={"admin_token": "ACPR-AUDIT-SECRET-KEY-2026", "limit": 5}
    )
    print("\n[BILAN DE CONFORMITÉ EN TEMPS RÉEL] :")
    print(json.dumps(audit_res.get("compliance_summary", {}), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
