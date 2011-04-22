from gui.meta import *

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
        handler.wfile.write('<div>' + output + '</div>')

    def pbr(self, handler, lines):
        self.p(handler, '<br />'.join(lines))

class EconomyStatusView(WebView):
    def __init__(self, ecostatus):
        self.status = ecostatus

    def render(self, handler):
        self.p(handler, ('<div id="ecoStatus">'
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
    def __init__(self, player):
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

#==============================================================================
# - handle different requests:
#     - /player/new/p_name => p_id
#     - /login/p_name/pass_hash
#     - /logout
#     - /factory/new/player_name/factory_type => f_id
#     - /factory/delete/f_id
# - all actions ends with two kinds of result:
#     - whole new rendered html (for static web gameplay)
#     - ajax json response to action (for dynamic js/ajax gameplay)
# - so we have to:
#     - route incoming request to corresponding game actions (events?)
#     - if requested, response with action response wrapped in json
#     - render whole html view of current game status (for current player)
#==============================================================================

