"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.set_searcher import SetSearcher

class SetGridSearcher(SetSearcher):
    def __init__(self, params_range_dict, max_iterations):
        params_set_generator = SetGridSearcher._create_grid_search_params_set_generator(params_range_dict)
        super(SetGridSearcher, self).__init__(params_set_generator, max_iterations)

    @staticmethod
    def _create_grid_search_params_set_generator(params_range_dict):
        import itertools

        keys = list(params_range_dict.keys())
        keys.sort()
        params_grid_elements = list(map(lambda key: params_range_dict[key].grid_elements(), keys))

        if params_grid_elements != []:
            params_cartesian_product = itertools.product(*params_grid_elements)

            for params_tuple in params_cartesian_product:
                yield {key: param for key, param in zip(keys, params_tuple)}