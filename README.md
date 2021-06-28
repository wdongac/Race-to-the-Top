# Demo of Raise to the TOP

## Table of Contents
* [About the Project](#about-the-project)  
* [Prerequisites](#prerequisites)
    * [Tools](#tools)
    * [Python Dependency](#python-dependency)
    * [Download Data](#download-data)
    * [Create PostgreSQL Database](#create-postgresql-database)
* [Demo System](#demo-system)
* [Demo Collecting Experimental Results](#demo-collecting-experimental-results)
	* [R2T Algorithm](#r2t-algorithm)
	* [Naive Truncation with Smooth Sensitivity](#naive-truncation-with-smooth-sensitivity)
	* [Smooth Distance Estimator](#smooth-distance-estimator)
	* [LP-based Mechanism](#lp-based-mechanism)
	* [Recursive Mechansim](#recursive-mechanism)
	* [Local-sensitivity based Mechanism](#local-sensitivity-based-mechanism)

## About The Project
Raise to the Top (R2T) is for answering conjunctive query with sum aggregation over the database with foreign key constraints. This work has been submitted to SIGMOD 2022. The main task of this project is to demo the R2T system and the experiments in paper of SIGMOD 2022.

The file structure is as below
```
project
│   README.md
└───Code
└───Data
│   └───Graph
│   └───TPCH
└───Figure
└───Information
│   └───Graph
│   └───TPCH
└───Query
└───Result
│   └───Graph
│   └───TPCH
└───Script
└───Temp
└───TestSystem
```
`./Code` stores the codes.
`./Data` stores the relations of the graph and TPCH datasets.
`./Figure` stores the figures used in the paper.
`./Information` stores the information between base table tuples and joined results for all queries.
* `./Information/Graph` and `./Information/TPCH` store the information for sub-graph counting querie and TPCH querys repectively.

`./Query` stores the queries used in the experiments of the paper.
`./Result` stores the results used in the experiments of the paper.
* `./Result/Graph` and `./Result/TPCH` store the results for sub-graph counting querie and TPCH querys repectively.

`./Script` stores the scripts used in the experiments of the paper.
`./Temp` is used to store tempoaray files generated by programs.
`./TestSystem` is used to store the demo queries for the system.


## Prerequisites
### Tools
Before running this project, please install below tools
* [PostgreSQL](https://www.postgresql.org/)
* [Python3](https://www.python.org/download/releases/3.0/)
* [Cplex](https://www.ibm.com/analytics/cplex-optimizer)

Please do not install `Cplex` dependency, which can only handle small dataset, but download the `Cplex API` and import that to python with this [instruction](https://www.ibm.com/docs/zh/icos/12.9.0?topic=cplex-setting-up-python-api).

### Python Dependency
Here are dependencies used in python codes:
* `matplotlib`
* `numpy`
* `sys`
* `getopt`
* `os`
* `math`
* `psycopg2`

### Download Data
Download two data packages ([Graph](https://drive.google.com/file/d/18qv_ivmYpbA3qgs0elVcnepOlGC5Wd6a/view?usp=sharing) and [TPCH](https://drive.google.com/file/d/1hXTv24oAi56Ax0gdTQo4Vvx1ZzSg0Kz1/view?usp=sharing)) and unzip them in `./Data`.

Download two packages containing the relationships between base table tuples and join results ([Graph](https://drive.google.com/file/d/17BgDq_4Jt7QMAVdLMvR-dC5hUrfQiNOL/view?usp=sharing) and [TPCH](https://drive.google.com/file/d/18ZbpVyxOMM7tKmi54qBf44BUTgfboXmI/view?usp=sharing)) and unzip them in `./Information`.

### Create PostgreSQL Database
To create an empty PostgreSQL database, for example, named "Deezer", run
```
createdb Deezer;
```

#### Import and Clean Data
To import/clean graph data into PostgreSQL database, go to `./Script` and run `ProcessGraphData.py`. There are three parameters
 - `-d`: the name of graph dataset;
 - `-D`: the name of PostgreSQL database;
 - `-m`: the option of importing(0)/cleaning(1) data in the database;

To import/clean TPCH data into PostgreSQL database, go to `./Script` and run `ProcessTPCHData.py`. There are four parameters
 - `-d`: the name of TPCH dataset;
 - `-D`: the name of PostgreSQL database;
 - `-m`: the option of importing(0)/cleaning(1) data in the database;
 - `-r`: the path of file containing the name(s) of the primary private relation(s). The ones used in the paper can be found in `./Query`;

For example, to import TPCH dataset with scale \_0 into database named "sc\_0" having primary private relations SUPPLIER and CUSTOMER, run
```sh
python ProcessTPCHData.py -d _0 -D sc_0 -m 0 -r ../Query/sc.txt
```

To clean database named "Deezer", run
```sh
python ProcessGraphData.py -D Deezer -m 1
```

## Demo System
Here, we implement a demo version for R2T system with PostgreSQL. Currently, the system support the self-join query with single private relation. For the case with multiple primary private relations, please refer to our paper to write it to a query with single private relation. Currently, the system supports the selection but not the projection, which will be finished in the meta version. The inputs here are a query and a set of private parameters like privacy budget, the primary private relations and the output here is a noised query result. 

To run the system, go to `./Script` and run `System.py`. There are eight parameters
 - `-D`: the name of PostgreSQL database;
 - `-Q`: the path of input query file. Here, we provide the experimental queries used in the paper in `./Query`;
 - `-P`: the path of file containing the primary private relations;
 - `-K`: the path of file containing the primary key of the primary private relation; Here, we also provide the ones used in the paper in `./Query`;
 - `-e`: privacy budget epsilon;
 - `-b`: the parameter beta, which controls the probablity of large error happening;
 - `-G`: the predefined global sensitivity.
 - `-p`: the number of threads used.

For example, we run the system with `Q5`
```
python System.py -D sc_3 -e 0.8 -b 0.1 -G 1000000 -p 10 -Q ../TestSystem/Q18.txt -K ../TestSystem/Q18_key.txt -P ../TestSystem/Q18_private_relation.txt
```

## Demo Collecting Experimental Results
Notice that, for some experiments that do not have very much randomness (do not need to randomly select parameter) like R2T, recursive mechanism, we only run each experiments with 10 times.

### R2T Algorithm
We implement R2T algorithm for both self-join-free queries and self-join queries, which are `./Code/R2T.py` and `./Code/R2TSJF.py`. Both two programs has the relationships between base table's tuples and join results as the input, which can be collected by `./Code/ExtractInfo.py`.

The `ExtractInfo.py` has the parameters
 - `-D`: the name of PostgreSQL database;
 - `-Q`: the path of input query file. Here, we provide the experimental queries used in the paper in `./Query`;
 - `-P`: the name of primary private relation;
 - `-K`: the path of file containing the primary key of the primary private relation; Here, we also provide the ones used in the paper in `./Query`;
 - `-O`: the path of output file;
Note that, this program only supports the queries with single primary relation but in the system above, the queries with multiple primary relations are also supported. For the output file, the first column is the function value for the join result and the other columns are the ids of base table tuples contributing to the jooin result.

For example,
```
python ExtractInfo.py -D RoadnetPA -Q ../Query/triangle.txt -P node -K ../Query/triangle_key.txt -O ../Information/Graph/triangle/RoadnetCA.txt
```

The `R2T.py` has the parameters
 - `-I`: the path of file containing relationship between base table tuples and join results;
 - `-e`: privacy budget epsilon;
 - `-b`: the parameter beta, which controls the probablity of large error happening;
 - `-G`: the predefined global sensitivity.
 - `-p`: the number of threads used.
For example,
 ```
python R2T.py -I ../Information/Graph/triangle/RoadnetCA.txt -e 0.8 -b 0.1 -p 10  -G 256
```

The `R2TSJF.py` has same parameters except no `-p`. Besides, one notice is that, we use base 5.5 instead of 2 in these two algorithms. That has no effect on any result of paper.

There are five experiements for R2T. 1) collecting the time of collecting relationships between base table tuples and join results for both sub-graph counting queries and TPCH queries; 2) experiments for sub-graph counting queries and TPCH queries with various epsilon; 3) experiments for TPCH queries with different scalability; 4) experiments for TPCH queries with different GS.

To implement above, we first go to `./Script`, for 1), run `CollectExtractInfoTimeGraph.py` and  `CollectExtractInfoTimeTPCH.py`; for 2), run `CollectResultsGraph.py` and `CollectResultsTPCH.py`; for 3), run `CollectResultsTPCHScalability.py`; for 4), run `CollectResultsTPCHGS.py`.
 
### Naive Truncation with Smooth Sensitivity
First create a database for the graph, named "NT_" +  graph name, for these experiments to collect the real counts after truncations. For example, for Deezer, run
```
createdb NT_Deezer;
```
To collect the experimental results of naive truncation with smooth sensitivity with settings in the paper, go to `./Script` and run `CollectResultsNT.py`. There is one parameter
 - `-G`: the name of graph. The given choices include Deezer, Amazon1, Amazon2, RoadnetPA and RoadnetCA;

For example, we collect the results for Deezer with 
```
python CollectResultsNT.py -G Deezer
```

### Smooth Distance Estimator
First create a database for the graph named "SDE_" +  graph name. For example,
```
createdb SDE_Deezer;
```
To collect the experimental results of smooth distance estimator with settings in the paper, go to `./Script` and run `CollectResultsSDE.py`. There is one parameter
 - `-G`: the name of graph. The given choices include Deezer, Amazon1, Amazon2, RoadnetPA and RoadnetCA;

For example, we collect the results for Deezer with 
```
python CollectResultsSDE.py -G Deezer
```

### LP-based Mechanism
For experimental results of LP-based mechanism, we first implement `./Script/CollectResultsLPAllTau.py` to collect the running time and results for the LP with different truncation threshold. It has two parameters
 - `-Q`: the id of query,  0(one_path)/1(triangle)/2(two_path)/3(rectangle);
 - `-D`: the id of data, 0(Amazon2)/1(Amazon1)/2(RoadnetPA)/3(RoadnetCA)/4(Deezer);

For example
```
python CollectResultsLPAllTau.py -Q 0 -D 0 > ../Result/Graph/LP_All_Tau_one_path_Amazon2.txt
```

Then, we collect the experimental results for LP-based mechanism with `./Script/CollectResultsLP.py`. Besides, to collect the experimental results for different fixed truncation thresholds, we use `./Script/CollectResultsLPDifferentTau.py`.

### Recursive Mechanism
To collect experimental results of recursive mechanism, go to `./Script` and run `CollectResultsRM.py` with parameters
 - `-Q`: the id of query,  0(one_path)/1(triangle)/2(two_path)/3(rectangle);
 - `-D`: the id of data, 0(Amazon2)/1(Amazon1)/2(RoadnetPA)/3(RoadnetCA)/4(Deezer);
- `-e`: privacy budget epsilon;

For example,
```
python CollectResultsRM.py -Q 0 -D 0 -e 0.8
```

### Local-sensitivity based Mechanism
There are three types of experiments for local-sensitivity based mechanism in the paper, 1) changing privacy budget epsilon, 2) changing scale of database and 3) changing predefined global sensitivity.

For 1), go to `./Script` and run `CollectResultsLS.py`. For 2), run `CollectResultsLSScalability.py` in `./Script`, and for 3) run `CollectResultsLSGS.py` in `./Script`.
