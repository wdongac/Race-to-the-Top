# -*- coding: utf-8 -*-
import psycopg2
import sys, getopt



def main(argv):
    dataset = ''
    database_name = ''
    path = ''
    model = 0
    
    try:
        opts, args = getopt.getopt(argv,"h:d:D:p:m:",["dataset=","Database=","path=","model="])
    except getopt.GetoptError:
        print("ProcessGraphData.py -d <dataset> -D <database name> -p <path> -m <model:0(import)/1(clean)>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("ProcessGraphData.py -d <dataset> -D <database name> -p <path> -m <model:0(import)/1(clean)>")
            sys.exit()
        elif opt in ("-d", "--dataset"):
            dataset = arg
        elif opt in ("-D","--Database"):
            database_name = arg
        elif opt in ("-p","--path"):
            path = arg
        elif opt in ("-m","--model"):
            model = int(arg)
    if model==0:
        if path=='':
            print("Invalid path.")
            sys.exit()
        if dataset=='':
            print("Invalid dataset.")
            sys.exit()
            
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()  
    if model==0:
        edge_file = path+"/"+dataset+"_edges.txt"
        node_file = path+"/"+dataset+"_nodes.txt"
        code = "CREATE TABLE NODE (ID INTEGER NOT NULL);"
        cur.execute(code)
        code = "CREATE TABLE EDGE (FROM_ID INTEGER NOT NULL, TO_ID INTEGER NOT NULL);"
        cur.execute(code)
        code = "CREATE INDEX on NODE using hash (ID);"
        cur.execute(code)
        code = "CREATE INDEX on EDGE using hash (FROM_ID);"
        cur.execute(code)
        code = "CREATE INDEX on EDGE using hash (TO_ID);"
        cur.execute(code)
        code = "Copy edge FROM '"+edge_file+"' WITH DELIMITER AS '|';"
        cur.execute(code)
        code = "Copy node FROM '"+node_file+"' WITH DELIMITER AS '|';"
        cur.execute(code)
    else:
        code = "drop table node;"
        cur.execute(code)
        code = "drop table edge;"
        cur.execute(code)
    con.commit()
    con.close()



if __name__ == "__main__":
   main(sys.argv[1:])