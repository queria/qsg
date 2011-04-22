import map
import eco

class QSGame(object):
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

    def players_count(self):
        return len(self.__players)

    def players(self):
        return self.__players

    def print_status(self):
        out = []
        out.append("- Game status: {0} players total".format(len(self.__players)))
        for p in self.__players:
            out.extend(p.print_status())
        out.append("\n")
        return out

