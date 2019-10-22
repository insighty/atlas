"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit.contract_validators.min_max_checker import MinMaxChecker

class TestMinMax(Spec):

    @let
    def column_name(self):
        return self.faker.word()

    @let
    def column_name_two(self):
        return self.faker.word()

    @let_now
    def dataframe_one_column(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name], data=[20, 40, 50, 100, 110])

    @let_now
    def dataframe_two_columns(self):
        import pandas
        return pandas.DataFrame(columns=[self.column_name, self.column_name_two], data=[[20, 0], [40, 4], [50, 10], [100, 40], [110, 99]])
    
    @let_now
    def dataframe_one_column_with_datetime(self):
        import datetime
        import pandas

        return pandas.DataFrame(columns=[self.column_name], data=[datetime.datetime(2020,2,16), datetime.datetime(2018,2,16), datetime.datetime(2019,2,16)])

    def test_min_max_test_returns_empty_dictionary_when_checker_not_configured(self):
        min_max_checker = MinMaxChecker()
        result = min_max_checker.validate(self.dataframe_one_column)
        self.assertEqual({}, result)
    
    def test_min_max_test_raises_value_error_if_bounds_not_passed_and_attributes_empty(self):
        min_max_checker = MinMaxChecker()

        with self.assertRaises(ValueError) as error_context:
            min_max_checker.configure(attributes=[])

    def test_min_max_test_raises_value_error_if_bounds_not_passed(self):
        min_max_checker = MinMaxChecker()

        with self.assertRaises(ValueError) as error_context:
            min_max_checker.configure(attributes=['abc'])
    
    def test_min_max_test_passes_when_lower_bound_provided(self):
        lower_bound = self.faker.random.randint(0, self.dataframe_one_column[self.column_name].min() - 1)
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': 20
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_fails_when_lower_bound_provided_greater_than_min_value(self):
        lower_bound = 30
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': False,
                    'min_value': 20,
                    'percentage_out_of_bounds': 0.2
                }
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_passes_when_upper_bound_provided(self):
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()
        upper_bound = self.faker.random.randint(max_val_of_dataframe + 1, max_val_of_dataframe + 100)
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_of_dataframe
                }
            }
        }

        self.assertEqual(expected_result, result)

    
    def test_min_max_test_returns_empty_dict_with_empty_dataframe(self):
        import pandas

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], upper_bound=self.faker.random.randint(0,10))
        result = min_max_checker.validate(pandas.DataFrame())

        expected_result = {}

        self.assertEqual(expected_result, result)

    def test_min_max_test_fails_when_upper_bound_provided_lesser_than_max_value(self):
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()
        upper_bound = max_val_of_dataframe - 1
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': False,
                    'max_value': max_val_of_dataframe,
                    'percentage_out_of_bounds': 0.2
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_runs_both_min_and_max_test_on_one_column_when_upper_bound_and_lower_bound_provided(self):
        min_val_of_dataframe = self.dataframe_one_column[self.column_name].min()
        max_val_of_dataframe = self.dataframe_one_column[self.column_name].max()

        lower_bound = self.faker.random.randint(0, min_val_of_dataframe - 1)
        upper_bound = self.faker.random.randint(max_val_of_dataframe + 1, max_val_of_dataframe + 100)

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound, upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_one_column)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_of_dataframe,
                },
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_of_dataframe,
                }
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_runs_min_test_and_passes_on_two_columns(self):
        min_val_one = self.dataframe_two_columns[self.column_name].min()
        min_val_two = self.dataframe_two_columns[self.column_name_two].min()

        min_val_of_dataframes = min(min_val_one, min_val_two)
        lower_bound = min_val_of_dataframes - 1

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=lower_bound)
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_one,
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_runs_max_test_and_passes_on_two_columns(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()
        max_val_two = self.dataframe_two_columns[self.column_name_two].max()

        max_val_of_dataframes = max(max_val_one, max_val_two)
        upper_bound = max_val_of_dataframes + 1

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], upper_bound=upper_bound)
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
            self.column_name_two: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_with_multiple_configure_statements_returns_expected_data(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()
        min_val_two = self.dataframe_two_columns[self.column_name_two].min()

        upper_bound = max_val_one + 1
        lower_bound = min_val_two - 1

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=lower_bound)
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': True,
                    'min_value': min_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_with_configure_on_same_column_twice_overwrites_test(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()

        upper_bound = max_val_one + 1

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=100)
        min_max_checker.configure(attributes=[self.column_name], upper_bound=upper_bound)
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
        }

        self.assertEqual(expected_result, result)

    def test_min_max_test_with_both_max_and_min_tests_on_two_columns(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()
        max_val_two = self.dataframe_two_columns[self.column_name_two].max()
        min_val_one = self.dataframe_two_columns[self.column_name].min()
        min_val_two = self.dataframe_two_columns[self.column_name_two].min()

        upper_bound_one = max_val_one + 1
        lower_bound_one = min_val_one - 1
        upper_bound_two = max_val_two + 1
        lower_bound_two = min_val_two - 1

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound_one, upper_bound=upper_bound_one)
        min_max_checker.configure(attributes=[self.column_name_two], lower_bound=lower_bound_two, upper_bound=upper_bound_two)
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound_one,
                    'passed': True,
                    'min_value': min_val_one,
                },
                'max_test': {
                    'upper_bound': upper_bound_one,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
            self.column_name_two: {
                'min_test': {
                    'lower_bound': lower_bound_two,
                    'passed': True,
                    'min_value': min_val_two,
                },
                'max_test': {
                    'upper_bound': upper_bound_two,
                    'passed': True,
                    'max_value': max_val_two,
                },
            }
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_excluding_all_columns(self):
        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], lower_bound=0)
        min_max_checker.exclude(attributes='all')
        
        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {}

        self.assertEqual(expected_result, result)

    def test_min_max_test_excluding_one_column(self):
        max_val_one = self.dataframe_two_columns[self.column_name].max()

        upper_bound = max_val_one + 1

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name, self.column_name_two], upper_bound=upper_bound)
        min_max_checker.exclude([self.column_name_two])

        result = min_max_checker.validate(self.dataframe_two_columns)

        expected_result = {
            self.column_name: {
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                },
            },
        }

        self.assertEqual(expected_result, result)
    
    def test_min_max_test_with_one_column_datetime(self):
        import datetime
        max_val_one = self.dataframe_one_column_with_datetime[self.column_name].max()
        min_val_one = self.dataframe_one_column_with_datetime[self.column_name].min() 

        upper_bound = max_val_one + datetime.timedelta(days=1)
        lower_bound = min_val_one + datetime.timedelta(days=1)

        min_max_checker = MinMaxChecker()
        min_max_checker.configure(attributes=[self.column_name], lower_bound=lower_bound, upper_bound=upper_bound)
        
        result = min_max_checker.validate(self.dataframe_one_column_with_datetime)

        expected_result = {
            self.column_name: {
                'min_test': {
                    'lower_bound': lower_bound,
                    'passed': False,
                    'min_value': min_val_one,
                    'percentage_out_of_bounds': 0.333
                },
                'max_test': {
                    'upper_bound': upper_bound,
                    'passed': True,
                    'max_value': max_val_one,
                }
            }
        }

        self.assertEqual(expected_result, result)