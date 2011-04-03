#!/usr/bin/python3.1
import map

print('hi')
w = map.World('Testovaci')
w.test('blah')
w.add_area(map.Area('Brno'))
w.add_area(map.Area('Branice', 128, 128))
w.print_areas()
brno = w.area_by_name('Brno')
qu = map.Object('Qu')
print(qu)
qu.travel_to(brno,12,34)
print(qu)
w.print_areas()

