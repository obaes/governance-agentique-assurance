"""
Policy-as-Code & Privacy Guardrails Engine for Insurance.
Implements RGPD scrubbing, health data blocking, and authority limits.
"""
import re
from typing import Tuple, Dict, Any
from registry import AgentPassport

# Mots-clés caractéristiques de données de santé (Secret médical / CNIL)
HEALTH_KEYWORDS = [
    "médical", "medecin", "docteur", "hôpital", "hospitalisation",
    "traumatisme", "cervical", "entorse", "fracture", "itt", "arrêt de travail",
    "ordonnance", "kinésithérapie", "invalidité", "séquelle", "pathologie"
]

class GuardrailsEngine:
    @staticmethod
    def contains_health_data(text: str) -> Tuple[bool, str]:
        """Détecte les données de santé protégées par le secret médical."""
        lowered = text.lower()
        for kw in HEALTH_KEYWORDS:
            if re.search(r'\b' + re.escape(kw) + r'\b', lowered):
                return True, kw
        return False, ""

    @staticmethod
    def scrub_pii(text: str) -> str:
        """Masque les identifiants hautement sensibles (IBAN, NIR/Secu, Cartes)."""
        # Masquage IBAN
        text = re.sub(r'[A-Z]{2}\d{2}[A-Z0-9]{11,30}', '[IBAN-MASQUÉ-RGPD]', text)
        # Masquage Numéro de Sécurité Sociale (13 ou 15 chiffres)
        text = re.sub(r'\b[12]\d{2}(0[1-9]|1[0-2])\d{8,10}\b', '[NIR-MASQUÉ-RGPD]', text)
        return text

    @staticmethod
    def check_agent_authority(agent: AgentPassport, action: str, params: Dict[str, Any]) -> Tuple[bool, str, str]:
        """
        Vérifie les règles déterministes d'autorité de la compagnie.
        Retourne : (autorisé: bool, type_décision: str, motif: str)
        Types de décision : 'APPROVED', 'ESCALATED_HITL', 'BLOCKED_POLICY', 'BLOCKED_SECURITY'
        """
        # Règle 0 : Vérification Kill-Switch & Statut
        if agent.kill_switch or agent.status != "ACTIVE":
            return False, "BLOCKED_SECURITY", f"L'agent {agent.agent_id} est suspendu (Kill Switch actif ou révoqué)."

        # Règle 1 : Invariant Juridique - Interdiction absolue de refus de garantie par agent
        if action == "claim_refusal":
            return False, "BLOCKED_POLICY", (
                "INVARIANT JURIDIQUE : Aucun refus de garantie ne peut être émis par un agent automatisé. "
                "Obligation légale d'examen et signature par un gestionnaire habilité (Code des Assurances)."
            )

        # Règle 2 : Données de santé
        raw_text = str(params)
        has_health, kw = GuardrailsEngine.contains_health_data(raw_text)
        if has_health and not agent.health_data_authorized:
            return False, "BLOCKED_SECURITY", (
                f"ALERTE RGPD / SECRET MÉDICAL : Détection de données de santé ('{kw}'). "
                f"L'agent {agent.agent_id} n'a pas l'accréditation corporelle requise."
            )

        # Règle 3 : Plafond financier d'indemnisation directe
        if action == "claim_settlement":
            amount = float(params.get("amount_eur", 0.0))
            if amount > agent.max_settlement_eur:
                return False, "ESCALATED_HITL", (
                    f"SEUIL DÉPASSÉ : Le montant demandé ({amount:,.2f} €) excède la délégation "
                    f"autorisée pour {agent.agent_id} ({agent.max_settlement_eur:,.2f} €). "
                    f"Escalade obligatoire vers la corbeille du superviseur humain."
                )

        # Règle 4 : Plafond commercial de remise
        if action == "commercial_discount":
            discount = float(params.get("discount_pct", 0.0))
            if discount > agent.max_commercial_discount_pct:
                return False, "BLOCKED_POLICY", (
                    f"DÉPASSEMENT COMMERCIAL : Remise de {discount}% supérieure au plafond autorisé "
                    f"({agent.max_commercial_discount_pct}%). Requiert accord écrit de l'Inspecteur Commercial."
                )

        return True, "APPROVED", "Requête conforme aux règles et plafonds d'autorité."
