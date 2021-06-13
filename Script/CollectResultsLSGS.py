import math
import os
import sys

repeat_times = 20

epsilons = [0.8]
queries = ["Q3", "Q12", "Q20"]
scale = "_3"

def main(argv):
	GS = 10000

	for pow_ in range(8):
		for query in queries:
			for epsilon in epsilons:
				errors = []

				cur_path = os.getcwd()
				cmd = cur_path + "/../../jr_python " + cur_path + "/../Code/LS.py -I " + cur_path + "/../Information/TPCH/" + query + scale + ".txt -e " + str(epsilon) + " -G " + str(int(GS))

				for i in range(repeat_times):
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					a = float(res[2])
					b = float(res[5])
		
					errors.append(abs(a - b))

				errors.sort()

				print(query, scale, epsilon, GS, sum(errors[4 : 16]) / 12, flush=True)

		GS *= 10

if __name__ == "__main__":
	main(sys.argv[1:])