import os
import sys
sys.path.insert(0, os.getcwd())
from tools.calcfucs import calc_ols

calc_ols('sample_CEO')
calc_ols('sample_CFO')
calc_ols('sample_Chairman')
calc_ols('sample_President')
calc_ols('sample_VP')
        