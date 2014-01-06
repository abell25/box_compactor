import os
import csv
import math
import time
import sys
import Layer

SLEIGH_LEN = 1000

# flipper
def flipSortedPresents(sortedPresents, C):
  # z_i -> mz - z_i
  # i am changing 1 to a 0
  for i in range(0,len(sortedPresents)):
    for j in range(1,25):
      if j%3 == 0:
        sortedPresents[i][j] = C['mz'] - sortedPresents[i][j] + 1

def naivePackPresent(present, C):
  id, px, py, pz = present
  x, y, z, mx, my, mz = C['x'], C['y'], C['z'], C['mx'], C['my'], C['mz']
  #print "present: ", present
  #print "    coords x =",x,",\ty =",y,",\tz =",z

  if x+px-1 > SLEIGH_LEN:
    x = mx = 1
    y = my+1 ##
  if y+py-1 > SLEIGH_LEN:
    x = mx = y = my = 1
    z = mz+1 ##
  
  #x, y, z now point to where the present will be placed
  x2, y2, z2 = x+px-1, y+py-1, z+pz-1 ##
  mx, my, mz = max(x2,mx), max(y2,my), max(z2,mz)
  
  #print "end coords x2=",x2,",\ty2=",y2,",\tz2=",z2
  #print "new maxes  mx=",mx,",\tmy=",my,",\tmz=",mz   #mx for latest x
  C['x'], C['y'], C['z'], C['mx'], C['my'], C['mz'] = x2+1, y, z, mx, my, mz
  return [x, x2, y, y2, z, z2]

def sortRowsAlgorithm(presents):
  packedPresents = []
  C = {'x':1,'y':1,'z':1,'mx':1,'my':1,'mz':1}
  
  #for p in presents:
  #  placedPresent = naivePackPresent(p, C)
  #  packedPresents.append([p[0]] + vertex_list(*placedPresent))
  i = 0
  z = mz = 1
  layers = []
  while i < len(presents):
    layer = Layer.Layer(z, SLEIGH_LEN)
    [rows, mz, i] = layer.makeLayer(presents, i)
    z = mz+1
    layers.append(layer)
    #print "there are now ", len(layers), " layer!"
  for layer in layers:
    packedPresents += layer.getCoords()

  print "number of packedPresents = ", len(packedPresents)

  print "Flipping the presents"
  print "present[0] is ", packedPresents[0]
  C['mz'] = mz+1
  flipSortedPresents(packedPresents, C)
  print "Presents flipped"
  return packedPresents

def naiveAlgorithm(presents):
  packedPresents = []
  C = {'x':1,'y':1,'z':1,'mx':1,'my':1,'mz':1}
  for p in presents:
    placedPresent = naivePackPresent(p, C)
    packedPresents.append([p[0]] + vertex_list(*placedPresent))
  
  print "Flipping the presents"
  flipSortedPresents(packedPresents, C)
  print "Presents flipped"
  return packedPresents

def vertex_list(x1, x2, y1, y2, z1, z2):
    list_vertices = [x1, y1, z1]
    list_vertices += [x1, y2, z1]
    list_vertices += [x2, y1, z1]
    list_vertices += [x2, y2, z1]
    list_vertices += [x1, y1, z2]
    list_vertices += [x1, y2, z2]
    list_vertices += [x2, y1, z2]
    list_vertices += [x2, y2, z2]
    return list_vertices 

def packPresents(presents):
  #packedPresents = naiveAlgorithm(presents)
  packedPresents = sortRowsAlgorithm(presents)
  return packedPresents


if __name__ == "__main__":
  start = time.clock()

  header = ['PresentId']
  for i in range(1,9):
      header += ['x' + str(i), 'y' + str(i), 'z' + str(i)]

  presentsFile = csv.reader(open('data/' + sys.argv[1], 'r'))
  submissionFile = csv.writer(open('data/submission.csv', 'w'))
  
  presentsFile.next()
  presents = [[int(i) for i in p] for p in presentsFile]
  print "data loaded into memory.."
  packedPresents = packPresents(presents)
  print "packing algorithm complete!"

  submissionFile.writerow(header)
  for p in packedPresents:
    submissionFile.writerow(p)

  print "************** All done ! *******************"
  print "Total time: ", str(time.clock() - start)
