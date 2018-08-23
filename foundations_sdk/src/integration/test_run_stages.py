"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations import *

class TestRunStages(unittest.TestCase):

    def test_can_run_single_stage(self):
        def method():
            return 5
        stage = pipeline.stage(method)
        self.assertEqual(5, stage.run_same_process())

    def test_can_run_single_stage_with_complex_return(self):
        def method():
            return {'hello': 125, 'world': 555}
        stage = pipeline.stage(method)
        self.assertEqual({'hello': 125, 'world': 555}, stage.run_same_process())

    def test_ignores_metrics(self):
        def method():
            return 17, {'hello': 125, 'world': 555}
        stage = pipeline.stage(method)
        self.assertEqual(17, stage.run_same_process())

    def test_can_take_input(self):
        def method(value):
            return value
        stage = pipeline.stage(method, 9)
        self.assertEqual(9, stage.run_same_process())

    def test_can_link_stages(self):
        def make_value(value):
            return value

        def double_value(value):
            return value * 2

        stage = pipeline.stage(make_value, 3).stage(double_value)
        self.assertEqual(6, stage.run_same_process())

    def test_can_link_stages_through_params(self):
        def make_value(value):
            return value

        def double_value(value):
            return value * 2

        stage = pipeline.stage(make_value, 7)
        stage2 = pipeline.stage(double_value, stage)
        self.assertEqual(14, stage2.run_same_process())

    def test_can_run_method_on_stage(self):
        def method():
            return 'hello'

        stage = pipeline.stage(method).replace('l', 'p')
        self.assertEqual('heppo', stage.run_same_process())

    def test_can_pass_list_as_constant_arg(self):
        elems = pipeline.stage(len, [1, 2, 3, 4, 5])
        self.assertEqual(5, elems.run_same_process())