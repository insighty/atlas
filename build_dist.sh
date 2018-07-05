#!/bin/bash

python_version=$1

wheel_suffix=""

if [[ "${python_version}" = "python2" ]]
then
    wheel_suffix="py2"
elif [[ "${python_version}" = "python3" ]]
then
    wheel_suffix="py3"
else
    echo "Usage: ./build_dist.sh (python2|python3)"
    exit 1
fi

cd vcat_sdk/ && \
    ${python_version} setup.py sdist bdist_wheel && \
    cd ../ && \
    ${python_version} -m pip install -U vcat_sdk/dist/vcat-0.0.1-${wheel_suffix}-none-any.whl && \
    cd gcp_utils/ && \
    ${python_version} setup.py sdist bdist_wheel && \
    cd ../ && \
    ${python_version} -m pip install -U gcp_utils/dist/vcat_gcp-0.0.1-${wheel_suffix}-none-any.whl && \
    cd ssh_utils/ && \
    ${python_version} setup.py sdist bdist_wheel &&\
    cd ../ && \
    ${python_version} -m pip install -U ssh_utils/dist/vcat_ssh-0.0.1-${wheel_suffix}-none-any.whl && \
    cd mlflow_utils/ && \
    ${python_version} setup.py sdist bdist_wheel &&\
    cd ../ && \
    ${python_version} -m pip install -U mlflow_utils/dist/vcat_mlflow-0.0.1-${wheel_suffix}-none-any.whl
