import numpy as np
import pandas as pd
import re
from datetime import datetime
from operator import sub, add


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


def process_education(stream: str, edu_pattern: re.Pattern):
  res = [[], []]
  stream = stream.strip('||')
  if edu_pattern.search(stream) == None:
    l = stream.split('||')
    if l[0] == 'degree':
      s = 1
      try:
        e_pop = l.index('Most Popular')
      except ValueError as e:
        e_pop = len(l)
      try:
        e_pub = l.index('Publications')
      except ValueError as e:
        e_pub = len(l)
      try:
        e_vmore = l.index('View More')
      except ValueError as e:
        e_vmore = len(l)
      e = min(e_pop, e_pub, e_vmore)
      # print(s, e)
      l = l[s + 1:e]
      for i, string in enumerate(l):
        if i % 2 == 0:
          res[0].append(string)
        else:
          res[1].append(string)
  maxlen = max(1, *[len(r) for r in res])
  for r in res:
    while len(r) <= maxlen:
      r.append(None)
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


def tenure_sorter(time_range: list, op=min):
  if len(time_range) == 2:
    s = time_range[0]
    e = time_range[1]
    if isinstance(s, datetime) and isinstance(e, datetime):
      # start_time - end_time
      max_time = op(s, e)
    elif isinstance(s, str) and isinstance(e, datetime):
      # UNKNOW - end_time
      max_time = e
    elif isinstance(s, datetime) and isinstance(e, str):
      # start_time - UNKNOW
      max_time = s
    else:
      # only UNKNOW
      raise ValueError(time_range)
  else:
    if isinstance(time_range[0], datetime):
      max_time = time_range[0]
    else:
      if time_range[0] == 'PRESENT':
        # only PRESENT
        max_time = datetime.now()
      elif time_range[0] == 'FORMER':
        # only FORMER
        max_time = datetime.strptime('01/1900', '%m/%Y')

  return max_time


def find_default(fmtltimes, i, idx, op):
  next_i = op(i, 1)
  try:
    while not isinstance(fmtltimes[next_i][1 if op == add else 0], datetime):
      next_i = op(next_i, 1)
  except IndexError as e:
    pass
  if next_i >= len(fmtltimes):
    fmtltimes[i][idx] = datetime.strptime('01/1900', '%m/%Y')
  elif next_i < 0:
    fmtltimes[i][idx] = datetime.now()
  else:
    if op == add:
      fmtltimes[i][idx] = fmtltimes[next_i][1]
    else:
      fmtltimes[i][idx] = fmtltimes[next_i][0]


def process_tenure(ltimes: list, timepattern):
  if not ltimes[0]:
    return [0], [[None, None]]
  fmtltimes = []
  for times in ltimes:
    fmttime = []
    if times:
      for groups in timepattern.findall(times):
        for i in range(timepattern.groups):
          if groups[i] == '':
            continue
          dtime: datetime
          if i == 0:  # %m/%d/%Y
            dtime = datetime.strptime(groups[i], '%m/%d/%Y')
          elif i == 1:  # %m/%Y
            dtime = datetime.strptime(groups[i], '%m/%Y')
          elif i == 2:  # PRESENT
            dtime = 'PRESENT'
          elif i == 3:  # FORMER
            dtime = 'FORMER'
          elif i == 4:  # UNKNOWN
            dtime = 'UNKNOWN'
          fmttime.append(dtime)
    else:
      fmttime.append('FORMER')

    fmtltimes.append(fmttime)
  # sort by time, and get sorted index
  sort_fmtltimes = sorted(enumerate(fmtltimes), key=lambda x: tenure_sorter(x[1]), reverse=True)
  index, fmtltimes = zip(*sort_fmtltimes)
  fmtltimes = list(fmtltimes)
  # process key word
  for i in range(len(fmtltimes) - 1, -1, -1):
    if len(fmtltimes[i]) == 1:
      # only has PRESENT
      if fmtltimes[i][0] == 'PRESENT':
        fmtltimes[i] = ['UNKNOWN', datetime.now()]
      elif fmtltimes[i][0] == 'FORMER':
        fmtltimes[i] = [datetime.strptime('01/1900', '%m/%Y'), 'UNKNOWN']
      elif isinstance(fmtltimes[i][0], str):
        fmtltimes[i] = [datetime.strptime('01/1900', '%m/%Y'), 'UNKNOWN']
      else:
        # only has time
        if i == 0:
          fmtltimes[i].insert(1, 'PRESENT')
        elif i == len(fmtltimes):
          fmtltimes[i].insert(0, 'FORMER')
        else:
          last = tenure_sorter(fmtltimes[i - 1], min)
          next = tenure_sorter(fmtltimes[i + 1], max)
          diff_last = fmtltimes[i][0] - last
          diff_next = fmtltimes[i][0] - next
          if abs((fmtltimes[i][0] - diff_last).second) < abs((fmtltimes[i][0] - diff_next).second):
            fmtltimes[i].insert(0, next)
          else:
            fmtltimes[i].insert(1, last)

    if 'PRESENT' in fmtltimes[i]:
      fmtltimes[i][fmtltimes[i].index('PRESENT')] = datetime.now()

    if 'FORMER' in fmtltimes[i]:
      fmtltimes[i][fmtltimes[i].index('FORMER')] = datetime.now()

    if 'UNKNOWN' in fmtltimes[i]:
      idx = fmtltimes[i].index('UNKNOWN')
      if idx == 0:
        # UNKNOW - end_time
        find_default(fmtltimes, i, idx, add)
      elif idx == 1:
        # start_time - UNKNOW
        find_default(fmtltimes, i, idx, sub)
  for i in range(len(fmtltimes)):
    for j in range(len(fmtltimes[i])):
      fmtltimes[i][j] = fmtltimes[i][j].strftime('%m/%Y')

  return index, fmtltimes
