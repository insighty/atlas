"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MockDeployment(object):

    def __init__(self, scheduler_backend_callback):
        self._scheduler_backend_callback = scheduler_backend_callback

    def scheduler_backend(self):
        return self._scheduler_backend_callback