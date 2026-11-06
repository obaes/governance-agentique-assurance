# 4. Passeport d'Agent (Spécification Technique)

Le **Passeport d'Agent** est le contrat d'accréditation technique que chaque direction doit soumettre au registre central pour enregistrer un agent. Il est versionné dans le dépôt Git de l'agent (`agent-passport.yaml`).

---

## 4.1 Schéma Formel YAML

```yaml
apiVersion: governance.assurance/v1
kind: AgentPassport

metadata:
  agent_id: "AGT-SIN-2026-04"
  name: "ClaimAssist-Auto-QuickSettlement"
  version: "1.2.0"
  direction: "Gestion & Sinistres"
  business_owner: "martine.dubois@votreassurance.fr"
  technical_owner: "dev-sinistres@votreassurance.fr"
  description: "Instruction et règlement direct des bris de glace et chocs légers sans tiers."

governance:
  # Niveaux d'autonomie :
  # - L1 : Copilote / Validation humaine systématique
  # - L2 : Semi-autonome sous seuils plafonnés avec audit continu
  # - L3 : Autonome (actions directes selon liste blanche stricte)
  autonomy_level: "L2"
  
  # Périmètre de délégation juridique et financière
  legal_authority:
    max_settlement_eur: 800.00           # Seuil maximum d'indemnité directe
    commercial_discount_max_percent: 0.0 # Remise commerciale autorisée
    contractual_amendment_allowed: false # Droit d'émettre des avenants
    claim_refusal_allowed: false         # Refus formel de garantie (INTERDIT aux agents)
  
  # Déclencheurs obligatoires d'escalade humaine (HITL)
  hitl_triggers:
    - trigger: "amount_exceeds_threshold"
      threshold_eur: 800.00
    - trigger: "fraud_score_elevated"
      threshold: 0.35
    - trigger: "coverage_exclusion_ambiguity"
    - trigger: "client_vulnerability_flag"

compliance_and_data:
  # Classification des données autorisées (ABAC)
  data_classification:
    pii_allowed: true                    # Données nominatives standards
    financial_data: true                 # Coordonnées bancaires pour virement
    health_data: false                   # Données de santé (bloqué physiquement si false)
  
  # Sources certifiées imposées (Grounding)
  grounding_sources:
    - "rag://clausier-auto-particuliers-2026"
    - "api://bareme-reparateurs-agrees-v3"
  
  # Contrôles de conformité obligatoires
  regulatory_checks:
    pog_dda_compliance: true             # Conformité Directive Distribution d'Assurance
    acpr_explainability_level: "full"    # Journalisation de l'arbre décisionnel

resilience_dora:
  kill_switch_enabled: true              # Débrayage d'urgence disponible
  fallback_mode: "route_to_human_queue"
  rate_limits:
    max_requests_per_minute: 60
    max_tokens_per_day: 500000
```

---

## 4.2 Cycle de Vie et Homologation

1. **Commit & Pull Request :** L'équipe métier dépose son code et le fichier `agent-passport.yaml`.
2. **Validation Statique du Passeport :** Le linter central vérifie la conformité du fichier aux politiques de sécurité (ex: si l'équipe demande `health_data: true`, le DPO doit apposer une signature cryptographique).
3. **Exécution du Banc de Test (Sandbox) :** Le pipeline CI/CD soumet l'agent aux cas d'usage types d'assurance.
4. **Signature & Émission du Jeton :** Une fois le score d'homologation atteint (> 98%), la passerelle émet un jeton d'accès mTLS de production.
