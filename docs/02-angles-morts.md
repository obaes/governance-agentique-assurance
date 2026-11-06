# 2. Les 6 Angles Morts Majeurs

La mise en place d'une structure de contrôle pour agents autonomes en assurance requiert d'anticiper 6 risques systémiques spécifiques au secteur :

---

### Angle Mort 1 : La Délégation de Pouvoir et l'Engagement Juridique
* **Problématique :** Qui engage juridiquement la compagnie lorsqu'un agent envoie un email ou valide un paiement ?
* **Impact en assurance :** En droit des assurances, une confirmation écrite émanant de la compagnie (même générée par une IA) peut constituer un engagement contractuel ou une renonciation tacite à une déchéance de garantie.
* **Réponse de la Structure Maître :** Tout agent doit obligatoirement être rattaché à une délégation de pouvoir formelle codifiée dans son passeport. Tout dépassement de seuil financier ou toute modification contractuelle déclenche un blocage physique de la passerelle vers une file de validation humaine (HITL).

---

### Angle Mort 2 : La Dérive de Souscription & le Risque Solvabilité II
* **Problématique :** Si les équipes commerciales ou réseau créent des agents de devis autonomes avec des capacités de négociation, ils risquent d'accorder des remises ou d'adapter des critères de souscription pour maximiser le chiffre d'affaires.
* **Impact en assurance :** Dégradation du ratio sinistres à primes (S/P) et altération du profil de risque sans concertation de l'actuariat, menaçant le modèle interne de solvabilité.
* **Réponse de la Structure Maître :** Les barèmes actuariels et les conditions de souscription sont exposés via des "APIs d'or" intangibles. Les agents métiers ne peuvent que consommer les règles sans jamais pouvoir en altérer les formules.

---

### Angle Mort 3 : La Ségrégation Stricte des Données (RGPD, Données de Santé)
* **Problématique :** En assurance de personnes ou en sinistres corporels, les agents manipulent des données médicales hautement sensibles.
* **Impact en assurance :** Sanctions sévères de la CNIL et violation du secret médical si des données de santé transitent par des LLM publics ou si elles sont indexées dans des bases RAG accessibles aux équipes marketing.
* **Réponse de la Structure Maître :** Contrôle d'accès basé sur les attributs (ABAC) au niveau de la passerelle. Détection et masquage automatique (scrubbing) des données de santé avant toute sollicitation de modèle de langage.

---

### Angle Mort 4 : Le Risque de Shadow Agentic IT
* **Problématique :** Si l'enregistrement auprès de la structure maître est trop complexe, chronophage ou bureaucratique, les collaborateurs contourneront le dispositif en utilisant des outils SaaS grand public.
* **Réponse de la Structure Maître :** Proposer un "Starter Kit" attractif. La structure maître doit offrir de la valeur immédiate aux créateurs d'agents : connecteurs CRM déjà configurés, accès gratuit aux meilleurs LLM souverains, et référentiel contractuel déjà indexé.

---

### Angle Mort 5 : Résilience Opérationnelle et Règlement DORA
* **Problématique :** Le règlement européen DORA impose aux institutions financières une résilience sans faille face aux risques informatiques liés aux tiers.
* **Impact en assurance :** Si votre processus de déclaration de sinistre repose sur une API d'un fournisseur unique de LLM et que ce dernier subit une panne mondiale de 12 heures, la compagnie est en non-conformité DORA.
* **Réponse de la Structure Maître :** Routage multi-fournisseurs (Multi-LLM Fallback) et "Kill Switch" d'urgence permettant de débrayer immédiatement un agent en anomalie vers un workflow dégradé ou 100% humain.

---

### Angle Mort 6 : L'Auditabilité et l'Explicabilité (ACPR / Médiation)
* **Problématique :** L'ACPR et le Médiateur de l'Assurance exigent qu'un refus de garantie ou une résiliation soit motivé de manière claire, transparente et non discriminatoire.
* **Réponse de la Structure Maître :** Journalisation immuable de chaque étape de raisonnement de l'agent (Audit Trail) : prompt système initial, documents consultés dans le RAG, calculs effectués et horodatage certifié.
