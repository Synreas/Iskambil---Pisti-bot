from GameLib import *

GC = GameController(0.5, 2)

GC.set_player()
GC.set_bot()
GC.set_table()

for r in range(1,7):
	GC.play_a_round()

GC.calculate_points()
input()