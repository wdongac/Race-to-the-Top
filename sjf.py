import getopt
import numpy as np
import sys

'''
python sjf.py -F ./data/test.csv -V 4 -C 2 -T 1
python sjf.py -F ./data/test2.csv -V 8 -C 4 -T 2

python sjf.py -F ./data/HepTh.csv -V 28339 -C 9877 -T 144
python sjf.py -F ./data/Facebook.csv -V 1612010 -C 4039 -T 128
python sjf.py -F ./data/FacebookPart.csv -V 500001 -C 4039 -T 128
'''

def linearLp():
	global FILE_PATH					# path of the read file
	global NUM_VARIABLE					# number of variables in the primal lp
	global NUM_CONSTRAINT				# number of constraints in the primal lp
	global T							# threshold
	
	f = open(FILE_PATH, "r")

	l = []

	for line in f:
		x = [int(e) for e in line.split('|')] # modify here : '|' for HepTh and test, ' ' for Facebook
		l.append(x[1])

	hist = [min(l.count(x), T) for x in set(l)]
	count = sum(hist)

	print(count)

def main(argv):
	global FILE_PATH					# path of the read file
	global NUM_VARIABLE					# number of variables in the primal lp
	global NUM_CONSTRAINT				# number of constraints in the primal lp
	global T							# threshold
	
	try:
		opts, args = getopt.getopt(argv,"h:F:V:C:T:",["FileName=","NumVariable=","NumConstraint=","Threshold="])
	except getopt.GetoptError:
		print("sjf.py -F <file name> -V <num of variables> -C <num of constraints> -T <threshold>")
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print("sjf.py -F <file name> -V <num of variables> -C <num of constraints> -T <threshold>")
			sys.exit()
		elif opt in ("-F", "--FileName"):
			FILE_PATH = str(arg)
		elif opt in ("-V","--NumVariable"):
			NUM_VARIABLE = int(arg)
		elif opt in ("-C","--NumConstraint"):
			NUM_CONSTRAINT = int(arg)
		elif opt in ("-T","--Threshold"):
			T = int(arg)

	linearLp()

if __name__ == "__main__":
	main(sys.argv[1:])