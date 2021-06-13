import math
import os
import sys

repeat_times = 10
'''
epsilons = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8]
graphs = ["network4", "network10", "network16", "network17", "network19"]
ks = ["one_path", "triangle", "two_path", "rectangle"]
'''

epsilons = [12.8]
graphs = ["network16"]
ks = ["one_path"]

def main(argv):
	for graph in graphs:
		if graph == "network4":
			thetas = [1024.0, 512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0, 4.0, 2.0]
		elif graph == "network10":
			thetas = [512.0, 256.0, 128.0, 64.0, 32.0, 16.0, 8.0]
		elif graph == "network19":
			thetas = [512.0, 256.0, 128.0, 64.0, 32.0]
		else:
			thetas = [16.0, 8.0, 4.0, 2.0]

		for i in range(len(ks)):
			k = ks[i]
			real_ans = 0

			for epsilon in epsilons:
				results = []

				for theta in thetas:
					sum_time = 0
					errors = []

					cur_path = os.getcwd()
					cmd = cur_path + "/../../dw_python " + cur_path + "/../Code/SDE.py -I " + cur_path + "/../Information/Graph/one_path/" + graph + ".txt -e " + str(epsilon) + " -t " + str(int(theta)) + " -k " + str(i) + " -D " + graph + "_sde"

					for j in range(repeat_times):
						print(j, flush=True)
						
						shell = os.popen(cmd, 'r')
						res = shell.read()
						res = res.split()

						if (graph == "network4" and theta == 1024.0) or (graph == "network10" and theta == 512.0) or (graph == "network16" and theta == 16.0) or (graph == "network17" and theta == 16.0) or (graph == "network19" and theta == 512.0):
							real_ans = float(res[2])

						b = float(res[5])
						c = float(res[7])
		
						errors.append(abs(real_ans - b))
						sum_time += c

					errors.sort()

					print(graph, k, epsilon, theta, real_ans, sum(errors[2 : 8]) / 6, sum_time/repeat_times, flush=True)

					results.append((theta, sum(errors[2 : 8]) / 6, sum_time/repeat_times))

				sorted_results = sorted(results, key=lambda tup: tup[0])
				l = len(sorted_results)

				if l % 2 == 0:
					print(graph, k, epsilon, real_ans, (sorted_results[int(l/2)][1] + sorted_results[int(l/2 - 1)][1]) / 2, (sorted_results[int(l/2)][2] + sorted_results[int(l/2 - 1)][2]) / 2, flush = True)
				else:
					print(graph, k, epsilon, real_ans, sorted_results[int((l-1)/2)][1], sorted_results[int((l-1)/2)][2], flush = True)

if __name__ == "__main__":
	main(sys.argv[1:])