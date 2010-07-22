import random
import csv
import bisect
import threading
import math

population = int(127510000 / 2)
reproductoin_rate = 2.0 / 2.0
generation = 100

slope = -1.80968730264954
intersect = 9.52262501383849

family_count_in_real_statistics = 49063000
family_count_estimation = 29931171
family_count_amplifier = family_count_in_real_statistics / float(family_count_estimation)

reader = csv.reader(open('fn.csv', 'r'))
threads = 1

initial_families = 0
fn = [0]
for row in reader:
  fn.append(fn[-1] + int(int(row[2]) * family_count_amplifier))
  initial_families += 1

while True:
  cnt = int(pow(10, slope * math.log10(initial_families) + intersect) * family_count_amplifier)
  if cnt == 0:
    break
  fn.append(fn[-1] + cnt)
  initial_families += 1

print (initial_families)
def getFamilyName(fn, r):
  return bisect.bisect_left(fn, fn[-1] * r) - 1

def printTitle():
  print ("generation, pop, top 10 share, top 100 share, top 1000 share, top 10000 share, top 100000 share, family name cnt")

def printStatistics(g, fn):
  tmp = {}
  for i in fn:
    tmp[i] = 1
  print ('%d,%d,%f,%f,%f,%f,%f,%d' % (g, population * 2, fn[9] / float(fn[-1]),fn[99] / float(fn[-1]), fn[999] / float(fn[-1]), fn[9999] / float(fn[-1]), fn[99999] / float(fn[-1]), len(tmp.keys()) - 1))
  #tmp.keys has to be minused 1 because fn[-1] is just a summention entry.

class Calc(threading.Thread):
  def __init__(self, fn, rng, population):
    threading.Thread.__init__(self)
    self.fn = fn
    self.rng = rng
    self.population = population
  def run(self):
    self.newfn = []
    for n in self.rng:
      familyName = getFamilyName(self.fn, n / float(self.population))
      while random.random() < (reproductoin_rate / (1 + reproductoin_rate)):
        self.newfn.append(familyName)

printTitle()

for g in range(generation):
  if population == 0:
    print ('popuration == 0')
    exit()
  printStatistics(g, fn)

  newfn = [0 for x in fn]
  thrs = []
  for t in range(threads):
    th = Calc(fn, range(t, population, threads), population)
    th.start()
    thrs.append(th)
  for t in thrs:
    t.join()
    for i in t.newfn:
      newfn[i] += 1

  newfn.sort()
  newfn.reverse()
  fn = [0]
  population = 0
  for i in range(len(newfn)):
    fn.append(fn[-1] + newfn[i])
    population += newfn[i]

