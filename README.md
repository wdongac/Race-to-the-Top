# Demo of Raise to the TOP

## Table of Contents
* [About the Project](#about-the-project)  
* [Prerequisites](#prerequisites)
    * [Tools](#tools)
    * [Python Dependency](#python-dependency)
    * [Create PostgreSQL Database](#create-postgresql-database)
* [Demo System](#demo-system)
* [Demo Collecting Experimental Results](#demo-baseline-algorithm)
	* [R2T Algorithm](#r2t-algorithms)
	* [Naive Truncation with Smooth Sensitivity](#naive-truncation-with-smooth-sensitivity)
	* [Smooth Distance Estimator](#smooth-distance-estimator)
	* [LP-based Mechanism](#lp-based-mechanism)
	* [Recursive Mechansim](#recursive-mechanism)
	* [Local-sensitivity based Mechanism](#local-sensitivity-based-mechanism)

## About The Project
Raise to the Top (R2T) is for answering conjunctive query with sum aggregation over the database with foreign key constraints. This work has been submitted to SIGMOD 2022. The main task of this project is to demo the R2T system and the experiments in paper of SIGMOD 2022. More precisely,
+ Demo the R2T system;
+ Demo baseline algorithms: naive truncation with smooth sensitivity (NT), smooth distance estimator (SDE), LP-based mechanism (LP), recursive mechansim (RM) and local-sensitivity based mechanism (LS).
+ Demo how to collect experimental results shown in our paper.

The file structure is as below
```
project
│   README.md
└───Code
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
```
`./Code` stores the codes.
`./Figure` stores the figures used in the paper.
`./Information` stores the information between base table tuples and joined results for all queries.
* `./Information/Graph` and `./Information/TPCH` store the information for sub-graph counting querie and TPCH querys repectively.

`./Query` stores the queries used in the experiments of the paper.
`./Result` stores the results used in the experiments of the paper.
* `./Result/Graph` and `./Result/TPCH` store the results for sub-graph counting querie and TPCH querys repectively.

`./Script` stores the scripts used in the experiments of the paper.
`./Temp` is used to store tempoaray files generated by programs.


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

### Create PostgreSQL Database

#### Import Data

## Demo System
Here, we implement a demo version for R2T system with PostgreSQL. Currently, the system support the self-join query with single private relation. For the case with multiple primary private relations, please refer to our paper to write it to a query with single private relation. Currently, the system supports the selection but not the projection, which will be finished in the meta version. The inputs here are a query and a set of private parameters like privacy budget, the primary private relation and the output here is a noised query result. 

To run the system, go to `./Script` and run `System.py`. There are eight parameters
 - `-D`: the name of PostgreSQL database;
 - `-Q`: the path of input query file. Here, we provide the experimental queries used in the paper in `./Query`;
 - `-P`: the name of primary private relation;
 - `-K`: the path of file containing the primary key of the primary private relation. Here, we also provate the ones used in the paper in `./Query`;
 - `-e`: privacy budget epsilon;
 - `-b`: the parameter beta, which controls the probablity of large error happening;
 - `-G`: the predefined global sensitivity.
 - `-p`: the number of threads used.

For example, we run the system with `Q5`
```
python System.py -D so_0 -Q ../Query/Q21.txt -P ids -K ../Query/Q21_key.txt -e 0.8 -b 0.1 -G 1000000 -p 10
```

## Demo Collecting Experimental Results

### R2T Algorithm

### Naive Truncation with Smooth Sensitivity

### Smooth Distance Estimator

### LP-based Mechanism

### Recursive Mechansim

### Local-sensitivity based Mechanism
