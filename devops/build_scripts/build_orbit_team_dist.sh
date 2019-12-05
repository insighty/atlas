#!/bin/bash

script_location="$(pwd)/devops/build_scripts"
source "$script_location/build_common.sh"

cwd=`pwd`

rm -rf dist/* && \
    build_module foundations_internal foundations_internal $cwd && \
    build_module foundations_events foundations_events $cwd && \
    build_module foundations_contrib foundations_contrib $cwd && \
    build_module foundations_local_docker_scheduler_plugin foundations_local_docker_scheduler_plugin $cwd && \
    build_module foundations_sdk dessa_foundations $cwd && \
    build_module foundations_orbit_sdk foundations_orbit $cwd && \
    build_module foundations_core_rest_api_components foundations_core_rest_api_components $cwd && \
    build_module foundations_rest_api foundations_rest_api $cwd && \
    build_module foundations_orbit_rest_api foundations_orbit_rest_api $cwd