import time

class ResourceKind(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self):
        return self.name

class Resource(object):
    FOOD = ResourceKind(0, 'FOOD')
    WOOD = ResourceKind(1, 'WOOD')
    STONE = ResourceKind(2, 'STONE')

    def __init__(self, amount, resource_kind):
        self.amount = float(amount)
        if not isinstance(resource_kind, ResourceKind):
            raise TypeError('Unknown resource')
        self.kind = resource_kind

    def __str__(self):
        return "{0}*{1}".format(
                self.amount,
                self.kind
                )


### RESOURCE FACTORIES
class ResourceFactory(object):
    def __init__(self):
        self.__income = []

    def add_income(self, resource):
        self.__income.append(resource)

    def resources_per_second(self):
        return self.__income

    def print_status(self):
        return ["--- " + self.__class__.__name__
                + ", ".join([ str(res) for res in self.resources_per_second() ]
                    )]

class FoodFactory(ResourceFactory):
    def __init__(self):
        super(FoodFactory, self).__init__()
        self.add_income(Resource(1.2, Resource.FOOD))

class WoodFactory(ResourceFactory):
    def __init__(self):
        super(WoodFactory, self).__init__()
        self.add_income(Resource(1.2, Resource.WOOD))

class StoneFactory(ResourceFactory):
    def __init__(self):
        super(StoneFactory, self).__init__()
        self.add_income(Resource(1.2, Resource.STONE))


### REST
class EconomyStatus(object):
    def __init__(self):
        self.__food = 0
        self.__wood = 0
        self.__stone = 0

    def change(self, resource, time_diff):
        if resource.kind == Resource.FOOD:
            self.__food += resource.amount * time_diff
        elif resource.kind == Resource.WOOD:
            self.__wood += resource.amount * time_diff
        elif resource.kind == Resource.STONE:
            self.__stone += resource.amount * time_diff
        else:
            raise TypeError('Unknown resource')

    def food(self):
        return self.__food

    def wood(self):
        return self.__wood

    def stone(self):
        return self.__stone

    def print_status(self):
        return ["--- Resources: [Food: {0}] [Wood: {1}] [Stone: {2}]".format(
            self.__food,
            self.__wood,
            self.__stone
            )]

class Player(object):
    def __init__(self, name):
        self.__name = name
        self.__storage = EconomyStatus()
        self.__factories = []
        self.__last_rec = time.time()

    def add_factory(self, factory):
        self.recalculate()
        self.__factories.append(factory)

    def name(self):
        return self.__name

    def factories(self):
        return self.__factories

    def recalculate(self):
        now = time.time()
        diff = now - self.__last_rec
        self.__last_rec = now
        for f in self.__factories:
            for res in f.resources_per_second():
                self.__storage.change(res, diff)

    def storage(self):
        self.recalculate()
        return self.__storage

    def print_status(self):
        self.recalculate()
        out = []
        out.append("-- Status of {0}:".format(self.__name))
        out.extend(self.__storage.print_status())
        for f in self.__factories:
            out.extend(f.print_status())
        return out

