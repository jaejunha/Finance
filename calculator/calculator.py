import sys

NUM_ARGS = 5

CONST_FEE = 0.3

if __name__=="__main__":
	if len(sys.argv) != NUM_ARGS:
		print("alert! please run program with argument (Gain Cut, Loss Cut, Count, Unit of Probability)")
		print("example) calculator.py 3 2 20 5")
		sys.exit()

	cut_gain = float(sys.argv[1])
	cut_loss = float(sys.argv[2])
	cnt_total = int(sys.argv[3])
	unit_pro = int(sys.argv[4])

	unit = 0
	while unit <= 100:
		sum_rate = 1.0
		cnt_win = int(cnt_total * unit / 100.0)
		cnt_loss = cnt_total - cnt_win
		sum_rate = sum_rate * ((1 + (cut_gain - CONST_FEE)/100.0) ** cnt_win)
		sum_rate = sum_rate * ((1 - (cut_loss + CONST_FEE)/100.0) ** cnt_loss)
		sum_rate *= 100
		sum_rate -= 100

		print("Pr: %3d%%\tProfit:%3.2f%%" % (unit, sum_rate))
		unit += unit_pro