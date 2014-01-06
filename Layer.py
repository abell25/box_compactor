import Row

class Layer:
  def __init__(self, z, SLEIGH_LEN):
    self.rows = []
    self.packagesUsed = []
    self.z = z
    self.SLEIGH_LEN = SLEIGH_LEN  

  def makeLayer(self, presents, i): #i is index of current present
    rows = []
    x = y = my = mz = 1
    row_num = 0
    while i < len(presents) and y < self.SLEIGH_LEN:
      [new_row, my, i, mz]= self.makeRow(presents, i, y, mz)
      row = Row.Row(new_row, x, y, self.z)
      rows.append(row)
      y = my+1

    #print "****************** Layer has ", len(rows), " rows! ************************" 
    self.squishRows(rows) #TODO: sort as triangles and try to "push" them together
    self.rows = rows
    self.mz = mz
    self.i = i
    return [rows, mz, i]

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
      if id == 20:
        print "at present 20"
        print "x = {0}, y = {1}, z = {2}".format(x, y, self.z)
        print "px = {1}, py = {2}, pz = {3}".format(*present)
      if y+py-1 > self.SLEIGH_LEN:
        #TODO: we could just try to flip the shape to get a small gain
        return [row, my, i, mz]

      if x+px-1 > self.SLEIGH_LEN:
        return [row, my, i, mz]
      
      i = i+1
      mz = max(mz, self.z+pz-1)
      row.append(present)
      xy_coords.append([x+px-1, y+py])
      my = max(my, y+py-1)
      x = x+px+1
      #print "len(row) = ", len(row), ", mx = ", x, ", my = ", my, ", mz = ", mz, ", i = ", i

    return [row, my, i, mz]

  def getCoords(self):
    #converts the presents in each row to their coords
    coords = []
    for row in self.rows:
      coords += row.getCoords()
    return coords

  def squishRows(self, rows):
    # Assuming every present is where its supposed to be, we are going to
    # Make complimentary triangles and _push_ the rows together
    pass

