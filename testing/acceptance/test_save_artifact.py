"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

import json
import foundations

class TestSaveArtifact(Spec):

    @let
    def _artifact_archive(self):
        from foundations_contrib.archiving import load_archive
        return load_archive('artifact_archive')

    @set_up
    def set_up(self):
        import copy

        import foundations
        from foundations_contrib.global_state import redis_connection

        self._redis_connection = redis_connection

        self._old_config = copy.deepcopy(foundations.config_manager.config())
        foundations.config_manager.reset()

    @tear_down
    def tear_down(self):
        import foundations

        foundations.config_manager.config().update(self._old_config)
        self._redis_connection.flushall()

    def test_save_artifact_outside_of_job_logs_warning(self):
        import subprocess

        completed_process = subprocess.run(['bash', '-c', 'cd acceptance/fixtures/save_artifact && python main.py'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        self.assertIn('WARNING', process_output)
        self.assertIn('Cannot save artifact outside of job.', process_output)

    def test_save_artifact_with_filepath_only_saves_file_with_key_equal_to_basename_and_saves_metadata_with_extension_in_redis(self):
        job_deployment = foundations.deploy(job_directory='acceptance/fixtures/save_artifact', env='stageless_local')
        job_deployment.wait_for_deployment_to_complete()

        job_id = job_deployment.job_name()
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'cool-artifact.txt': 'cool-artifact.txt'
            },
            'metadata': {
                'cool-artifact.txt': {}
            }
        }

        self.assertEqual(b'contents of artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_with_filepath_and_key_saves_file_with_specified_key_and_saves_metadata_with_extension_in_redis(self):
        job_deployment = foundations.deploy(job_directory='acceptance/fixtures/save_artifact_with_key', env='stageless_local')
        job_deployment.wait_for_deployment_to_complete()

        job_id = job_deployment.job_name()
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'this-key': 'cool-artifact.txt'
            },
            'metadata': {
                'cool-artifact.txt': {}
            }
        }

        self.assertEqual(b'contents of artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_twice_with_filepath_and_key_saves_file_with_specified_key_and_saves_metadata_with_extension_in_redis(self):
        job_deployment = foundations.deploy(job_directory='acceptance/fixtures/save_artifact_with_key_twice', env='stageless_local')
        job_deployment.wait_for_deployment_to_complete()

        job_id = job_deployment.job_name()
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cooler-artifact.other', job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'this-key': 'cooler-artifact.other'
            },
            'metadata': {
                'cooler-artifact.other': {}
            }
        }

        self.assertEqual(b'contents of cooler artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_twice_with_filepath_and_key_logs_appropriate_warning(self):
        import subprocess

        completed_process = subprocess.run(['python', '-m', 'foundations', 'deploy', '--env=stageless_local', '--job-directory=acceptance/fixtures/save_artifact_with_key_twice'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        self.assertIn('WARNING', process_output)
        self.assertIn('Artifact "this-key" already exists - overwriting.', process_output)

    def test_save_artifact_twice_with_filepath_only_saves_file_and_saves_metadata_with_extension_in_redis(self):
        job_deployment = foundations.deploy(job_directory='acceptance/fixtures/save_artifact_twice', env='stageless_local')
        job_deployment.wait_for_deployment_to_complete()

        job_id = job_deployment.job_name()
        artifact_contents = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'cool-artifact.txt': 'cool-artifact.txt'
            },
            'metadata': {
                'cool-artifact.txt': {}
            }
        }

        self.assertEqual(b'contents of cooler artifact', artifact_contents)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_two_artifacts_with_different_keys_saves_files_in_archive_and_saves_metadata_with_extension_in_redis(self):
        job_deployment = foundations.deploy(job_directory='acceptance/fixtures/save_artifact_with_two_different_keys', env='stageless_local')
        job_deployment.wait_for_deployment_to_complete()

        job_id = job_deployment.job_name()
        artifact_contents_0 = self._artifact_archive.fetch_binary('user_artifacts/cool-artifact.txt', job_id)
        artifact_contents_1 = self._artifact_archive.fetch_binary('user_artifacts/cooler-artifact.other', job_id)
        artifact_metadata = json.loads(self._redis_connection.get(f'jobs:{job_id}:user_artifact_metadata'))

        expected_metadata = {
            'key_mapping': {
                'this-key': 'cool-artifact.txt',
                'that-key': 'cooler-artifact.other'
            },
            'metadata': {
                'cool-artifact.txt': {},
                'cooler-artifact.other': {}
            }
        }

        self.assertEqual(b'contents of artifact', artifact_contents_0)
        self.assertEqual(b'contents of cooler artifact', artifact_contents_1)
        self.assertEqual(expected_metadata, artifact_metadata)

    def test_save_artifact_twice_with_filepath_only_logs_appropriate_warning(self):
        import subprocess

        completed_process = subprocess.run(['python', '-m', 'foundations', 'deploy', '--env=stageless_local', '--job-directory=acceptance/fixtures/save_artifact_twice'], stdout=subprocess.PIPE)
        process_output = completed_process.stdout.decode()
        self.assertIn('WARNING', process_output)
        self.assertIn('Artifact "cool-artifact.txt" already exists - overwriting.', process_output)