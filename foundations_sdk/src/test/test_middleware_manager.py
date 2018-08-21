"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.middleware_manager import MiddlewareManager
from foundations.basic_stage_middleware import BasicStageMiddleware


class TestMiddlewareManager(unittest.TestCase):

    class MockMiddleware(BasicStageMiddleware):
        pass

    class MockMiddlewareTwo(BasicStageMiddleware):
        pass

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from foundations.stage_config import StageConfig
        from foundations.stage_context import StageContext
        from foundations.stage import Stage
        from foundations.config_manager import ConfigManager

        from uuid import uuid4

        self._pipeline_context = PipelineContext
        self._stage_config = StageConfig
        self._stage_context = StageContext

        self._stage_uuid = str(uuid4())
        self._stage = Stage(None, self._stage_uuid,
                            self._function, self._function)

        self._config_manager = ConfigManager()

    def test_has_redundant_middleware(self):
        from foundations.redundant_execution_middleware import RedundantExecutionMiddleware
        self._test_has_middleware('Redundant', RedundantExecutionMiddleware)

    def test_has_redundant_middleware_configured(self):
        self._test_constructor_attributes('Redundant')

    def test_has_error_middleware(self):
        from foundations.error_middleware import ErrorMiddleware
        self._test_has_middleware('Error', ErrorMiddleware)

    def test_has_error_middleware_configured(self):
        self._test_constructor_attributes('Error')

    def test_has_stage_output_middleware(self):
        from foundations.stage_output_middleware import StageOutputMiddleware
        self._test_has_middleware('StageOutput', StageOutputMiddleware)

    def test_has_stage_output_middleware_configured(self):
        self._test_constructor_attributes('StageOutput')

    def test_has_stage_log_middleware(self):
        from foundations.stage_log_middleware import StageLogMiddleware
        self._test_has_middleware('StageLog', StageLogMiddleware)

    def test_has_stage_log_middleware_configured(self):
        self._test_constructor_attributes('StageLog')

    def test_has_argument_filler_middleware(self):
        from foundations.argument_filler_middleware import ArgumentFillerMiddleware
        self._test_has_middleware('ArgumentFiller', ArgumentFillerMiddleware)

    def test_has_argument_filler_middleware_configured(self):
        self._test_constructor_attributes('ArgumentFiller')

    def test_has_cache_middleware(self):
        from foundations.cache_middleware import CacheMiddleware
        self._test_has_middleware('Cache', CacheMiddleware)

    def test_has_cache_middleware_configured(self):
        self._test_constructor_attributes('Cache')

    def test_has_upstream_result_middleware(self):
        from foundations.upstream_result_middleware import UpstreamResultMiddleware
        self._test_has_middleware('UpstreamResult', UpstreamResultMiddleware)

    def test_has_context_aware_middleware(self):
        from foundations.context_aware_middleware import ContextAwareMiddleware
        self._test_has_middleware('ContextAware', ContextAwareMiddleware)

    def test_has_context_aware_middleware_configured(self):
        self._test_constructor_attributes('ContextAware')

    def test_has_time_stage_middleware(self):
        from foundations.time_stage_middleware import TimeStageMiddleware
        self._test_has_middleware('TimeStage', TimeStageMiddleware)

    def test_has_time_stage_middleware_configured(self):
        self._test_constructor_attributes('TimeStage')

    def test_has_stage_logging_middleware(self):
        from foundations.stage_logging_middleware import StageLoggingMiddleware
        self._test_has_middleware('StageLogging', StageLoggingMiddleware)

    def test_has_stage_logging_middleware_configured(self):
        self._test_constructor_attributes('StageLogging')

    def test_has_configured_middleware(self):
        self._config_manager['stage_middleware'] = [
            {'name': 'Mock', 'constructor': self.MockMiddleware}
        ]
        self._test_has_middleware('Mock', self.MockMiddleware)

    def test_has_configured_middleware_configured(self):
        self._config_manager['stage_middleware'] = [
            {'name': 'Mock', 'constructor': self.MockMiddleware}
        ]
        self._test_constructor_attributes('Mock')

    def test_has_configured_middleware_different_middleware(self):
        self._config_manager['stage_middleware'] = [
            {'name': 'MockTwo', 'constructor': self.MockMiddlewareTwo}
        ]
        self._test_has_middleware('MockTwo', self.MockMiddlewareTwo)

    def _test_constructor_attributes(self, name):
        middleware_manager = MiddlewareManager(self._config_manager)
        middleware = self._construct_middleware(middleware_manager, name)

        # hack for ensuring construction is working
        has_any = False
        for attribute in ['_pipeline_context', '_stage_config', '_stage_context', '_stage']:
            if hasattr(middleware, attribute):
                has_any = True
                expected_result = getattr(self, attribute)
                result = getattr(middleware, attribute)
                self.assertEqual(expected_result, result)
        self.assertTrue(has_any)

    def _test_has_middleware(self, name, middleware_type):
        middleware_manager = MiddlewareManager(self._config_manager)
        middleware = self._construct_middleware(middleware_manager, name)
        self.assertTrue(isinstance(middleware, middleware_type))

    def _function(self):
        pass

    def _construct_middleware(self, middleware_manager, name):
        for middleware in middleware_manager.stage_middleware():
            if middleware.name == name:
                return middleware.callback(self._pipeline_context, self._stage_config, self._stage_context, self._stage)

        return None