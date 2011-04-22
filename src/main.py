#!/usr/bin/python
import getopt
import sys
import game


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

def usage():
    print("QSGame starter")
    print('')
    print('Defaults to console/command-line client.')
    print('Use [-w | --web] to start webserver for simple')
    print(' http interface.')

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hw', ['help', 'web'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    web = False
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-w', '--web'):
            web = True
    g = game.QSGame()
    gui = None
    if web:
        from gui.web import WebGui
        gui = WebGui(g)
    else:
        from gui.console import ConsoleGui
        gui = ConsoleGui(g)
    gui.run()

if __name__ == '__main__':
    main()

