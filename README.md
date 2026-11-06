# Gouvernance Agentique d'Entreprise pour l'Assurance 🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-brightgreen.svg)](https://www.python.org/)
[![Protocol: MCP](https://img.shields.io/badge/Protocol-MCP%202.x-indigo.svg)](https://modelcontextprotocol.io/)
[![Regulatory: ACPR | DDA | DORA](https://img.shields.io/badge/Conformit%C3%A9-ACPR%20%7C%20DDA%20%7C%20DORA-emerald.svg)]()

> **Cadre stratégique, architectural et prototype opérationnel pour gouverner, piloter et contrôler une flotte d'agents IA décentralisés au sein d'une compagnie d'assurance multi-branches.**

---

## 🎯 Vision Exécutive

Dans une compagnie d'assurance (Distribution, Gestion, Sinistres, Réclamations, Actuariat, Marketing), l'avènement de l'IA agentique permet à chaque collaborateur et direction de créer ses propres outils.

Ce projet apporte la solution au dilemme de la Direction Générale : **Permettre la subsidiarité et l'innovation métier décentralisée tout en garantissant une gouvernance absolue, le respect du code des pratiques, la conformité réglementaire (DDA, ACPR, DORA, RGPD) et des plafonds d'autorité financière stricts.**

```mermaid
flowchart TD
    subgraph METIERS["1. DIRECTIONS MÉTIERS (Développement Décentralisé)"]
        direction TB
        A1["Agent Distribution & Réseau\n(Devis, Remises, Prospection)"]
        A2["Agent Sinistres & Réclamation\n(Règlement direct, Instruction)"]
        A3["Agent Actuariat & Data\n(Tarification, Surveillance S/P)"]
        A4["Agent Marketing & Satisfaction\n(Rétention, Enquêtes)"]
    end

    subgraph CONTROL_PLANE["2. STRUCTURE MAÎTRE (Serveur MCP de Contrôle)"]
        direction TB
        REGISTRY["Agent Registry & Passports\n(Identité, Niveaux L1-L3, Habilitations)"]
        GATEWAY["Passerelle & Garde-fous\n(Masquage RGPD, Détection Secret Médical)"]
        OPA["Moteur de Règles & Matrice de Pouvoir\n(Plafonds financiers déterministes)"]
        AUDIT["Observabilité & Journal Immuable\n(Audit Trail horodaté ACPR)"]
    end

    subgraph SI["3. EXÉCUTION RÉGULÉE"]
        CORE_SI["SI Coeur & Comptabilité\n(Virements, Contrats)"]
        HITL["Validation Humaine Obligatoire\n(Corbeille Superviseur HITL)"]
    end

    METIERS -->|Appels outillés standardisés MCP| CONTROL_PLANE
    CONTROL_PLANE -->|Si sous le seuil d'autorité| CORE_SI
    CONTROL_PLANE -->|Si dépassement de seuil ou litige| HITL
```

---

## 📂 Contenu du Répertoire

* **`docs/` & `mkdocs.yml`** : Documentation intégrale en 9 chapitres au format MkDocs (thème Material) détaillant la stratégie, les 6 angles morts, la matrice de délégation, l'architecture et la roadmap.
* **`mcp-server/`** : Prototype opérationnel du Serveur MCP Maître d'Assurance en Python (`mcp 2.3.0`) avec 7 scénarios réels de test.
* **`cockpit/`** : Cockpit visuel interactif HTML/Tailwind pour simuler les interceptions en temps réel et piloter les indicateurs FinOps / conformité.

---

## ⚡ Démarrage Rapide

### 1. Lancer la Démonstration en Direct (Serveur MCP)

```bash
cd mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Lancer la simulation d'un cas sinistre avec interception MCP :
python run_live_demo.py
```

### 2. Exécuter le Banc de Test Automatisé (7 Scénarios)

```bash
python test_client_harness.py
```

**Les 7 contrôles validés :**
1. **Masquage RGPD :** Masquage automatique des IBAN lors de la consultation d'un contrat.
2. **Règlement Direct sous Seuil (450 € < 800 €) :** Virement validé en autonomie L2.
3. **Dépassement de Seuil (1 850 € > 800 €) :** Interception physique et création d'un ticket HITL pour le gestionnaire humain.
4. **Refus de Garantie (Invariant Juridique) :** Interdiction stricte aux agents de refuser une garantie (dossier routé au Juridique).
5. **Secret Médical :** Blocage immédiat de requêtes manipulant des données de santé sans habilitation.
6. **Kill-Switch DORA :** Révocation instantanée d'un agent en anomalie par le RSSI.
7. **Rapport d'Audit ACPR :** Traçabilité immuable avec ID de preuve.

### 3. Consulter la Documentation Complète MkDocs

```bash
pip install mkdocs mkdocs-material
mkdocs serve
# Ouvrir http://127.0.0.1:8000
```

---

## ⚖️ Matrice des Pouvoirs Numériques

| Direction | Opération d'Assurance | Niveau L3 (Autonome) | Niveau L2 (Délégué) | Escalade HITL (L1) |
| :--- | :--- | :--- | :--- | :--- |
| **Gestion des Sinistres** | Indemnisation directe facture réparateur | < 300 € | 300 € à 800 € | > 800 € ou suspicion fraude |
| **Gestion des Sinistres** | Refus formel de garantie | **Interdit** | **Interdit** | **100% Humain obligatoire** |
| **Sinistres Corporels** | Évaluation préjudice & offre indemnité | **Interdit** | **Interdit** | **100% Médecin / Inspecteur** |
| **Distribution / Réseau** | Remise commerciale sur devis annuel | 0% à 3% | 3,1% à 7% | > 7% ou dérogation clauses |
| **Actuariat & Risques** | Modification barème de tarification | **Interdit** | **Interdit** | **Chef Actuaire + DG** |

---

## 📜 Licence & Propriété

Projet développé pour la gouvernance agentique d'entreprise dans le secteur de l'assurance. Sous licence MIT.
