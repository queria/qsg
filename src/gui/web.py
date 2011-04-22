from gui.meta import *
import eco

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class WebGui(GUI):

    gw = None

    def __init__(self, game, address='localhost', port='8888'):
        WebGui.gw = QSGameView(game)
        game.new_player('Pepa')
        self.addr = address
        self.port = port
        WebGui.__instance = self

    def run(self):
        try:
            print('Starting server at http://{0}:{1}/'.format(
                self.addr, self.port))
            server = HTTPServer((self.addr, int(self.port)), WebGuiHandler)
            server.serve_forever()
        except KeyboardInterrupt:
            print ' shutting down...'
            server.socket.close()

class WebView(View):
    def __init__(self):
        pass

    def p(self, handler, output):
        handler.wfile.write(output)

    def pd(self, handler, output):
        handler.wfile.write('<div>'+output+'</div>')

    def pbr(self, handler, lines):
        self.p(handler, '<br />'.join(lines))

class EconomyStatusView(WebView):
    def __init__(self,ecostatus):
        self.status = ecostatus

    def render(self, handler):
        self.p(handler,('<div id="ecoStatus">'
            + 'Resources:'
            + ' <span class="ecoRes wood"><span class="count">{0}</span> food</span>'
            + ' <span class="ecoRes wood"><span class="count">{1}</span> wood</span>'
            + ' <span class="ecoRes wood"><span class="count">{2}</span> stone</span>'
            + '</div>').format(
                    self.status.food(),
                    self.status.wood(),
                    self.status.stone()
                    ))

class PlayerView(WebView):
    def __init__(self,player):
        self.player = player

    def render(self, handler):
        self.pd(handler, "-- Status of {0}:".format(self.player.name()))
        EconomyStatusView(self.player.storage()).render(handler)
        for f in self.player.factories():
            EconomyStatusView(f).render(handler)

class QSGameView(WebView):
    def __init__(self, game):
        self.game = game

    def render(self, handler):
        self.pd(handler, "- Game status: {0} players total".format(
            str(self.game.players_count())))
        for p in self.game.players():
            PlayerView(p).render(handler)

    #def new_player(self, handler, name):
    #    self.pbr(handler, self.game.new_player(name).print_status())


class WebGuiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        path = self.path.split('/')
        path = path[1:]
        if path[0] == 'status':
            WebGui.gw.render(self)
        #elif path[0] == 'player':
        #    if path[1] == 'new':
        #        WebGui.gw.new_player(self, path[2])
        else:
            self.wfile.write("Hello world!")

        self.wfile.write('<p>Current request is {0}</p>'.format(self.path))
        self.wfile.write('<p>Current path is {0}</p>'.format(str(path)))
        return

#class Console:
#    def __init__(self, game):
#        self.game = game
#
#    def run(self):
#        print("\n\n")
#        print("=== QSGame ~ economy draft ===")
#        self.main_loop()
#        print("==============================")
#        print("\n\n")
#
#    def color(self,color):
#        if color == 'green':
#            return '32'
#        elif color == 'yellow':
#            return '33'
#        return '0'
#
#    def color_start(self, color):
#        print('\x1b[{0}m'.format(self.color(color))),
#    def color_end(self):
#        print('\x1b[0m'),
#
#    def main_loop(self):
#        command = ''
#        while command != 'q':
#            self.color_start('green')
#            command = raw_input('[n]ew player, add [f]actory, [p]rint_status, [q]uit: ')
#            self.color_end()
#            if command == 'p':
#                self.game.print_status()
#            elif command == 'n':
#                self.color_start('yellow')
#                name = raw_input(' Player name (empty=cancel): ')
#                self.color_end()
#                if len(name) != 0:
#                    p = self.game.new_player(name)
#                    p.print_status()
#                else:
#                    print(' - canceled')
#            elif command == 'f':
#                self.color_start('yellow')
#                name = raw_input(' Player name (empty=cancel): ')
#                self.color_end()
#                p = self.game.player_by_name(name)
#                if p:
#                    self.color_start('yellow')
#                    kind = raw_input(' Factory type [food|wood|stone]: ')
#                    self.color_end()
#                    f = None
#                    if kind == 'food':
#                        f = eco.FoodFactory()
#                    elif kind == 'wood':
#                        f = eco.WoodFactory()
#                    elif kind == 'stone':
#                        f = eco.StoneFactory()
#                    if f:
#                        self.game.new_factory(p, f)
#                        f.print_status()
#                    else:
#                        print(' - canceled - bad type of factory')
#                else:
#                    print(' - canceled - player not found')
#
#
