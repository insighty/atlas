"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import unittest
from mock import patch
from foundations_rest_api.filters.contains_filter import ContainsFilter

class TestContainsFilter(unittest.TestCase):

    class MockJobInfo(object):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def test_user_contains(self):
        params = {
            'user_contains': 'oven'
        }

        job_users = ['mozart', 'beethoven', 'tchaikovsky']

        result = [self.MockJobInfo(user=job_user) for job_user in job_users]

        contain_filter = ContainsFilter()
        new_result = contain_filter(result, params)

        self.assertEqual(len(new_result), 1)

        new_result_users = [job.user for job in new_result]
        expected_new_result_user = ['beethoven']
        self.assertEqual(expected_new_result_user, new_result_users)
