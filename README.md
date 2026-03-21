# meteo-vs-transports

docker compose up -d
    Démarre tous les services définis dans le docker-compose.yaml en mode détaché (en arrière-plan).

docker compose exec airflow-webserver ls /opt/airflow/dags
    Exécute la commande 'ls /opt/airflow/dags' à l'intérieur du conteneur 'airflow-webserver' 
    pour lister les fichiers DAG présents dans le dossier monté.

docker compose up --build -d
    Reconstruit les images Docker si nécessaire (Dockerfile ou dépendances modifiées) 
    puis démarre les services en mode détaché.

docker compose up airflow-init
    Démarre le service 'airflow-init' défini dans le docker-compose.yaml, 
    utilisé pour initialiser la base de données et créer les utilisateurs.

docker compose rm -f airflow-init
    Supprime le conteneur 'airflow-init' sans demander de confirmation (-f = force).

docker compose restart airflow-webserver airflow-scheduler
    Redémarre les conteneurs 'airflow-webserver' et 'airflow-scheduler', utile pour 
    recharger les DAGs ou appliquer des changements sans rebuild complet.

docker ps
    Affiche la liste des conteneurs Docker actuellement en fonctionnement.

docker ps -a
    Affiche la liste de tous les conteneurs Docker, qu'ils soient en fonctionnement ou arrêtés.

docker compose logs airflow-webserver
    Affiche les logs du conteneur 'airflow-webserver' pour vérifier le démarrage, 
    le chargement des DAGs et d’éventuelles erreurs.