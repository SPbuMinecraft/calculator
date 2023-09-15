from inspect import getmembers, isfunction

import calculation_test
import parsing_test


for name, test in getmembers(calculation_test, isfunction):
    if name != 'safe_eval':
        test()
for name, test in getmembers(parsing_test, isfunction):
    if name != 'safe_eval':
        test()
