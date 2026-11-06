# 1. Contexte & Enjeux

## 1.1 L'Organisation Traditionnelle face à la Vague Agentique

Dans une compagnie d'assurance traditionnelle, les activités sont cloisonnées par spécialité métier et par direction :
* **Distribution & Réseau :** Vente directe, courtiers, agents généraux, partenariats.
* **Gestion des Contrats :** Émission, avenants, résiliations, quittancement.
* **Gestion des Sinistres & Réclamations :** Déclaration, mission d'expert, calcul d'indemnité, recours.
* **Actuariat & Data :** Tarification, calcul des provisions techniques (Best Estimate), modélisation des risques Solvabilité II.
* **Relation Client & Marketing :** Rétention, fidélisation, enquêtes de satisfaction NPS.

Ces directions s'appuient historiquement sur des systèmes d'information lourds (progiciels de gestion d'assurance, ERP, CRM) dont les cycles de modification prennent plusieurs mois.

## 1.2 La Révolution Agentique : Une Opportunité et un Péril

L'avènement de l'IA agentique bouleverse cette donne :
* **Démocratisation :** N'importe quel collaborateur ou direction peut désormais concevoir ses propres outils, scripts et agents autonomes en langage naturel.
* **Agilité Métier :** Une équipe sinistres peut automatiser l'analyse de factures d'artisans en quelques jours ; le marketing peut orchestrer des campagnes d'écoute personnalisées en temps réel.
* **Le Danger du Chaos Décentralisé :** Sans cadre, ce foisonnement engendre du **Shadow Agentic IT** :
    * Multiplication des clés API non sécurisées.
    * Décisions juridiques prises par des agents sans pouvoir d'engagement.
    * Fuite de données personnelles ou de santé vers des modèles tiers non conformes.
    * Hallucinations contractuelles engageant la responsabilité financière de la compagnie.

## 1.3 L'Ambition du Modèle Fédéré (Hub & Spoke)

L'objectif de cette stratégie n'est **pas d'interdire** ou de recentraliser le développement des agents à la DSI, ce qui briderait l'innovation métier.

Il s'agit d'instaurer un **modèle fédéré** :
* **Les Spokes (Directions Métiers) :** Développent, innovent et adaptent leurs agents à leurs besoins quotidiens.
* **Le Hub Central (Structure Maître) :** Fournit le cadre régalien, la passerelle sécurisée, le contrôle d'accès aux données de l'entreprise et la certification réglementaire.
