# 9. Prototype MCP Opérationnel (Code & Validation)

Le prototype fonctionnel de la **Structure Maître MCP (Model Context Protocol)** a été développé et validé dans le répertoire `/home/antigravity/mcp-master-prototype`.

---

## 9.1 Architecture du Code Source

```
/home/antigravity/mcp-master-prototype/
├── registry.py             # Registre des Passeports d'Agents & Kill-Switch
├── guardrails.py           # Moteur Policy-as-Code (PII, Santé, Seuils d'autorité)
├── audit_store.py          # Journal immuable d'audit (ACPR & DORA)
├── server.py               # Serveur MCP Maître exposant les outils sécurisés
└── test_client_harness.py  # Banc d'essai automatisé (7 scénarios de test)
```

---

## 9.2 Les 7 Scénarios de Contrôle Validés

Le banc d'essai `test_client_harness.py` a été exécuté avec succès et valide les contrôles suivants :

1. **Consultation de Contrat avec Masquage RGPD :**
   * L'agent consulte le contrat `POL-AUTO-8821`.
   * L'IBAN de l'assuré est automatiquement masqué (`[IBAN-MASQUÉ-RGPD]`) avant restitution à l'agent.
2. **Règlement Direct sous Seuil (450 € < 800 €) :**
   * L'agent ordonne le paiement d'une facture de pare-brise de 450,00 €.
   * Le contrôle vérifie que $450 \le 800$ € : **Virement validé immédiatement en autonomie (L2)** et journalisé avec l'identifiant `AUD-20261106-1002`.
3. **Dépassement du Seuil Financier (2 400 € > 800 €) :**
   * L'agent tente d'ordonner un paiement de 2 400,00 € suite à un choc parking.
   * La passerelle intercepte la requête : **Virement bloqué et escalade humaine automatique (HITL)** vers la corbeille du superviseur avec le ticket `HITL-TASK-0902`.
4. **Interception d'un Refus de Garantie (Invariant Juridique) :**
   * L'agent tente de notifier un refus de prise en charge pour exclusion de garantie.
   * La passerelle bloque l'action : **Interdiction légale d'émettre un refus sans signature d'un gestionnaire habilité** ; le dossier est routé vers le Contentieux.
5. **Détection de Données de Santé (Violation RGPD / Secret Médical) :**
   * Une note mentionnant un *"traumatisme cervical"* est transmise à un agent matériel.
   * L'agent n'ayant pas d'habilitation corporelle, **la requête est rejetée immédiatement pour motif de sécurité**.
6. **Arrêt d'Urgence DORA (Kill Switch) :**
   * L'administrateur active le Kill-Switch sur l'agent `AGT-SIN-001`.
   * Toutes les requêtes ultérieures de cet agent sont instantanément rejetées (`BLOCKED_SECURITY`). Le rétablissement s'effectue en 1 clic.
7. **Rapport d'Audit et de Conformité ACPR :**
   * Extraction des statistiques en temps réel (taux d'autonomie à 40%, 1 escalade HITL, 2 blocages pour non-conformité, 0 fuite de données).

---

## 9.3 Commandes d'Exécution du Prototype

Pour relancer le banc d'essai :

```bash
cd /home/antigravity/mcp-master-prototype
.venv/bin/python test_client_harness.py
```
