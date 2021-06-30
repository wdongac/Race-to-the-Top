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
Raise to the Top (R2T) is for answering SJPA over the database with foreign key constraints. This work has been submitted to SIGMOD 2022. The main task of this project is to demo the R2T system and the experiments in that paper.

The file structure is as below
```
project
│   
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

`./Data` stores graph and TPCH datasets.

`./Figure` stores the figures used in the paper.

`./Information` stores the relationships between base table tuples and joined results for all queries.
* `./Information/Graph` and `./Information/TPCH` store such information for sub-graph counting querie and TPCH querys repectively.

`./Query` stores the queries used in the experiments of the paper.

`./Result` stores the experimental results.
* `./Result/Graph` and `./Result/TPCH` store the results for sub-graph counting queries and TPCH queries respectively.

`./Script` stores the scripts used in the experiments of the paper.

`./Temp` stores temporary files generated by programs.

`./TestSystem` stores the demo queries for the system.


## Prerequisites
### Tools
Before running this project, please install below tools
* [PostgreSQL](https://www.postgresql.org/)
* [Python3](https://www.python.org/download/releases/3.0/)
* [Cplex](https://www.ibm.com/analytics/cplex-optimizer)

Please do not install `Cplex` dependency, which can only handle a small dataset, but download the `Cplex API` and import that to python with this [instruction](https://www.ibm.com/docs/zh/icos/12.9.0?topic=cplex-setting-up-python-api).

### Python Dependency
Here are dependencies used in python programs:
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

Here, we need five databases for the graph dataset: `Deezer`, `Amazon1`, `Amazon2`, `RoadnetPA` and `RoadnetCA`. For TPCH dataset, we use `7` different scales: `0.125,0.25,..,8` which are marked as `_0,_1,..,_6`, For each scale, we create two databases: `sc` and `so`. `sc` has `Customer` and `Supplier` as the primary private relations while `so` has `Orders` and `Supplier` as the primary private relations. For example, for scale `_3`, we create `sc_3` and `so_3`. The reason why we need to consider these two cases separately is that, when we conduct the experiments, we only support self-join queries with single primary private relation thus we need to create a new ID table and assign the IDs for the tuples in the designated primary private relations. However, this issue has been addressed in our system, which means you can use either database in our system demo.

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

For example, to import TPCH dataset with scale `_0` into `sc\_0` database, run
```sh
python ProcessTPCHData.py -d _0 -D sc_0 -m 0 -r ../Query/sc.txt
```

To clean database named "Deezer", run
```sh
python ProcessGraphData.py -D Deezer -m 1
```

## Demo System
Here, we implement a demo version for R2T system with PostgreSQL. Currently, the system supports the selection, join, sum aggregation but not the projection, which will be finished in the meta version. The inputs here are a query and a set of private parameters like privacy budget, the primary private relations, and the output here is a noised query result.

To run the system, go to `./Script` and run `System.py`. There are eight parameters
 - `-D`: the name of PostgreSQL database;
 - `-Q`: the path of input query file;
 - `-P`: the path of the file containing the primary private relations;
 - `-K`: the path of the file containing the primary key of the primary private relation; 
 - `-e`: privacy budget epsilon;
 - `-b`: the parameter beta, which controls the probability of large error happening;
 - `-G`: the predefined global sensitivity.
 - `-p`: the number of threads used.

We provide several demo queries in `./TestSystem`. For example, we run the system with `Q5`
```
python System.py -D sc_3 -e 0.8 -b 0.1 -G 1000000 -p 10 -Q ../TestSystem/Q18.txt -K ../TestSystem/Q18_key.txt -P ../TestSystem/Q18_private_relation.txt
```

## Demo Collecting Experimental Results
Notice that, for some experiments that do not have very much randomness (do not need to randomly select parameter) like R2T, RM, we only repeat each experiment with 10 times instead of 100 times at same the time.

### R2T Algorithm
We implement R2T algorithm for both self-join-free queries and self-join queries, which are `./Code/R2T.py` and `./Code/R2TSJF.py`. Both two programs have the relationships between the base table's tuples and join results as the input, which can be collected by `./Code/ExtractInfo.py`.

The `ExtractInfo.py` has five parameters
 - `-D`: the name of PostgreSQL database;
 - `-Q`: the path of input query file. Here, we provide the experimental queries used in the paper in `./Query`;
 - `-P`: the name of primary private relation;
 - `-K`: the path of the file containing the primary key of the primary private relation; Here, we also provide the ones used in the paper in `./Query`;
 - `-O`: the path of the output file;
Note that, this program only supports the queries with single primary relation but in the system above, the queries with multiple primary relations are supported. For the output file, the first column is the function value for the join result and the other columns are the IDs of base table tuples contributing to that join result.

For example,
```
python ExtractInfo.py -D RoadnetPA -Q ../Query/triangle.txt -P node -K ../Query/triangle_key.txt -O ../Information/Graph/triangle/RoadnetCA.txt
```
Such information for the queries used in the paper have already been collected and store in `./Information/Graph` and `./Information/TPCH`. One notice is that recursive mechanism and LP-based mechanism also have such information as their inputs.

The `R2T.py` has five parameters
 - `-I`: the path of the file containing the relationship between base table tuples and join results;
 - `-e`: privacy budget epsilon;
 - `-b`: the parameter beta, which controls the probability of large error happening;
 - `-G`: the predefined global sensitivity.
 - `-p`: the number of threads used.
For example,
 ```
python R2T.py -I ../Information/Graph/triangle/RoadnetCA.txt -e 0.8 -b 0.1 -p 10  -G 256
```

The `R2TSJF.py` has the same parameters except no `-p` parameter. Besides, one notice is that we use base 5.5 (2e) instead of 2 in these two algorithms, which will not affect any theoretical result in the paper.

There are five experiments for R2T. 1) collecting the time of extracting relationships between base table tuples and join results for both sub-graph counting queries and TPCH queries; 2) experiments for sub-graph counting queries and TPCH queries with various epsilon; 3) experiments for TPCH queries with different scalability; 4) experiments for TPCH queries with different GS.

To implement above, we first go to `./Script` and for 1), run `CollectExtractInfoTimeGraph.py` and  `CollectExtractInfoTimeTPCH.py`; for 2), run `CollectResultsGraph.py` and `CollectResultsTPCH.py`; for 3), run `CollectResultsTPCHScalability.py`; for 4), run `CollectResultsTPCHGS.py`.
 
### Naive Truncation with Smooth Sensitivity
First create a database for the graph, named "NT_" +  graph name, for these experiments to collect the real counts after truncations. For example, for Deezer, run
```
createdb NT_Deezer;
```
To collect the experimental results of naive truncation with smooth sensitivity with settings in the paper, go to `./Script` and run `CollectResultsNT.py`. There is one parameter
 - `-G`: the name of the graph. The given choices include Deezer, Amazon1, Amazon2, RoadnetPA, and RoadnetCA;

For example, we collect the results for Deezer with 
```
python CollectResultsNT.py -G Deezer
```

### Smooth Distance Estimator
First, create a database for the graph named "SDE_" +  graph name. For example,
```
createdb SDE_Deezer;
```
To collect the experimental results of smooth distance estimator with settings in the paper, go to `./Script` and run `CollectResultsSDE.py`. There is one parameter
 - `-G`: the name of the graph. The given choices include Deezer, Amazon1, Amazon2, RoadnetPA, and RoadnetCA;

For example, we collect the results for Deezer with 
```
python CollectResultsSDE.py -G Deezer
```

### LP-based Mechanism
For experimental results of the LP-based mechanism, we first implement `./Script/CollectResultsLPAllTau.py` to collect the running time and results for the LP with different truncation thresholds. It has two parameters
 - `-Q`: the id of query,  0(one_path)/1(triangle)/2(two_path)/3(rectangle);
 - `-D`: the id of data, 0(Amazon2)/1(Amazon1)/2(RoadnetPA)/3(RoadnetCA)/4(Deezer);

For example
```
python CollectResultsLPAllTau.py -Q 0 -D 0 > ../Result/Graph/LP_All_Tau_one_path_Amazon2.txt
```

Then, we collect the experimental results for the LP-based mechanism with `./Script/CollectResultsLP.py`. Besides, to collect the experimental results for different fixed truncation thresholds, please run `./Script/CollectResultsLPDifferentTau.py`.

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
There are three types of experiments for local-sensitivity based mechanism in the paper, 1) changing privacy budget epsilon, 2) changing the scale of the database, and 3) changing predefined global sensitivity.

For 1), go to `./Script` and run `CollectResultsLS.py`. For 2), run `CollectResultsLSScalability.py` in `./Script`, and for 3) run `CollectResultsLSGS.py` in `./Script`.
