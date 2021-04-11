import cplex
import getopt
import math
import numpy as np
import psycopg2
import random
import sys
import time

'''
python SmoothDistanceEstimator.py -I ./data/edge/Facebook.csv -e 1 -d 0.1 -t 100 -k 1
python SmoothDistanceEstimator.py -I ./data/edge/HepTh.csv -e 1 -d 0.1 -t 32 -k 1
python SmoothDistanceEstimator.py -I ./data/edge/test.csv -e 1 -d 0.1 -t 1 -k 1
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

	if k == 1:		# triangle
		return theta * (2 * theta - 1)
	elif k == 2:	# quadrilateral
		return theta * (2 * theta - 1) * (2 * theta - 2)
	elif k == 3:	# star S_3
		return 4 * theta * (2 * theta - 1) * (2 * theta - 2) / 3
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

	truncations = []
	connections_truncated = []

	for i in range(len(projections)):
		if projections[i] >= 0.25:
			truncations.append(i)

	for connection in connections:
		if connection[0] not in truncations and connection[1] not in truncations:
			connections_truncated.append(connection)

	'''
	output_file_path = "./data/edge_truncated/" + input_file_path[len(input_file_path) - list(reversed(input_file_path)).index('/') : -4] + "_" + str(theta) + ".csv"
	output_file = open(output_file_path,'w')

	for connection in connections_truncated:
		output_file.write(str(connection[0]) + ' ' + str(connection[1]) + '\n')
	'''

def Count():
	global k
	global connections_truncated

	con = psycopg2.connect(dbname="fangjuanru")
	cur = con.cursor()

	cur.execute("CREATE TABLE edge (id serial PRIMARY KEY, p1 integer, p2 integer);")

	for connection in connections_truncated:
		cur.execute("INSERT INTO edge (p1, p2) VALUES (%s, %s)", (connection[0], connection[1]))
		cur.execute("INSERT INTO edge (p1, p2) VALUES (%s, %s)", (connection[1], connection[0]))

	num = 0
	query = ""

	if k == 1:		# triangle
		query = "SELECT count(*) FROM edge as A, edge as B, edge as C WHERE A.p2 = B.p1 AND B.p2 = C.p1 AND C.p2 = A.p1 AND A.p1 < B.p1 AND B.p1 < C.p1;"
	elif k == 2:	# quadrilateral
		query = "SELECT count(*) FROM edge as A, edge as B, edge as C, edge as D WHERE A.p2 = B.p1 AND B.p2 = C.p1 AND C.p2 = D.p1 AND D.p2 = A.p1 AND A.p1 < B.p1 AND B.p1 < C.p1 AND C.p1 < D.p1;"
	elif k == 3:	# star S_3
		query = "SELECT count(*) FROM edge as A, edge as B, edge as C WHERE A.p1 = B.p1 AND B.p1 = C.p1 AND A.p2 < B.p2 AND B.p2 < C.p2"
	else:
		return num

	cur.execute(query)

	num = int(cur.fetchall()[0][0])

	print("Count", num)

	return num

def RunAlgorithm():
	global epsilon
	global delta
	global projections

	base = math.e
	beta = epsilon / 2 / math.log(2 / delta, base)

	projections, distance_estimator = LPSolver()

	Truncation()

	s_max = (2 * distance_estimator + 5) * RestrictedSensitivity()

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

	return Count() + LapNoise() * 2 * s_max / epsilon

def main(argv):
	global input_file_path
	global epsilon
	global delta
	global theta
	global k
	
	try:
		opts, args = getopt.getopt(argv,"h:I:e:d:t:k:",["Input=","epsilon=","delta=","t=","k="])
	except getopt.GetoptError:
		print("SmoothDistanceEstimator.py -I <input file> -e <epsilon> -d <delta> -t <t> -k <k>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("SmoothDistanceEstimator.py -I <input file> -e <epsilon> -d <delta> -t <t> -k <k>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_file_path = str(arg)
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg)
		elif opt in ("-d","--delta"):
			delta = float(arg)
		elif opt in ("-t","--t"):
			theta = int(arg)
		elif opt in ("-k","--k"):
			k = int(arg)

	ReadInput()
	res = RunAlgorithm()

	print("Output", res)

if __name__ == "__main__":
	main(sys.argv[1:])
