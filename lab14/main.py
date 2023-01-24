class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

def orientation(a, b, c):
    res = (b.y - a.y) * (c.x - b.x) - (c.y - b.y) * (b.x - a.x)
    if res == 0:
        return 0 #wspolliniowe
    elif res > 0:
        return -1 #prawoskretne
    elif res < 0:
        return 1 #lewoskretne

def between(a, b, c):
    if a.x == b.x == c.x:
        if b.y >= a.y and b.y <= c.y or b.y <= a.y and b.y >= c.y:
            return True
    elif a.y == b.y == c.y:
        if b.x >= a.x and b.x <= c.x or b.x <= a.x and b.x >= c.x:
            return True
        

def Jarvis(points, n):
    res = []
    start = 0
    for point_inx in range(n):
        if points[point_inx].x < points[start].x:
            start = point_inx
        elif points[point_inx].x == points[start].x and points[point_inx].y < points[start].y:
            start = point_inx
            
    current_point = start
    res.append(points[current_point])
    while True:
        q = (current_point + 1) % n
        for point_inx in range(n):
            criterion = orientation(points[current_point], points[q], points[point_inx])
            if criterion == -1:
                q = point_inx
            if criterion == 0 and between(points[current_point], points[q], points[point_inx]):
                q = point_inx
        current_point = q
        res.append(points[current_point])
        if q == start:
            return res

def test(data):
    lst = []
    for element in data:
        lst.append(Point(element[0],element[1]))
    print(Jarvis(lst, len(lst)))

test1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
test2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
test3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]

test(test1)
test(test2)
test(test3)