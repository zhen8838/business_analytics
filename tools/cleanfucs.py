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

def process_education(education):
    res = [[], []]
    df2 = education.split('||')
    #清楚多余的表头或者表尾
    if df2[0] == '':
      df2.pop(0)
    if df2[-1] == '':
      df2.pop(-1)
    #判断是否为有用信息，如果不是则为null
    if len(df2) > 0:
      if df2[0] != 'degree':
        df2.clear()
        res[0].append(None)
        res[1].append(None)
        return res
      if 'Most Popular' in df2:
        #if 'institution' in df2:
          s = df2.index('institution')
          e = df2.index('Most Popular')
          d = df2[s + 1:e]
          for j in range(len(d)):
            if j % 2 == 1:
              res[1].append(d[j])
            else:
              res[0].append(d[j])
      else:
        s = df2.index('institution')
        d = df2[s + 1:]
        for j in range(len(d)):
          if j % 2 == 1:
            res[1].append(d[j])
          else:
            res[0].append(d[j])
    return res
    
def process_board_memberships(board):
    res = [[], [], []]
    df2 = board.split('||')
    if df2[0] == '':
      df2.pop(0)
    if df2[-1] == '':
      df2.pop(-1)
    if len(df2) > 0:
      if df2[0] != 'title':
        df2.clear()
        res[0].append(None)
        res[1].append(None)
        res[2].append(None)
        return res
      if 'View More' in df2:
        s = df2.index('View More')
        e = df2.index('tenure')
        d = df2[e + 1:s]
        h = df2[s + 4:]
        for j in range(len(d)):
          if j % 3 == 1:
            res[0].append(d[j])
          elif j % 3 == 2:
            res[2].append(d[j])
          else:
            res[1].append(d[j])
        for m in range(len(h)):
          if m % 2 == 1:
            res[1].append(h[m])
          else:
            res[0].append(h[m])
            res[2].append(None)

      elif 'Other Memberships' in df2 and 'View More' not in df2:
        s = df2.index('tenure')
        e = df2.index('Other Memberships')
        d = df2[s + 1:e]
        h = df2[e + 3:]
        n = len(h) // 2
        for j in range(len(d)):
          if j % 3 == 1:
            res[0].append(d[j])
          elif j % 3 == 2:
            res[2].append(d[j])
          else:
            res[1].append(d[j])
        for m in range(len(h)):
          if m % 2 == 1:
            res[1].append(h[m])
          else:
            res[0].append(h[m])
            res[2].append(None)
      else:
        s = df2.index('tenure')
        d = df2[s + 1:]
        for j in range(len(d)):
          if j % 3 == 1:
            res[0].append(d[j])
          elif j % 3 == 2:
            res[2].append(d[j])
          else:
            res[1].append(d[j])
    return res