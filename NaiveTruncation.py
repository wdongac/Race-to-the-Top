import cplex
import getopt
import math
import numpy as np
import psycopg2
import random
import sys
import time

'''
python NaiveTruncation.py -I ./data/edge/Facebook.csv -e 1 -d 0.1 -t 100 -k 1
python NaiveTruncation.py -I ./data/edge/HepTh.csv -e 1 -d 0.1 -t 32 -k 1
python NaiveTruncation.py -I ./data/edge/test.csv -e 1 -d 0.1 -t 1 -k 1
'''

def ReadInput():
	global input_file_path
	global tuples
	global connections
	global size_dic
	global max_degree

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

	max_degree = max(size_dic.values())

def RestrictedSensitivity():
	global theta
	global k

	if k == 1:		# triangle
		return theta * (theta - 1) / 2
	elif k == 2:	# quadrilateral
		return theta * (theta - 1) * (theta - 2) / 2
	elif k == 3:	# star S_3
		return 2 * theta * (theta - 1) * (theta - 2) / 3
	else:
		return 0

def LocalSensitivity(i):
	global theta
	global size_dic

	count = 0

	for val in size_dic.values():
		if val >= theta - i and val <= theta + i + 1:
			count += 1

	return count

def LapNoise():
	a = random.uniform(0, 1)
	b = math.log(1 / (1 - a))
	c = random.uniform(0, 1)

	if c > 0.5:
		return b
	else:
		return -b

def Truncation():
	global theta
	global connections
	global size_dic
	global connections_truncated

	truncations = []
	connections_truncated = []

	for element in size_dic.keys():
		if size_dic[element] > theta:
			truncations.append(element)

	for connection in connections:
		if connection[0] not in truncations and connection[1] not in truncations:
			connections_truncated.append(connection)

	'''
	output_file_path = "./data/edge_naive_truncated/" + input_file_path[len(input_file_path) - list(reversed(input_file_path)).index('/') : -4] + "_" + str(theta) + ".csv"
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
	global max_degree

	Truncation()

	base = math.e
	beta = epsilon / 2 / math.log(2 / delta, base)

	max_ss_truncation = 0

	for i in range(max_degree):
		ls_truncation = LocalSensitivity(i) + i + 1
		ss_truncation = math.pow(base, - beta * i) * ls_truncation
		if ss_truncation > max_ss_truncation:
			max_ss_truncation = ss_truncation

	ss = max_ss_truncation * RestrictedSensitivity()

	print("Truncation sensitivity", max_ss_truncation)
	print("RS", RestrictedSensitivity())
	print("SS", ss)

	return Count() + LapNoise() * 2 * ss / epsilon

def main(argv):
	global input_file_path
	global epsilon
	global delta
	global theta
	global k
	
	try:
		opts, args = getopt.getopt(argv,"h:I:e:d:t:k:",["Input=","epsilon=","delta=","theta=","k="])
	except getopt.GetoptError:
		print("NaiveTruncation.py -I <input file> -e <epsilon> -d <delta> -t <theta> -k <k>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print("NaiveTruncation.py -I <input file> -e <epsilon> -d <delta> -t <theta> -k <k>")
			sys.exit()
		elif opt in ("-I", "--Input"):
			input_file_path = str(arg)
		elif opt in ("-e","--epsilon"):
			epsilon = float(arg)
		elif opt in ("-d","--delta"):
			delta = float(arg)
		elif opt in ("-t","--theta"):
			theta = int(arg)
		elif opt in ("-k","--k"):
			k = int(arg)

	ReadInput()
	res = RunAlgorithm()

	print("Output", res)

if __name__ == "__main__":
	main(sys.argv[1:])
