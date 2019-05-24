#!/bin/bash
docker run -d 
exit 0

postgres:
                image: docker.ask4ua.com/whir-db
                ports:
                        - 5432:5432
                volumes:
                        - postgres_vol:/var/lib/postgresql/data
                secrets:
                        - whir_db_password
                        - root_db_password
                environment:
                        - POSTGRES_USER=whir
                        - POSTGRES_DB=whir
                        - POSTGRES_PASSWORD_FILE=/run/secrets/whir_db_password
                        - POSTGRES_ROOT_PASSWORD_FILE=/run/secrets/root_db_password
                networks:
                        - whirnet
                deploy:
                        placement:
                                constraints: [node.role == manager]
                        replicas: 1
                        restart_policy:
                                condition: any

