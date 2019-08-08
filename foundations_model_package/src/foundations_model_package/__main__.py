"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def main():
    import os

    from foundations_model_package.job import Job
    from foundations_model_package.redis_actions import indicate_model_ran_to_redis
    from foundations_model_package.resource_factories import prediction_resource
    from foundations_model_package.flask_app import flask_app

    _hack_for_cleaning_up_logs()

    job = Job(os.environ['JOB_ID'])

    prediction_function = _load_prediction_function(job)

    root_model_serving_resource = prediction_resource(prediction_function)
    predict_model_serving_resource = prediction_resource(prediction_function)
    app = flask_app(root_model_serving_resource, predict_model_serving_resource)
    indicate_model_ran_to_redis(job.id())

    print('Model server running successfully')

    app.run(debug=False, port=80, host='0.0.0.0')

def _hack_for_cleaning_up_logs():
    import click
    import logging

    def _break_click_echo(*args, **kwargs):
        pass

    click.echo = _break_click_echo
    click.secho = _break_click_echo

    log = logging.getLogger('werkzeug')
    log.disabled = True

def _module_name_and_function_name(manifest):
    prediction_definition = manifest['entrypoints']['predict']
    return prediction_definition['module'], prediction_definition['function']

def _move_to_job_directory(job):
    import sys
    import os

    root_of_the_job = job.root()
    if not os.path.exists(root_of_the_job):
        raise Exception(f'Job, {job.id()} not found!')

    sys.path.insert(0, root_of_the_job)
    os.chdir(root_of_the_job)

def _add_module_to_sys_path(job_root, module_name):
    import sys
    import os.path

    module_path = module_name.replace('.', '/')
    module_directory = os.path.dirname(module_path)
    if module_directory:
        module_directory = f"{job_root}/{module_directory}"
        sys.path.insert(0, module_directory)

def _load_prediction_function(job):
    import importlib

    _move_to_job_directory(job)
    module_name, function_name = _module_name_and_function_name(job.manifest())
    _add_module_to_sys_path(job.root(), module_name)

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as error:
        raise Exception('Prediction module defined in manifest file could not be found!') from error
    except Exception as error:
        raise Exception('Unable to load prediction module from manifest') from error

    function = getattr(module, function_name, None)

    if not function:
        raise Exception('Prediction function defined in manifest file could not be found!')

    return function

if __name__ == '__main__':
    main()