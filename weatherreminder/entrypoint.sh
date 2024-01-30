#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Deleting "
python manage.py flush --no-input

echo "Start migration"
python manage.py makemigrations
python manage.py migrate
echo "Migration done!"

#echo "Creating test user"
#python manage.py filler

exec "$@"
