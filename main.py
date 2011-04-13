#!/usr/bin/python
import map
import gui
import eco

#print('hi')
#w = map.World('Testovaci')
#w.test('blah')
#w.add_area(map.Area('Brno'))
#w.add_area(map.Area('Branice', 128, 128))
#w.print_areas()
#brno = w.area_by_name('Brno')
#qu = map.Object('Qu')
#print(qu)
#qu.travel_to(brno,12,34)
#print(qu)
#w.print_areas()

class Game(object):
    def __init__(self):
        self.__players = []

    def new_player(self, name):
        p = eco.Player(name)
        self.__players.append(p)
        return p

    def player_by_name(self, name):
        for p in self.__players:
            if p.name() == name:
                return p
        return None

    def new_factory(self, player, f):
        if not isinstance(f, eco.ResourceFactory):
            raise TypeError('Bad type of factory')
        player.add_factory( f )
        return f

    def print_status(self):
        print("- Game status: {0} players total".format(len(self.__players)))
        for p in self.__players:
            p.print_status()
        print("\n")


g = Game()
gui = gui.Console(g)
gui.run()
