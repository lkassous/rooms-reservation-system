#!/bin/bash

# Variables
BACKUP_DIR="/backups"  # Répertoire où les sauvegardes seront stockées
DB_CONTAINER_NAME="postgres-db"  # Nom du pod PostgreSQL
DB_NAME="reservationsdb"  # Nom de la base de données
DB_USER="admin"  # Utilisateur PostgreSQL
DB_PASSWORD="admin"  # Mot de passe PostgreSQL
BACKUP_FILE="${DB_NAME}_$(date +\%Y\%m\%d\%H\%M\%S).sql"

# Créer le répertoire de sauvegarde si nécessaire
mkdir -p $BACKUP_DIR

# Exécuter la commande de sauvegarde PostgreSQL
kubectl exec -it $DB_CONTAINER_NAME -- pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/$BACKUP_FILE

# Vérifier que la sauvegarde a réussi
if [ $? -eq 0 ]; then
    echo "Sauvegarde réussie: $BACKUP_FILE"
else
    echo "Échec de la sauvegarde"
fi
