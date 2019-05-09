"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""


class DataFrameParser(object):
    
    def data_frame_for(self, input):
        from pandas import DataFrame

        columns = [field['name'] for field in input['schema']]

        return DataFrame(input['rows'], columns=columns)
