“Plus de 50% des features présentent une dérive statistiquement significative.
Les dérives les plus importantes concernent les variables EXT_SOURCE_2, EXT_SOURCE_3, AMT_REQ_CREDIT_BUREAU_YEAR et HOUR_APPR_PROCESS_START.
Ces variables sont critiques pour le modèle de scoring, ce qui suggère que les données de production ne sont pas représentatives du dataset d’entraînement.
Dans un contexte réel, cela pourrait entraîner une dégradation progressive des performances du modèle.”

“Le système de monitoring détecte correctement la dérive des données.
Les dérives observées sont cohérentes avec le faible volume de données de production et la nature simulée des requêtes.
Dans un environnement réel, ces dérives nécessiteraient une surveillance continue et potentiellement un réentraînement du modèle.”

“L’analyse opérationnelle réalisée avec Evidently sur les métriques status_code et latency_ms ne montre aucune dérive.
Les distributions observées en production sont cohérentes avec la référence, ce qui indique que l’API est stable, que les temps de réponse sont maîtrisés et qu’aucune augmentation anormale du taux d’erreur n’a été détectée.”

Et tu peux ajouter :

“Cette stabilité opérationnelle est un prérequis essentiel avant d’entamer la phase d’optimisation du modèle et de l’infrastructure.”

Le pic à 1528 ms est anormal → probablement un cold start ou un premier chargement du modèle.
Ton API est performante, mais souffre d’un goulot d’étranglement au démarrage.

L’analyse des logs de production montre que le modèle présente un temps d’inférence moyen de 15 à 25 ms, ce qui est excellent pour un modèle de scoring. Un pic de latence à 1528 ms a été observé lors de la première requête, indiquant un cold start lié au chargement initial du modèle.

Le taux d’erreur est faible, avec deux erreurs 422 dues à des valeurs manquantes dans les données d’entrée. Aucun drift opérationnel n’a été détecté sur la latence ou les codes HTTP.

Goulots d’étranglement identifiés
Cold start important lors de la première prédiction.

Validation Pydantic trop stricte, entraînant des erreurs 422.

Optimisations réalisées

Ajout d’un warm-up au démarrage de l’API

Assouplissement de la validation Pydantic

Augmentation du nombre de workers Uvicorn
