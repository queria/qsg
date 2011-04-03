
class World:
    def __init__(self, name):
        self.name = name
        self.areas = []
        pass

    def add_area(self, area):
        self.areas.append(area)

    def area_by_name(self, area_name):
        for a in self.areas:
            if a.name == area_name:
                return a
        return None

    def print_areas(self):
        print('Total {0} areas:'.format(len(self.areas)))
        for a in self.areas:
            print(" - "+a.full_str())

    def test(self, str):
        print('World test: '+str)

class PositionError(ValueError):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "Invalid coordinates {0}x{1}!".format(self.x, self.y)

class Area:
    
    def __init__(self, name, width=255, height=255):
        self.name = name
        self.width = width
        self.height = height
        self.objects = set()

    def __str__(self):
        return self.name
    def full_str(self):
        return "{0}[{1}x{2}] with {3} objects".format(
                self.name, self.width, self.height,
                len(self.objects))
    def validate(self, x, y):
        if ((x < 0 or y < 0 )
            or x > (self.width-1)
            or y > (self.height-1)):
            raise PositionError(x, y)

    def enter(self, object):
        self.objects.add(object)
    def leave(self, object):
        self.objects.remove(object)

class Object:
    def __init__(self, name):
        self.__name = name
        self.__area = None
        self.__x = 0
        self.__y = 0

    def __str__(self):
        return "{0} at {1}:{2}x{3}".format(
                self.__name,
                str(self.__area),
                self.__x,
                self.__y)

    def area(self):
        return self.__area

    def travel_to(self, area, x, y):
        area.validate(x,y)
        if self.__area:
            self.__area.leave(self)
        self.__area = area
        self.move_to(x,y)
        if self.__area:
            self.__area.enter(self)

    def move_to(self, x, y):
        self.__area.validate(x,y)
        self.__x = x
        self.__y = y


