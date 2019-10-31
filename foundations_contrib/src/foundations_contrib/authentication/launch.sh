#!/usr/bin/env sh

docker run -d --name keycloak2 \
    -e KEYCLOAK_USER=admin \
    -e KEYCLOAK_PASSWORD=admin \
    -e KEYCLOAK_IMPORT=/keycloak/atlas.json \
    -v $(realpath keycloak):/keycloak \
    -p 8080:8080 \
    jboss/keycloak