"""
Démonstration Live : Cycle de vie complet d'un sinistre via l'Agent Métier et le Serveur MCP Maître.
"""
import asyncio
import json
import time
from server import mcp_server

# Couleurs ANSI pour une lisibilité parfaite dans la console
C_BLUE = "\033[94m"
C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

def banner(title: str):
    print("\n" + "=" * 80)
    print(f"{C_BOLD}{C_CYAN}🛡️  {title}{C_RESET}")
    print("=" * 80)

async def simulate_agent_turn(case_num: int, title: str, client_msg: str, agent_id: str, claim_details: dict):
    banner(f"CAS {case_num} : {title}")
    
    print(f"\n{C_BOLD}👤 L'ASSURÉ DIT :{C_RESET}")
    print(f'   "{C_YELLOW}{client_msg}{C_RESET}"')
    time.sleep(0.5)

    print(f"\n{C_BOLD}🤖 AGENT MÉTIER ({agent_id}) - ANALYSE DU SKILL SINISTRES :{C_RESET}")
    print(f"   [1] Identification du contrat : {claim_details['policy_id']}")
    print(f"   [2] Appel de la Passerelle MCP Maître pour vérification des garanties...")
    
    # Étape 1 : Consultation Contrat via MCP
    contract_res = await mcp_server.call_tool("consult_policy_contract", {
        "agent_id": agent_id,
        "policy_id": claim_details["policy_id"]
    })
    c_data = contract_res.structured_content.get("result", {})
    
    print(f"       ↳ {C_GREEN}✓ Contrat certifié récupéré{C_RESET} | Titulaire: {c_data['contract']['holder_name']} | IBAN: {c_data['contract']['holder_iban']}")
    print(f"       ↳ {C_BLUE}Garanties actives :{C_RESET} {', '.join(c_data['contract']['coverage'])}")
    time.sleep(0.5)

    # Étape 2 : L'agent tente le règlement
    amount = claim_details["amount_eur"]
    print(f"\n{C_BOLD}🤖 AGENT MÉTIER - TENTATIVE D'ACTION FINANCIÈRE :{C_RESET}")
    print(f"   Montant réclamé : {amount:,.2f} € | Motif : {claim_details['reason']}")
    print(f"   Appel de l'outil MCP régalien : {C_CYAN}settle_claim_payment(){C_RESET}...")
    time.sleep(0.5)

    settle_res = await mcp_server.call_tool("settle_claim_payment", {
        "agent_id": agent_id,
        "claim_id": claim_details["claim_id"],
        "policy_id": claim_details["policy_id"],
        "amount_eur": amount,
        "reason": claim_details["reason"],
        "invoice_ref": claim_details["invoice_ref"]
    })
    s_data = settle_res.structured_content.get("result", {})

    # Étape 3 : Réponse du Control Plane
    print(f"\n{C_BOLD}🛡️  VERDICT DE LA STRUCTURE MAÎTRE (CONTROL PLANE) :{C_RESET}")
    status = s_data.get("status")
    
    if status == "APPROVED":
        print(f"   Statut   : {C_GREEN}{C_BOLD}AUTORISÉ (Plafond L2 respecté){C_RESET}")
        print(f"   Virement : Réf {s_data.get('settlement_ref')} ordonnancé au réparateur")
        print(f"   Audit ID : {s_data.get('audit_trail_id')}")
        print(f"\n{C_BOLD}🤖 RÉPONSE FINALE DE L'AGENT AU CLIENT :{C_RESET}")
        print(f'   "{C_GREEN}Bonjour M. Dupont. Votre facture de {amount:,.2f} € pour le bris de glace a été validée immédiatement. Le virement de règlement est en cours (Réf : {s_data.get("settlement_ref")}). Vous n\'avez rien à débourser !{C_RESET}"')

    elif status == "ESCALATED_TO_HUMAN":
        print(f"   Statut   : {C_YELLOW}{C_BOLD}INTERCEPTÉ - ESCALADE HUMAINE OBLIGATOIRE (HITL){C_RESET}")
        print(f"   Motif    : {s_data.get('message')}")
        print(f"   Ticket   : {s_data.get('escalation_ticket_id')} -> Assigné à la file '{s_data.get('assigned_queue')}'")
        print(f"   Audit ID : {s_data.get('audit_trail_id')}")
        print(f"\n{C_BOLD}🤖 RÉPONSE FINALE DE L'AGENT AU CLIENT :{C_RESET}")
        print(f'   "{C_YELLOW}Bonjour Mme Martin. J\'ai bien pris en charge votre déclaration de dégât des eaux pour {amount:,.2f} €. Compte tenu du montant important, votre dossier a été transmis pour validation prioritaire à notre gestionnaire senior (Dossier {s_data.get("escalation_ticket_id")}). Il vous contactera sous 24h.{C_RESET}"')

    else:
        print(f"   Statut   : {C_RED}{C_BOLD}BLOQUÉ PAR POLITIQUE DE SÉCURITÉ{C_RESET}")
        print(f"   Motif    : {s_data.get('message')}")
        print(f"   Audit ID : {s_data.get('audit_trail_id')}")
        print(f"\n{C_BOLD}🤖 RÉPONSE FINALE DE L'AGENT AU CLIENT :{C_RESET}")
        print(f'   "{C_RED}Nous ne pouvons pas donner suite à cette demande par voie automatisée. Votre demande nécessite un accompagnement spécialisé.{C_RESET}"')

async def main():
    print(f"\n{C_BOLD}{C_BLUE}================================================================================")
    print("   LANCEMENT DU SCÉNARIO D'EXEMPLE : COUPLAGE AGENT MÉTIER & SERVEUR MCP MAÎTRE")
    print(f"================================================================================{C_RESET}")

    # SCÉNARIO 1 : Bris de glace classique (450 €) -> Autorisé directement en autonomie L2
    await simulate_agent_turn(
        case_num=1,
        title="Sinistre Auto Bris de Glace (450 €) - Traitement 100% Autonome",
        client_msg="Bonjour, j'ai fait remplacer mon pare-brise suite à un éclat de gravillon sur l'A6. La facture Carglass s'élève à 450 €. Mon contrat est le POL-AUTO-8821.",
        agent_id="AGT-SIN-001",
        claim_details={
            "claim_id": "SIN-2026-0811",
            "policy_id": "POL-AUTO-8821",
            "amount_eur": 450.00,
            "reason": "Remplacement pare-brise Carglass",
            "invoice_ref": "FAC-CG-9921"
        }
    )

    # SCÉNARIO 2 : Dégât des eaux important (1 850 €) -> Interception & Escalade Humaine HITL
    await simulate_agent_turn(
        case_num=2,
        title="Sinistre Dégât des Eaux Important (1 850 €) - Dépassement Seuil & Escalade",
        client_msg="Bonjour, j'ai subi une fuite importante dans ma cuisine. Le devis des artisans est de 1 850 € sur mon contrat POL-MRH-4412. Pouvez-vous régler ?",
        agent_id="AGT-SIN-001",
        claim_details={
            "claim_id": "SIN-2026-0812",
            "policy_id": "POL-MRH-4412",
            "amount_eur": 1850.00,
            "reason": "Réfection plafond et parquet cuisine fuite canalisation",
            "invoice_ref": "FAC-PLOMB-4410"
        }
    )

    # SCÉNARIO 3 : Synthèse de l'Audit ACPR
    banner("EXTRACTION DU REGISTRE D'AUDIT POUR L'ACPR")
    audit_report = await mcp_server.call_tool("audit_compliance_report", {
        "admin_token": "ACPR-AUDIT-SECRET-KEY-2026",
        "limit": 2
    })
    res = audit_report.structured_content.get("result", {})
    print(f"{C_BOLD}Statistiques consolidées du Control Plane :{C_RESET}")
    print(json.dumps(res.get("compliance_summary", {}), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
