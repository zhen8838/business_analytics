import pandas as pd
import numpy as np
import pandas as pd
import re


def process_career_history(stream: str, pattern: re.Pattern):
  res = [[], [], []]
  # 清除多余的|
  l = [s.strip('|').rstrip('|') for s in stream.split('||')]
  l = l[1 + 3:]  # 删除表头
  if len(l) > 0:
    # 如果表尾不是空,不删除
    if l[-1] == '':
      l.pop()
    l.reverse()  # 反向遍历
    # 找到最后一个tenure的位置
    end_time_idx = 0
    for s in l:
      if pattern.match(s) != None:
        break
      end_time_idx += 1

    if end_time_idx == len(l):
      # 如果没有tenure,那么就近原则分配
      cnt = len(l) - 1
    else:
      # 删除非tenure的条目
      l = l[end_time_idx:]
      cnt = 2
    for s in l:
      # print(s, pattern.match(s) != None)
      if pattern.match(s):
        cnt = 2
      res[cnt].insert(0, s)
      cnt -= 1
  # padding到相同长度,并且至少要大于1
  maxlen = max(1, max([len(r) for r in res]))
  for r in res:
    while len(r) != maxlen:
      r.append(None)
  return res
