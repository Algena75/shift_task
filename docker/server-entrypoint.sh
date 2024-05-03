#!/bin/sh

until  alembic upgrade head 
do
    echo "Waiting for db to be ready..."
    sleep 2
done


poetry run project
