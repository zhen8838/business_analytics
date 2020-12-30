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
  # 清楚多余的表头或者表尾
  if df2[0] == '':
    df2.pop(0)
  if df2[-1] == '':
    df2.pop(-1)
  # 判断是否为有用信息，如果不是则为null
  if len(df2) > 0:
    if df2[0] != 'degree':
      df2.clear()
      res[0].append(None)
      res[1].append(None)
      return res
    if 'Most Popular' in df2:
      # if 'institution' in df2:
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


def process_board_memberships(stream: str):

  def put_by_cycle(res: list, v: list, cycle: int = 3):
    for i, s in enumerate(v):
      # if s in ['Education', 'degree', 'institution']:
      #   return
      res[i % cycle].append(s)

  res = [[], [], []]
  v = stream.split('||')
  if len(v) > 1:
    v.pop(0)
    v.pop(-1)
    assert v[0] == 'title'
    v: list = v[3:]  # remove 'title','company','tenure',
    try:
      # Most Popular后面也需要删除
      e = v.index('Most Popular')
      v = v[:e]
    except ValueError as e:
      pass
    if v[-1] == 'View More':
      v.pop(-1)
    if 'View More' not in v:
      try:
        # 可能没有View More,但存在Other Memberships
        e = v.index('Other Memberships')
        put_by_cycle(res, v[:e], 3)
        put_by_cycle(res, v[e + 3:], 2)
      except ValueError as e:
        pass
      put_by_cycle(res, v, 3)
    else:
      e = v.index('View More')
      put_by_cycle(res, v[:e], 3)
      # remove Other Memberships,title,company
      put_by_cycle(res, v[e + 4:], 2)

  mlen = max(1, max([len(r) for r in res]))
  [r.extend([None] * (mlen - len(r))) for r in res]
  return res
