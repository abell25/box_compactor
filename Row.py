
class Row:
  def __init__(self, presents, x, y, z):
    self.presents = presents
    self.x = x
    self.y = y
    self.z = z

  def getCoords(self):
    coords = []
    x1, y1, z1 = self.x, self.y, self.z
    
    for present in self.presents:
      id, px, py, pz = present
      x2, y2, z2 = x1+px-1, y1+py-1, z1+pz-1
      if id == 20:
        print "calculating coords of id = {0}".format(id)
        print "x1: {0}, x2: {1}, y1: {2}, y2: {3}, z1: {4}, z2: {5}".format(x1, x2, y1, y2, z1, z2)

      coords.append([id] + self.vertex_list(x1, x2, y1, y2, z1, z2))
      x1 = x2+1

    return coords

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
