"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def _load_data_stage(file_location):
    from foundations_production.serving.data_from_file import data_from_file
    return data_from_file(file_location)

def create_retraining_job(model_package_id, features_location, targets_location):
    import foundations

    data_from_file_stage = foundations.create_stage(_load_data_stage)

    return data_from_file_stage(features_location)