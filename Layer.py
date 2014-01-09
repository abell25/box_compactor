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

  def doPackingAlgorithm(self, presents, i):
    packedPresents = []
    [new_i, lz, latestPackedPresents] = self.selfFirstFit(presents, i)
    #[new_i, latestPackedPresents] = self.fillRemainingZSpace(presents, latestPackedPresents, lz, new_i)
    if new_i - i > len(packedPresents):
      packedPresents = latestPackedPresents
      

    return [new_i, lz, packedPresents]

  def fillRemainingZSpace(self, presents, packedPresents, lz, i):
    closedShelves = []
    for p in packedPresents:
      [present, x, y, z] = p
      [id, px, py, pz] = present
      closedShelves.append([x, x+px-1, y, y+py-1, z+pz, z+lz])

    closedShelves.sort(key=lambda c: c[4], reverse=True)

    while i < len(presents):
      present = presents[i]
      id, px, py, pz = present
      [used_space, packedPresent] = self.packPresentInSpaces3D(present, closedShelves)
      if used_space:
        packedPresents.append(packedPresent)
        i = i+1
      else:
        return [i, packedPresents]
    return [i, packedPresents]

  def selfFirstFit(self, presents, i):
    closedShelves = [] # [x, end_x, y, end_y]
    packedPresents = []
    x = y = mx = my = lz = 1
    while i < len(presents):
      [used_closed_shelf, packedPresent] = self.packPresentInSpaces(presents[i], closedShelves)

      if used_closed_shelf:
        pz = packedPresent[0][3]
        packedPresents.append(packedPresent)
        lz = max(lz, pz-1)
        i = i+1
      else:
        present = presents[i]
        id, px, py, pz = present

        if x+px-1 > self.SLEIGH_LEN:
          closedShelves.append([x, self.SLEIGH_LEN, y, my])
          x = mx = 1
          y = my+1
        if y+py-1 > self.SLEIGH_LEN:
          return [i, lz, packedPresents]

        i = i+1
        lz = max(lz, pz-1)
        packedPresents.append([present, x, y, self.z])
        my = max(my, y+py-1)
        x = x+px

    return [i, lz, packedPresents]

  def packPresentInClosed3D(self, closedSpace, present):
    id, px, py, pz = present
    dimens = [px, py, pz]
    configs = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [2, 0, 1], [1, 2, 0], [2, 1, 0]]

    [cx, cmx, cy, cmy, cz, cmz] = closedSpace

    for config in configs:
      px, py, pz = dimens[config[0]], dimens[config[1]], dimens[config[2]], 
        
      if cmx-cx-1 > px and cmy-cy-1 > py and cmz-cz-1 > pz:
        print "z freebee!"
        packedPresent = [[id, px, py, pz], cx, cy, cz]
        shelf = [cx, cmx, cy, cmy, cz, cmz]
        if cmx-cx+px == max([cmx-cx+px, cmy-cy+py, cmy-cy+py]):
          shelf = [cx+px, cmx, cy, cmy, cz, cmz]
        elif cmx-cx+px == max([cmx-cx+px, cmy-cy+py, cmy-cy+py]):
          shelf = [cx, cmx, cy+py, cmy, cz, cmz]
        elif cmx-cx+px == max([cmx-cx+px, cmy-cy+py, cmy-cy+py]):
          shelf = [cx+px, cmx, cy, cmy, cz+pz, cmz]
          
        return [True, packedPresent, shelf]

    return [False, None, None]

  def packPresentInClosed(self, closedSpace, present):
    id, px, py, pz = present
    dimens = [px, py, pz]
    configs = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [2, 0, 1], [1, 2, 0], [2, 1, 0]]
    cx, cmx, cy, cmy = closedSpace

    for config in configs:
      px, py, pz = dimens[config[0]], dimens[config[1]], dimens[config[2]], 
        
      if cmx-cx-1 > px and cmy-cy-1 > py:
        packedPresent = [[id, px, py, pz], cx, cy, self.z]
        shelf = [cx+px, cmx, cy, cmy]
        return [True, packedPresent, shelf]

    return [False, None, None]

  def packPresentInSpaces3D(self, present, closedSpaces):
    used_closed_shelf = False

    for shelf in closedSpaces:
      [used_closed_shelf, packedPresent, closedShelf] = self.packPresentInClosed3D(shelf, present)
      if used_closed_shelf:
        closedSpaces.append(closedShelf)
        closedSpaces.remove(shelf)
      return [used_closed_shelf, packedPresent] 
    
    return [False, None]


  def packPresentInClosed1(self, closedSpace, present):
    id, px, py, pz = present
    configs = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [1, 2, 0], [1, 0, 2]]
    cx, cmx, cy, cmy = closedSpace
      
    if cmx-cx-1 > px and cmy-cy-1 > py:
      packedPresent = [[id, px, py, pz], cx, cy, self.z]
      shelf = [cx+px, cmx, cy, cmy]
      return [True, packedPresent, shelf]
      
    px, py = py, px

    if cmx-cx-1 > px and cmy-cy-1 > py:
      packedPresent = [[id, px, py, pz], cx, cy, self.z]
      shelf = [cx+px, cmx, cy, cmy]
      return [True, packedPresent, shelf]

    return [False, None, None]

  def packPresentInSpaces(self, present, closedSpaces):
    used_closed_shelf = False

    for shelf in closedSpaces:
      [used_closed_shelf, packedPresent, closedShelf] = self.packPresentInClosed(shelf, present)
      if used_closed_shelf:
        shelf[0] = closedShelf[0]
      return [used_closed_shelf, packedPresent] 
    
    return [False, None]


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
