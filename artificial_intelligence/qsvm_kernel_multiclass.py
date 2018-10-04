# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from datasets import *
from qiskit_aqua.utils import split_dataset_to_data_and_labels
from qiskit_aqua.input import get_input_instance
from qiskit_aqua import run_algorithm
import numpy as np

n = 2  # dimension of each data point

sample_Total, training_input, test_input, class_labels = Wine(training_size=40,
                                                                     test_size=10, n=n, PLOT_DATA=False)

temp = [test_input[k] for k in test_input]
total_array = np.concatenate(temp)

params = {
            'problem': {'name': 'svm_classification', 'random_seed': 10598},
            'algorithm': {
                'name': 'QSVM.Kernel',
            },
            'backend': {'name': 'qasm_simulator_cpp', 'shots': 1024},
            # 'multiclass_extension': {'name': 'OneAgainstRest'},
            'multiclass_extension': {'name': 'AllPairs'},
            # 'multiclass_extension': {'name': 'ErrorCorrectingCode', 'code_size': 5},
            'feature_map': {'name': 'SecondOrderExpansion', 'depth': 2, 'entangler_map': {0: [1]}}
        }

algo_input = get_input_instance('SVMInput')
algo_input.training_dataset = training_input
algo_input.test_dataset = test_input
algo_input.datapoints = total_array

result = run_algorithm(params, algo_input)
print(result)
