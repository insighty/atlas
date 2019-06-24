"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
from foundations.prototype import set_tag

from model import *

foundations.set_project_name('stageless-projects-nested')
set_tag('model', 'cnn')

def print_words():
    print('Hello World!')

print_words()

addition_result = add(82,2)
set_tag('Loss', addition_result)

subtraction_result = subtract(44,2)
foundations.log_metric('Accuracy', subtraction_result)

cached_subtraction_result = subtract(44,2)
foundations.log_metric('Cached_accuracy', cached_subtraction_result)