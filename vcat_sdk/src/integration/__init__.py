"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from uuid import uuid4
import vcat
from integration.test_pipeline_interface import TestPipelineInterface
from integration.test_run_stages import TestRunStages
from integration.test_placeholder_parameters import TestPlaceHolderParameters
from integration.test_caching import TestCaching

vcat.config_manager['cache_implementation'] = {
    'cache_type': vcat.LocalFileSystemCacheBackend,
    'constructor_arguments': ['/tmp/vcat_example_' + str(uuid4())],
}
