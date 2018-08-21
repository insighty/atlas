"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.stage_connector_wrapper_builder import StageConnectorWrapperBuilder


class TestStageConnectorWrapper(unittest.TestCase):

    def setUp(self):
        from foundations.stage_graph import StageGraph
        from foundations.pipeline_context import PipelineContext

        self._graph = StageGraph()
        self._pipeline_context = PipelineContext()

    def test_stage_generates_uuid(self):
        def method():
            pass

        builder = StageConnectorWrapperBuilder(self._graph, self._pipeline_context)
        builder.stage('start', method, (), {})
        stage = builder.build(self._make_stage)
        self.assertEqual('6ab26d5d22e1506907576a678c93b314895978f7', stage.uuid())

    def test_stage_generates_uuid_different_code(self):
        def method():
            return 5

        builder = StageConnectorWrapperBuilder(self._graph, self._pipeline_context)
        builder.stage('start', method, (), {})
        stage = builder.build(self._make_stage)
        self.assertEqual('fac6b50108007d3832429951f9563903cf061298', stage.uuid())

    def test_stage_generates_uuid_different_method(self):
        builder = StageConnectorWrapperBuilder(self._graph, self._pipeline_context)
        builder.stage('start', self._method_two, (), {})
        stage = builder.build(self._make_stage)
        self.assertEqual('95333fba530a08675c0a2b0c41b00ee04c5d2f85', stage.uuid())

    def test_stage_generates_uuid_different_parent(self):
        builder = StageConnectorWrapperBuilder(self._graph, self._pipeline_context)
        builder.stage('somewhere in the middle', self._method_two, (), {})
        stage = builder.build(self._make_stage)
        self.assertEqual('0d93f32a7c95768e99aaf10bf0c82322a4e69c7a', stage.uuid())

    def _method(self):
        pass

    def _method_two(self):
        pass

    def _make_stage(self, stage):
        from foundations.stage_connector import StageConnector
        return StageConnector(stage, [])