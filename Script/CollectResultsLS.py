import math
import os
import sys

repeat_times = 30

epsilons = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
queries = ["Q3", "Q12", "Q20"]
scales = ["_3"]

GS = 1000000.0

def main(argv):
	for query in queries:
		for scale in scales:
			for epsilon in epsilons:
				sum_time = 0
				errors = []

				cur_path = os.getcwd()
				cmd = cur_path + "/../../jr_python " + cur_path + "/../Code/LS.py -I " + cur_path + "/../Information/TPCH/" + query + scale + ".txt -e " + str(epsilon) + " -G " + str(int(GS))

				for i in range(repeat_times):
					shell = os.popen(cmd, 'r')
					res = shell.read()
					res = res.split()

					a = float(res[2])
					b = float(res[5])
					c = float(res[7])
		
					errors.append(abs(a - b))
					sum_time += c

				errors.sort()

				print(query, scale, epsilon, GS, sum(errors[6 : 24]) / 18, sum_time/repeat_times, flush=True)

if __name__ == "__main__":
		main(sys.argv[1:])