#!/bin/bash

source activate_dev_env.sh
source ./devops/set_environment_for_docker_scheduler.sh

cwd=`pwd`

cd foundations_ui \
    && yarn install \
    && export CYPRESS_LOCAL_FOUNDATIONS_HOME="${cwd}/foundations_ui/cypress/fixtures/atlas_scheduler/.foundations" \
    && export CYPRESS_SCHEDULER_IP=127.0.0.1 \
    && export CYPRESS_SCHEDULER_FOUNDATIONS_HOME=/home/pairing/.foundations \
    && export CYPRESS_SCHEDULER_REDIS_PORT=5556 \
    && export CYPRESS_GUI_HOST=127.0.0.1\
    && export CYPRESS_GUI_PORT=5555 \
    && export CYPRESS_ATLAS_EDITION=CE \
    && npm run cy:run