# encoding: utf-8
import subprocess
from operator import itemgetter
import re

cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | awk \'{ print NR, $2, $3, $1 }\''
(stdoutdata, stderrdata) = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).communicate()

result = []
for line in stdoutdata.split('\n'):
  # NR, MacAddr, RSSI, Name
  try:
    nr, mac, rssi, name = line.split(' ')
  except:
    continue

  # Mac Address Check
  match = re.search(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$', mac, re.IGNORECASE)
  if match:
    result.append([mac, (int(rssi)+30)*-1, name])
  
# result.sort(key=itemgetter(1))
# print result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def min_max(x, axis=None):
    min = x.min(axis=axis)
    max = x.max(axis=axis)
    result = (x-min)/(max-min)
    return result

result = pd.DataFrame(result, columns=list('ABC'))
seiki = min_max(result['B'])
df = pd.concat([result, seiki], axis=1)
df.columns = list('ABCD')

fig = plt.figure()
ax = plt.axes()

print df
# fc = face color, ec = edge color
colorlist = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', 'b', 'w']
for key, column in df.iteritems():
  if key == 'D':
    for i, v in column.iteritems():
      print i, v
      v = v/7
      x = v*np.random.rand()
      y = v-x
      c = patches.Circle(xy=(x, y), radius=v, ec='b', alpha=0.3, fill=False)
      ax.add_patch(c)


c = patches.Circle(xy=(0, 0), radius=0.001, ec='r', alpha=1, fill=True)
ax.add_patch(c)
plt.axis('scaled')
ax.set_aspect('equal')

plt.show()
