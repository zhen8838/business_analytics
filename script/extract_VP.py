import os
import sys
sys.path.insert(0, os.getcwd())
import numpy as np
import re
import pandas as pd
from datetime import datetime
from tools.cleanfucs import maskfuc, work, institution


df1: pd.DataFrame = pd.read_csv('tmp\VP_tenure.csv')#读取职业生涯信息
series1: pd.Series = df1.set_index(['person_id', 'start_tenure', 'end_tenure']).index
person_group1 = df1.groupby('person_id')
promote_time = person_group1.apply(lambda s: maskfuc(s, 'vp'))
work_before = person_group1.apply(lambda s: work(s, 'vp'))
df2: pd.DataFrame = pd.read_csv('tmp\VP_rank.csv')
series2: pd.Series = df2.set_index(['person_id', 'top30', 'top200']).index
person_group2 = df2.groupby('person_id')
top_sch = person_group2.apply(institution)
df3: pd.DataFrame = pd.read_csv('tmp\VP_info.csv')
promote_time = list(promote_time)
work_before = list(work_before)
top_sch = list(top_sch)
c = {"promote_time": promote_time,
     "work_beforeCFO": work_before,
     "top_sch": top_sch}
c = pd.DataFrame(c)
sample = pd.concat([df3, c], axis=1)
sample.to_pickle('tmp/sample_VP.pkl')