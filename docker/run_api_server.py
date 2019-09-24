# Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
# Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018

import logging
import os

os.environ['FOUNDATIONS_COMMAND_LINE'] = 'True'

from foundations_contrib.global_state import config_manager
from foundations_rest_api.global_state import app_manager
import subprocess
import yaml

if os.path.exists("/root/.kube"):
    from foundations_scheduler_plugin.config.scheduler import translate
    
    nodes_yaml = subprocess.check_output(["/bin/bash", "-c", "kubectl get node -o yaml -l node-role.kubernetes.io/master="""]).decode()
    nodes = yaml.load(nodes_yaml)
    master_ip = nodes['items'][0]['status']['addresses'][0]['address']

    submission_config = {
        'results_config': {
            'redis_end_point': os.environ["REDIS_URL"]
        },
        'ssh_config': {
            'host': master_ip,
            'port': 31222,
            'code_path': '/jobs',
            'key_path': '~/.ssh/id_foundations_scheduler',
            'user': 'job-uploader'
        }
    }
    translated_submission_config = translate(submission_config)
else:
    translated_submission_config = {'redis_url': os.environ["REDIS_URL"]}

configuration = config_manager.config()
configuration.update(translated_submission_config)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('/var/foundations/rest_api.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

root_logger.info("Running with configuration {}".format(configuration))

app = app_manager.app()

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Type"] = "application/json"
    return response
