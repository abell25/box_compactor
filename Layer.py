class Layer:
  def __init__(self, z, SLEIGH_LEN):
    self.rows = []
    self.presentsUsed = [] # of form [[id px py pz] x y z]
    self.z = z
    self.SLEIGH_LEN = SLEIGH_LEN  

  def makeLayer(self, presents, i): #i is index of current present
    x = y = my = mz = 1
    row_num = 0
    i_init = i
    while i < len(presents) and y < self.SLEIGH_LEN:
      [new_row, my, i, mz]= self.makeRow(presents, i, y, mz)
      row_num += 1
      y = my+1
      self.presentsUsed += new_row
        

    #print "******* Layer has ", len(rows), " rows! *********" 
    self.mz = mz
    self.i = i
    return [self.rows, mz, i]

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

  def getCoords(self):
    #converts the presents in each row to their coords
    #return self.coords
    coords = []
    for placedPresent in self.presentsUsed:
      coords.append(self.getPresentCoords(placedPresent))
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
