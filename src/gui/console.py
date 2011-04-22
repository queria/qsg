import gui.meta
import eco

class ConsoleGui(gui.meta.GUI):
    def __init__(self, game):
        self.game = game

    def run(self):
        print("\n\n")
        print("=== QSGame ~ economy draft ===")
        self.main_loop()
        print("==============================")
        print("\n\n")

    def color(self, color):
        if color == 'green':
            return '32'
        elif color == 'yellow':
            return '33'
        return '0'

    def color_start(self, color):
        print('\x1b[{0}m'.format(self.color(color))),
    def color_end(self):
        print('\x1b[0m'),

    def main_loop(self):
        command = ''
        while command != 'q':
            self.color_start('green')
            command = raw_input('[n]ew player, add [f]actory, [p]rint_status, [q]uit: ')
            self.color_end()
            if command == 'p':
                print('\n'.join(self.game.print_status()))
            elif command == 'n':
                self.color_start('yellow')
                name = raw_input(' Player name (empty=cancel): ')
                self.color_end()
                if len(name) != 0:
                    p = self.game.new_player(name)
                    print('\n'.join(p.print_status()))
                else:
                    print(' - canceled')
            elif command == 'f':
                self.color_start('yellow')
                name = raw_input(' Player name (empty=cancel): ')
                self.color_end()
                p = self.game.player_by_name(name)
                if p:
                    self.color_start('yellow')
                    kind = raw_input(' Factory type [food|wood|stone]: ')
                    self.color_end()
                    f = None
                    if kind == 'food':
                        f = eco.FoodFactory()
                    elif kind == 'wood':
                        f = eco.WoodFactory()
                    elif kind == 'stone':
                        f = eco.StoneFactory()
                    if f:
                        self.game.new_factory(p, f)
                        print('\n'.join(f.print_status()))
                    else:
                        print(' - canceled - bad type of factory')
                else:
                    print(' - canceled - player not found')


