import cplex
import getopt
import math
import numpy as np
import psycopg2
import random
import sys
import time
'''
python SmoothDistanceEstimator.py -I ./edge/network4.txt -e 1 -t 256 -k 0
'''
def ReadInput():
	global input_file_path
	global tuples
	global connections

	size_dic = {}
	id_dic = {}
	id_num = 0

	tuples = []
	connections = []

	input_file = open(input_file_path,'r')

	for line in input_file.readlines():
		elements = line.split()
		connection = []

		for element in elements:
			element = int(element)

			if element in id_dic.keys():
				element = id_dic[element]
			else:
				tuples.append(id_num)
				id_dic[element] = id_num
				element = id_num
				id_num += 1

			if element in size_dic.keys():
				size_dic[element] += 1
			else:
				size_dic[element] = 1

			connection.append(element)

		connections.append(connection)

def RestrictedSensitivity():
	global theta
	global k

	theta_ = 2 * theta

	if k == 0:		# edge
		return theta_
	elif k == 1:	# triangle
		return theta_ * (theta_ - 1) / 2
	elif k == 2:	# rectangle
		return theta_ * (theta_ - 1) * (theta_ - 2) / 2
	elif k == 3:	# two triangle
		return theta_ * (theta_ - 1) * (theta_ - 2)
	elif k == 4:	# two path
		return theta_ * (theta_ - 1) * 3 / 2
	else:
		return 0

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def CauchyCum(x):
	a = 1/4/math.sqrt(2)*(math.log(abs(x**2+math.sqrt(2)*x+1))+2*math.atan(math.sqrt(2)*x+1))
	a += 1/4/math.sqrt(2)*(-math.log(abs(x**2-math.sqrt(2)*x+1))+2*math.atan(math.sqrt(2)*x-1))

	return a

def CauNoise():
	a = random.uniform(0,math.pi/2/math.sqrt(2))

	left = 0
	right = 6000
	mid = (left + right) / 2.0

	while(abs(CauchyCum(mid) - a) > 0.000001):
		if CauchyCum(mid) > a:
			right = mid
		else:
			left = mid
		mid = (left + right) / 2.0

	c = random.uniform(0, 1)

	if c > 0.5:
		return mid
	else:
		return -mid

def LPSolver():
	global theta
	global tuples
	global connections

	num_nodes = len(tuples)
	num_edges = len(connections)

	cpx = cplex.Cplex()
	cpx.objective.set_sense(cpx.objective.sense.minimize)

	obj = np.append(np.ones(num_nodes), np.zeros(num_edges))
	ub = np.append(np.ones(num_nodes), np.ones(num_edges))
	cpx.variables.add(obj=obj, ub=ub)

	rhs = np.append(np.ones(num_nodes) * theta, np.ones(num_edges) * -1)
	senses = "L" * (num_nodes + num_edges)
	cpx.linear_constraints.add(rhs=rhs, senses=senses)

	cols = []
	rows = []
	vals = []

	for i in range(num_edges):
		for j in connections[i]:
			cols.append(num_nodes + i)
			rows.append(j)
			vals.append(1)

	for i in range(num_edges):
		cols.append(num_nodes + i)
		rows.append(num_nodes + i)
		vals.append(-1)

		for j in connections[i]:
			cols.append(j)
			rows.append(num_nodes + i)
			vals.append(-1)

	cpx.linear_constraints.set_coefficients(zip(rows, cols, vals))

	cpx.solve()

	return cpx.solution.get_values()[0 : num_nodes], 4 * cpx.solution.get_objective_value() 

def Truncation():
	global theta
	global connections
	global projections
	global connections_truncated
	global output_file_path

	truncations = []
	connections_truncated = []

	for i in range(len(projections)):
		if projections[i] >= 0.25:
			truncations.append(i)

	for connection in connections:
		if connection[0] not in truncations and connection[1] not in truncations:
			connections_truncated.append(connection)

	output_file_path = "./projection_edge/" + input_file_path[len(input_file_path) - list(reversed(input_file_path)).index('/') : -4] + "_" + str(theta) + ".csv"
	output_file = open(output_file_path,'w')

	for connection in connections_truncated:
		output_file.write(str(connection[0]) + ' ' + str(connection[1]) + '\n')
		output_file.write(str(connection[1]) + ' ' + str(connection[0]) + '\n')

def Count():
	global k
	global connections_truncated
	global output_file_path

	con = psycopg2.connect(dbname="fangjuanru")
	cur = con.cursor()

	output_file = open(output_file_path, 'r')

	cur.execute("CREATE TABLE EDGE (FROM_ID INTEGER NOT NULL, TO_ID INTEGER NOT NULL);")
	cur.execute("CREATE INDEX on EDGE using hash (FROM_ID);")
	cur.execute("CREATE INDEX on EDGE using hash (TO_ID);")

	cur.copy_from(output_file, 'EDGE', sep=' ')

	num = 0
	query = ""

	if k == 0:		# edge
		query = "SELECT count(*) FROM edge WHERE edge.from_id < edge.to_id;"
	elif k == 1:	# triangle
		query = "SELECT count(*) FROM edge as r4, edge as r5, edge as r6 WHERE r4.from_id = r6.to_id and r5.from_id = r4.to_id and r6.from_id = r5.to_id and r4.from_id < r5.from_id and r5.from_id < r6.from_id;"
	elif k == 2:	# rectangle
		query = "SELECT count(*) FROM edge as r5, edge as r6, edge as r7, edge as r8 WHERE r5.from_id = r8.to_id and r6.from_id = r5.to_id and r7.from_id = r6.to_id and r8.from_id = r7.to_id and r5.from_id < r6.from_id and r5.from_id < r7.from_id and r5.from_id < r8.from_id and r6.from_id < r8.from_id;"
	elif k == 3:	# two triangle
		query = "SELECT count(*) FROM edge as r5, edge as r6, edge as r7, edge as r8, edge as r9 WHERE r5.from_id = r8.to_id and r6.from_id = r5.to_id and r7.from_id = r6.to_id and r8.from_id = r7.to_id and r5.from_id < r7.from_id and r6.from_id < r8.from_id and r9.from_id = r5.from_id and r9.to_id = r7.from_id;"
	elif k == 4:	# two path
		query = "SELECT count(*) FROM edge as r4, edge as r5 WHERE r5.from_id = r4.to_id and r4.from_id < r5.to_id;"
	else:
		return num

	cur.execute(query)

	num = int(cur.fetchall()[0][0])

	print("Count", num)

	return num

def RunAlgorithm():
	global epsilon
	global projections

	base = math.e
	beta = epsilon / 10

	projections, distance_estimator = LPSolver()

	Truncation()

	round_distance_estimator = math.ceil(distance_estimator)
	s_max = math.pow(base, - beta / 4 * (round_distance_estimator - distance_estimator)) * (2 * round_distance_estimator + 5) * RestrictedSensitivity()

	d_1 = math.floor(4 / beta - 5 / 2)
	d_2 = math.ceil(4 / beta - 5 / 2)

	if d_1 >= distance_estimator:
		s = math.pow(base, - beta / 4 * (d_1 - distance_estimator)) * (2 * d_1 + 5) * RestrictedSensitivity()
		if s > s_max:
			s_max = s
	
	if d_2 >= distance_estimator:
		s = math.pow(base, - beta / 4 * (d_2 - distance_estimator)) * (2 * d_2 + 5) * RestrictedSensitivity()
		if s > s_max:
			s_max = s

	print("Distance estimator", distance_estimator)
	print("RS", RestrictedSensitivity())
	print("SS", s_max)

	return Count() + CauNoise() * 10 * s_max / epsilon

def main(argv):
	global input_file_path
	global epsilon
	global theta
	global k
	
	try:
		opts, args = getopt.getopt(argv,"h:I:e:d:t:k:",["Input=","epsilon=","t=","k="])
	except getopt.GetoptError:
		print("SmoothDistanceEstimator.py -I <input file> -e <epsilon> -t <t> -k <k>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("SmoothDistanceEstimator.py -I <input file> -e <epsilon> -t <t> -k <k>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_file_path = str(arg)
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg)
		elif opt in ("-t","--t"):
			theta = int(arg)
		elif opt in ("-k","--k"):
			k = int(arg)

	ReadInput()
	res = RunAlgorithm()

	print("Output", res)

if __name__ == "__main__":
	main(sys.argv[1:])
