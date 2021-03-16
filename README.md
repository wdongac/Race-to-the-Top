# DP Foreign-key Constraints

## Table of Contents
* [Extract Relationships](#extract_relationships)
* [About the Project](#about-the-project)
* [Prerequisites](#prerequisites)

##About the Project
This project focuses on the counting query with self-joins and foreign key constraints. Without loss of generality, we assume there is only one private relation with a primary key (if there is no one, we just assume all attributes are combined to form a primary key).

The query supported has the form
```sh
Select COUNT(*)
From R1 AS R11, R1 AS R12, R2, R3 ...
Where ...;
```

#Prerequisites
Create a PostgreSql database like `test` and import data into that.

## Extract Relationships
To extract relationships between tuples in base table and query results.
```
python ExtractInfo.py -D test -Q ./testquery.txt -P edge -K ./testkeylist.txt -O out.txt
```
`-D` indicates the PostgreSql database name.
`-Q` the path of file storing the testing query.
`-P` the name of private relation.
`-K` the path of file storing the keys of the private relation. The keys should be in one line with splitted by space.
`-O` the path of output file. The IDs of tuples corresponding to one query result is stored in one line.
