class Layer:
  def __init__(self, z, SLEIGH_LEN):
    self.packedPresents = [] # of form [[id px py pz] x y z]
    self.z = z
    self.SLEIGH_LEN = SLEIGH_LEN  

  def makeLayer(self, presents, i): #i is index of current present
    self.i = i
    x = y = my = lz = 1
    [new_i, lz, packedPresents] = self.doPackingAlgorithm(presents, i)

    self.mz = mz = lz + self.z
    self.packedPresents = packedPresents
    return [mz, new_i]

  def makeRow(self, presents, i, y, mz):
    x=1
    my = y+1
    row = []
    id, px, py, pz = presents[i]
    xy_coords = [[1, y+py]]

    while i < len(presents):
      present = presents[i]
      #i = i+1
      id, px, py, pz = present
      
      if y+py-1 > self.SLEIGH_LEN:
        #TODO: we could just try to flip the shape to get a small gain
        return [row, my, i, mz]

      if x+px-1 > self.SLEIGH_LEN:
        return [row, my, i, mz]
      
      i = i+1
      mz = max(mz, self.z+pz-1)
      row.append([present, x, y, self.z])
      xy_coords.append([x+px-1, y+py])
      my = max(my, y+py-1)
      x = x+px+1

    return [row, my, i, mz]

  #present:       [id px py pz]
  #packedPresent [[id px py pz] x y z]
  def doPackingAlgorithm(self, presents, i):
    packedPresents = []
    [new_i, lz, latestPackedPresents] = self.selfFirstFit(presents, i)
    if new_i - i > len(packedPresents):
      packedPresents = latestPackedPresents
    return [new_i, lz, packedPresents]

  def selfFirstFit(self, presents, i):
    closedShelves = [] # [x, end_x, y, end_y]
    packedPresents = []
    x = y = mx = my = lz = 1
    while i < len(presents):
      present = presents[i]
      id, px, py, pz = present

      used_closed_shelf = False
      for shelf in closedShelves:
        cx, cmx, cy, cmy = shelf
        if cmx-cx-1 > px and cmy-cy-1 > py:
          #print "dx: {0}-{1}, dy: {2}-{3}".format(cx, cmx, cy, cmy)
          used_closed_shelf = True
          packedPresents.append([present, cx, cy, self.z])
          shelf[0] = cx+px
      
      if used_closed_shelf:
        lz = max(lz, pz-1)
        i = i+1
        continue

      if x+px-1 > self.SLEIGH_LEN:
        closedShelves.append([x, self.SLEIGH_LEN, y, my])
        x = mx = 1
        y = my+1
      if y+py-1 > self.SLEIGH_LEN:
        return [i, lz, packedPresents]
        closedShelves.append([x, self.SLEIGH_LEN, y, self.SLEIGH_LEN])
      i = i+1
      lz = max(lz, pz-1)
      packedPresents.append([present, x, y, self.z])
      my = max(my, y+py-1)
      #print "x = {0}, x' = {1}, px = {2}".format(x, x+px-1, px)
      x = x+px

    return [i, lz, packedPresents]

# Returns the coordinates of the packedPresents
  def getCoords(self):
    #converts the presents in each row to their coords
    #return self.coords
    coords = []
    for packedPresent in self.packedPresents:
      coords.append(self.getPresentCoords(packedPresent))
    return coords

  def getPresentCoords(self, placedPresent):
    present, x1, y1, z1 = placedPresent
    id, px, py, pz = present
    x2, y2, z2 = x1+px-1, y1+py-1, z1+pz-1
    return [id] + self.vertex_list(x1, x2, y1, y2, z1, z2)

  def vertex_list(self, x1, x2, y1, y2, z1, z2):
    list_vertices = [x1, y1, z1]
    list_vertices += [x1, y2, z1]
    list_vertices += [x2, y1, z1]
    list_vertices += [x2, y2, z1]
    list_vertices += [x1, y1, z2]
    list_vertices += [x1, y2, z2]
    list_vertices += [x2, y1, z2]
    list_vertices += [x2, y2, z2]
    return list_vertices    
