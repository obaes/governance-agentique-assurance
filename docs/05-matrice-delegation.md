# 5. Matrice des Pouvoirs & Human-in-the-Loop (HITL)

La matrice de délégation de pouvoir numérique formalise les frontières d'autonomie entre l'agent et le collaborateur humain. Elle est directement transcrite en règles déterministes dans le moteur de règles Open Policy Agent (OPA).

---

## 5.1 Grille Opérationnelle par Direction

| Direction | Opération d'Assurance | Niveau L3 (Autonome) | Niveau L2 (Délégué / Audit continu) | Escalade HITL Obligatoire (L1) |
| :--- | :--- | :--- | :--- | :--- |
| **Gestion des Sinistres** | Indemnisation directe bris de glace / petit matériel | < 300 € | 300 € à 800 € | > 800 € ou non concordance des factures |
| **Gestion des Sinistres** | Mandatement d'un expert automobile / bâtiment | Automatique si barème respecté | Dossier atypique | Suspicion de fraude > 0.35 |
| **Gestion des Sinistres** | Refus formel de garantie | **Strictement interdit** | **Strictement interdit** | **100% Humain (Gestionnaire + Juriste)** |
| **Sinistres Corporels** | Calcul des provisions et indemnisation | **Strictement interdit** | **Strictement interdit** | **100% Humain (Inspecteur corporel / Médecin)** |
| **Distribution / Réseau** | Remise commerciale sur prime annuelle | 0% à 3% | 3,1% à 7% | > 7% ou dérogation de garanties |
| **Distribution / Réseau** | Souscription en ligne contrat IARD standard | Profil sans sinistre antérieur | 1 sinistre non responsable | Profil hors norme / Risque aggravé |
| **Actuariat & Tarification**| Modification des règles de calcul de prime | **Strictement interdit** | **Strictement interdit** | **Validation formelle Chef Actuaire + Direction** |
| **Actuariat & Risques** | Alerting dérive sinistralité (S/P) | Surveillance continue autonome | - | Déclenchement alerte CODIR si ratio > 105% |
| **Réclamation & Qualité** | Geste commercial de conciliation | < 50 € | 50 € à 150 € | > 150 € ou menace de saisine médiateur |
| **Relation Clientèle** | Émission d'attestation d'assurance | Immédiate si contrat à jour | - | Blocage si contentieux impayé en cours |

---

## 5.2 Les 4 Invariants Juridiques Non Négociables

1. **Aucun refus de prise en charge par une machine :** Un agent ne peut en aucun cas notifier un refus de garantie à un assuré sans qu'un être humain qualifié n'ait analysé le dossier et signé la décision.
2. **Sanctuarisation du secret médical :** Les agents ne disposant pas expressément d'une habilitation corporelle certifiée ne peuvent recevoir ni traiter aucun compte-rendu médical ou certificat d'ITT.
3. **Plafonnement financier strict :** Tout ordre de paiement ou de virement émis par un agent est capé par la passerelle à un montant maximal inviolable.
4. **Devoir de conseil DDA :** Tout devis proposé à un client ou prospect doit s'accompagner de la traçabilité des besoins exprimés pour prouver le caractère loyal et adapté du conseil.
