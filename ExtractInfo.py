#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import getopt
import psycopg2



def ReadQuery():
    global query
    global query_path
    query = ""
    query_file = open(query_path,'r')
    for line in query_file.readlines():
        query = query+line
        if ";" in query:
            query = query.replace('\n'," ")
            break
    
    
    
def ReadPrimaryKey():
    global primary_key_list
    global primary_key_path
    key_list_file = open(primary_key_path,'r')
    line=key_list_file.readline()
    primary_key_list = line.split()
    
    
    
def RewriteQuery():
    global query
    global private_relation_name
    global rewrite_query
    global primary_key_list
    # Separate from each part
    parser_string = query.lower()
    parser_string = parser_string.replace(" from ","\n")
    parser_string = parser_string.replace(" where ","\n")
    parser_string = parser_string.replace(";","")
    parser_strings = parser_string.split("\n")
    from_strings = parser_strings[1]
    where_strings = parser_strings[2]
    renaming_private_relations=[]
    #Extract the renaming information for relation part
    relations_strings = from_strings.replace(",","\n")
    relations_strings = relations_strings.split("\n")

    #For each renaming
    for relations_string in relations_strings:
        relations_string = relations_string.split()
        origin_relation = relations_string[0]
        if len(relations_string)>1:
            renaming_relation = relations_string[2]
        else:
            renaming_relation = relations_string[0]
        if origin_relation==private_relation_name:
            renaming_private_relations.append(renaming_relation)
            
    #Begin to rewrite the query
    rewrite_query = "select "
    for i in range(len(renaming_private_relations)):
        concat_attr = ""
        for j in range(len(primary_key_list)):
            if j==0:
                concat_attr = "concat("+renaming_private_relations[i]+"."+primary_key_list[j]+",\',\')"
            else:
                concat_attr = concat_attr+"||concat("+renaming_private_relations[i]+"."+primary_key_list[j]+",\',\')"
        concat_attr=concat_attr+" as id"+str(i)
        if i==0:
            rewrite_query=rewrite_query+concat_attr
        else:
            rewrite_query=rewrite_query+", "+concat_attr
    rewrite_query=rewrite_query+" "
    #Add the from part and where part
    rewrite_query = rewrite_query+"from "+from_strings+" where "+where_strings+";"
    
    

def ExtractRelationship():
    global database_name
    global rewrite_query
    global output_file
    con = psycopg2.connect(database=database_name)
    cur = con.cursor()
    cur.execute(rewrite_query)
    res = cur.fetchall()
    id_dic = {}
    results = open(output_file,'w')
    num_id = 0
    for i in range(len(res)):
        temp_res = res[i]
        for j in range(len(temp_res)):
           temp_id = temp_res[j]
           if temp_id in id_dic:
               results.write(str(id_dic[temp_id])+" ")
           else:
               id_dic[temp_id] = num_id
               results.write(str(num_id)+" ")
               num_id+=1
        results.write("\n")

        

def main(argv):
    global database_name
    global query_path
    global private_relation_name
    global primary_key_path
    global output_file
    
    try:
        opts, args = getopt.getopt(argv,"h:D:Q:P:K:O:",["Database=","QueryPath=","PrivateRelationName=","PrimaryKey=","Output="])
    except getopt.GetoptError:
        print("ExtractInfo.py -D <database name> -Q <query file path> -P <private relation name> -K <primary key of private relation> -O <output file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("ExtractInfo.py -D <database name> -Q <query file path> -P <private relation name> -K <primary key of private relation> -O <output file>")
            sys.exit()
        elif opt in ("-D", "--Database"):
            database_name = arg
        elif opt in ("-Q","--QueryPath"):
            query_path = arg
        elif opt in ("-P","--PrivateRelationName"):
            private_relation_name = arg
        elif opt in ("-K","--PrimaryKey"):
            primary_key_path=arg
        elif opt in ("-O","--Output"):
            output_file=arg
    
    ReadQuery()
    ReadPrimaryKey()
    RewriteQuery()
    ExtractRelationship()



if __name__ == "__main__":
   main(sys.argv[1:])