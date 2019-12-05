"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class RowCountChecker(object):

    def __init__(self, reference_row_count):
        self._number_of_rows = reference_row_count

    def __str__(self):
        import json
        return json.dumps({'number_of_rows': self._number_of_rows})

    def validate(self, dataframe_to_validate):
        row_count_to_check = len(dataframe_to_validate)
        return {
            'expected_row_count': self._number_of_rows,
            'actual_row_count': row_count_to_check,
            'row_count_diff': (row_count_to_check - self._number_of_rows) / self._number_of_rows
        }

    def configure(self, attributes=None, row_count=None):
        if row_count:
            self._number_of_rows = row_count
        # TODO display warning if attributes is not none (unexpected behaviour) - attributes kept for conformance if super-class type structure to be created

    def exclude(self, attributes=None):
        # TODO display warning if attributes is not none (unexpected behaviour) - attributes kept for conformance if super-class type structure to be created
        pass