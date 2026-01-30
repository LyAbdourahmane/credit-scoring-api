# **API de Scoring Crédit (MLOps – Déploiement & Monitoring)**

## **Contexte du projet**

Ce projet s’inscrit dans la continuité du travail réalisé dans *Initiez-vous au MLOps (partie 1/2)*.  
Après avoir entraîné, versionné et évalué un modèle de scoring crédit avec MLflow, l’objectif est désormais de :

- **déployer le modèle en production via une API**  
- **conteneriser l’application avec Docker**  
- **mettre en place un pipeline CI/CD**  
- **monitorer les performances du modèle et détecter la dérive des données**  

Ce travail simule la mission confiée par Chloé Dubois, Lead Data Scientist chez *Prêt à Dépenser*, pour permettre au département *Crédit Express* d’utiliser le modèle en quasi temps réel.

---

# **Objectifs du projet**

### ✔ Développer une API de scoring (FastAPI)  
L’API reçoit les données d’un client et retourne :

- une probabilité de défaut  
- une prédiction binaire (0 = accepté, 1 = refusé)

### ✔ Conteneuriser l’API avec Docker  
L’image Docker doit être :

- légère  
- reproductible  
- compatible avec un déploiement cloud (Render)

### ✔ Déployer automatiquement via CI/CD  
Pipeline GitHub Actions permettant :

- exécution des tests unitaires  
- build de l’image Docker  
- déploiement automatique sur Render

### ✔ Mettre en place un monitoring  
Collecte et analyse :

- des inputs / outputs du modèle  
- des latences  
- des distributions des features  
- de la dérive des données (Evidently AI)

### ✔ Documenter l’ensemble du projet  
README complet + screenshots + instructions de lancement.

---

# **1. API FastAPI**

### Endpoint principal : `/predict`

**Méthode :** `POST`  
**Sécurité :** API Key (`x-api-key`)  
**Entrée :** JSON validé par Pydantic  
**Sortie :**

```json
{
  "prediction": 0,
  "probability": 0.23
}
```

### 📍 Endpoint de test : `/`

Retourne des informations sur le modèle et la version.

### 📍 Chargement du modèle

Le modèle est chargé **une seule fois au démarrage** :

- évite les lenteurs  
- améliore la scalabilité  
- réduit la consommation mémoire  

---

# **3. Déploiement Render**

L’API est déployée automatiquement via Render :

- Build Docker automatique  
- Déploiement continu  
- URL publique :  
  **https://credit-scoring-api-1-op28.onrender.com**

### Variables d’environnement

| Nom | Description |
|-----|-------------|
| `API_KEY` | Clé d’accès à l’API |

---

# **4. Pipeline CI/CD (GitHub Actions)**

Pipeline automatisé :

1. **Tests unitaires**  
2. **Build Docker**  
3. **Push image**  
4. **Déploiement Render**

### `.github/workflows/cicd.yml`

- Séparation des étapes : test → build → deploy  
- Gestion des secrets GitHub  
- Déclenchement sur `push main ou master`

---

# **5. Tests unitaires**

Tests réalisés avec `pytest` :

- validation des schémas Pydantic  
- test du endpoint `/predict`  
- test du chargement du modèle  
- test des erreurs (API key, données invalides)

Exécution :

```bash
pytest -v
```

---

# **6. Monitoring & Data Drift**

### Données collectées

- Inputs du modèle  
- Outputs (probabilité + prédiction)  
- Latence  
- Timestamp  
- Statut HTTP  

### Analyse Evidently

Un notebook dédié :

```
notebook/monitoring.ipynb
```

Permet :

- comparaison des distributions  
- détection de dérive  
- analyse des performances  
- visualisation des métriques  

### Stockage des logs

- local : fichiers JSONL

---

# **7. Optimisation post-déploiement**

Tests réalisés :

- mesure du temps d’inférence  
- profiling CPU  
- optimisation du pipeline de features  
- réduction du poids du modèle  
- amélioration du Dockerfile  

---

# **9. Documentation Swagger**

Une fois l’API lancée :

- Swagger UI :  
  **http://localhost:8000/docs**

- ReDoc :  
  **http://localhost:8000/redoc**

---

# **10. Sécurité**

- API Key obligatoire  
- Validation stricte des entrées (Pydantic)  
- Aucun chargement du modèle à chaque requête  
- Secrets gérés via GitHub Secrets + Render Environment Variables  

---
