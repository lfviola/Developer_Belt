# 🐍 📄 PySpark Cheat Sheet 
from https://github.com/kevinschaich/


A quick reference guide to the most commonly used patterns and functions in PySpark SQL.

#### Table of Contents

- [Common Patterns](#common-patterns).
    - [Creating a single column DF](#Creating-a-single-column-DF)   
    - [Creating DF without schema](#Creating-DF-without-schema)
    - [Creating DF with schema](#Creating-DF-with-schema)
    - [Creating a json DF](#Creating-a-json-DF)
    - [Importing Functions & Types](#importing-functions--types)
    - [Filtering](#filtering)
    - [Joins](#joins)
    - [Column Operations](#column-operations)
    - [Casting & Coalescing Null Values & Duplicates](#casting--coalescing-null-values--duplicates)
- [String Operations](#string-operations)
    - [String Filters](#string-filters)
    - [String Functions](#string-functions)
- [Number Operations](#number-operations)
- [Date & Timestamp Operations](#date--timestamp-operations)
- [Array Operations](#array-operations)
- [Aggregation Operations](#aggregation-operations)
- [Advanced Operations](#advanced-operations)
    - [Repartitioning](#repartitioning)
    - [UDFs (User Defined Functions](#udfs-user-defined-functions)
    - [Window Functions](#window-functions)
    - [Regular Expressions (RegEx)](#regular-rxpressions--regex-)

If you can't find what you're looking for, check out the [PySpark Official Documentation](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html) and add it here!

## Common Patterns

#### Creating a single column DF

```python
df = spark.createDataFrame(
    [
    (1,),(2,),(3,)
    ]
).toDF("id")
```

#### Creating DF without schema

```python
df = spark.createDataFrame(
    [
    ('2018-03-31','6','1'),
    ('2018-03-31','27','2'),
    ('2018-03-31','3','3'),
    ('2018-03-31','44','4'),
    ],
    ["date", "median", "Q"]
)\
    .withColumn('date', F.col('date').cast('date'))\
    .withColumn('median', F.col('median').cast('integer'))\
    .withColumn('Q', F.col('Q').cast('integer'))
```

#### Creating DF with schema

```python
from pyspark.sql import functions as F
from pyspark.sql.types import *

data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])
  
df = spark.createDataFrame(data=data2,schema=schema)
df.show()
df.printSchema()
```

#### Creating a json DF

```python
from pyspark.sql.types import *
from pyspark.sql import functions as F


data = [('a1', '[{"key":"key1","value":10.0},{"key":"key2","value":20.0}]')
       ,('a1', '[{"key":"key3","value":30.0},{"key":"key1","value":40.0}]')
       ,('a2', '[{"key":"key1","value":10.0},{"key":"key1","value":50.0}]')]

my_schema = ArrayType(
                      StructType([
                          StructField('key', StringType()),
                          StructField('value', DoubleType())
                      ])
                      )
    
df = spark.createDataFrame(data, ['id', 'json_str'])\
    .withColumn('json', F.from_json('json_str', my_schema))
```

#### Importing Functions & Types

```python
# Easily reference these as F.my_function() and T.my_type() below
from pyspark.sql import functions as F, types as T
```

#### Filtering

```python
# Filter on equals condition
df = df.filter(df.is_adult == 'Y')

# Filter on >, <, >=, <= condition
df = df.filter(df.age > 25)

# Multiple conditions require parentheses around each condition
df = df.filter((df.age > 25) & (df.is_adult == 'Y'))

# Compare against a list of allowed values
df = df.filter(col('first_name').isin([3, 4, 7]))

# Sort results
df = df.orderBy(df.age.asc()))
df = df.orderBy(df.age.desc()))
```

#### Joins

```python
# Left join in another dataset
df = df.join(person_lookup_table, 'person_id', 'left')

# Match on different columns in left & right datasets
df = df.join(other_table, df.id == other_table.person_id, 'left')

# Match on multiple columns
df = df1.join(df2, (df1.x1 == df2.x1) & (df1.x2 == df2.x2))

# Match on multiple columns
df = df.join(other_table, ['first_name', 'last_name'], 'left')

# Useful for one-liner lookup code joins if you have a bunch
def lookup_and_replace(df1, df2, df1_key, df2_key, df2_value):
    return (
        df1
        .join(df2[[df2_key, df2_value]], df1[df1_key] == df2[df2_key], 'left')
        .withColumn(df1_key, F.coalesce(F.col(df2_value), F.col(df1_key)))
        .drop(df2_key)
        .drop(df2_value)
    )

df = lookup_and_replace(people, pay_codes, id, pay_code_id, pay_code_desc)
```

#### Column Operations

```python
# Add a new static column
df = df.withColumn('status', F.lit('PASS'))

# Construct a new dynamic column
df = df.withColumn('full_name', F.when(
    (df.fname.isNotNull() & df.lname.isNotNull()), F.concat(df.fname, df.lname)
).otherwise(F.lit('N/A'))

# Pick which columns to keep, optionally rename some
df = df.select(
    'name',
    'age',
    F.col('dob').alias('date_of_birth'),
)

# Remove columns
df = df.drop('mod_dt', 'mod_username')

# Rename a column
df = df.withColumnRenamed('dob', 'date_of_birth')

# Keep all the columns which also occur in another dataset
df = df.select(*(F.col(c) for c in df2.columns))

# Batch Rename/Clean Columns
for col in df.columns:
    df = df.withColumnRenamed(col, col.lower().replace(' ', '_').replace('-', '_'))
```

#### Casting & Coalescing Null Values & Duplicates

```python
# Cast a column to a different type
df = df.withColumn('price', df.price.cast(T.DoubleType()))

# Replace all nulls with a specific value
df = df.fillna({
    'first_name': 'Tom',
    'age': 0,
})

# Take the first value that is not null
df = df.withColumn('last_name', F.coalesce(df.last_name, df.surname, F.lit('N/A')))

# Drop duplicate rows in a dataset (distinct)
df = df.dropDuplicates()

# Drop duplicate rows, but consider only specific columns
df = df.dropDuplicates(['name', 'height'])
```

## String Operations

#### String Filters

```python
# Contains - col.contains(string)
df = df.filter(df.name.contains('o'))

# Starts With - col.startswith(string)
df = df.filter(df.name.startswith('Al'))

# Ends With - col.endswith(string)
df = df.filter(df.name.endswith('ice'))

# Is Null - col.isNull()
df = df.filter(df.is_adult.isNull())

# Is Not Null - col.isNotNull()
df = df.filter(df.first_name.isNotNull())

# Like - col.like(string_with_sql_wildcards)
df = df.filter(df.name.like('Al%'))

# Regex Like - col.rlike(regex)
df = df.filter(df.name.rlike('[A-Z]*ice$'))

# Is In List - col.isin(*cols)
df = df.filter(df.name.isin('Bob', 'Mike'))
```

#### String Functions

```python
# Substring - col.substr(startPos, length)
df = df.withColumn('short_id', df.id.substr(0, 10))

# Trim - F.trim(col)
df = df.withColumn('name', F.trim(df.name))

# Left Pad - F.lpad(col, len, pad)
# Right Pad - F.rpad(col, len, pad)
df = df.withColumn('id', F.lpad('id', 4, '0'))

# Left Trim - F.ltrim(col)
# Right Trim - F.rtrim(col)
df = df.withColumn('id', F.ltrim('id'))

# Concatenate - F.concat(*cols)
df = df.withColumn('full_name', F.concat('fname', F.lit(' '), 'lname'))

# Concatenate with Separator/Delimiter - F.concat_ws(delimiter, *cols)
df = df.withColumn('full_name', F.concat_ws('-', 'fname', 'lname'))

# Regex Replace - F.regexp_replace(str, pattern, replacement)[source]
df = df.withColumn('id', F.regexp_replace(id, '0F1(.*)', '1F1-$1'))

# Regex Extract - F.regexp_extract(str, pattern, idx)
df = df.withColumn('id', F.regexp_extract(id, '[0-9]*', 0))
```

## Number Operations

```python
# Round - F.round(col, scale=0)
df = df.withColumn('price', F.round('price', 0))

# Floor - F.floor(col)
df = df.withColumn('price', F.floor('price'))

# Ceiling - F.ceil(col)
df = df.withColumn('price', F.ceil('price'))

# Absolute Value - F.abs(col)
df = df.withColumn('price', F.abs('price'))

# X raised to power Y – F.pow(x, y)
df = df.withColumn('exponential_growth', F.pow('x', 'y'))

# Select smallest value out of multiple columns – F.least(*cols)
df = df.withColumn('least', F.least('subtotal', 'total'))

# Select largest value out of multiple columns – F.greatest(*cols)
df = df.withColumn('greatest', F.greatest('subtotal', 'total'))
```

## Date & Timestamp Operations

```python
# Convert a string of known format to a date (excludes time information)
df = df.withColumn('date_of_birth', F.to_date('date_of_birth', 'yyyy-MM-dd'))

# Convert a string of known format to a timestamp (includes time information)
df = df.withColumn('time_of_birth', F.to_timestamp('time_of_birth', 'yyyy-MM-dd HH:mm:ss'))

# Get year from date:       F.year(col)
# Get month from date:      F.month(col)
# Get day from date:        F.dayofmonth(col)
# Get hour from date:       F.hour(col)
# Get minute from date:     F.minute(col)
# Get second from date:     F.second(col)
df = df.filter(F.year('date_of_birth') == F.lit('2017'))

# Add & subtract days
df = df.withColumn('three_days_after', F.date_add('date_of_birth', 3))
df = df.withColumn('three_days_before', F.date_sub('date_of_birth', 3))

# Add & Subtract months
df = df.withColumn('next_month', F.add_month('date_of_birth', 1))

# Get number of days between two dates
df = df.withColumn('days_between', F.datediff('start', 'end'))

# Get number of months between two dates
df = df.withColumn('months_between', F.months_between('start', 'end'))

# Keep only rows where date_of_birth is between 2017-05-10 and 2018-07-21
df = df.filter(
    (F.col('date_of_birth') >= F.lit('2017-05-10')) &
    (F.col('date_of_birth') <= F.lit('2018-07-21'))
)
```

## Array Operations

```python
# Column Array - F.array(*cols)
df = df.withColumn('full_name', F.array('fname', 'lname'))

# Empty Array - F.array(*cols)
df = df.withColumn('empty_array_column', F.array([]))

# Array Size/Length – F.size(col)
df = df.withColumn('array_length', F.size(F.col('my_array')))
```

## Aggregation Operations

```python
# Row Count:                F.count()
# Sum of Rows in Group:     F.sum(*cols)
# Mean of Rows in Group:    F.mean(*cols)
# Max of Rows in Group:     F.max(*cols)
# Min of Rows in Group:     F.min(*cols)
# First Row in Group:       F.alias(*cols)
df = df.groupBy('gender').agg(F.max('age').alias('max_age_by_gender'))

# Collect a Set of all Rows in Group:       F.collect_set(col)
# Collect a List of all Rows in Group:      F.collect_list(col)
df = df.groupBy('age').agg(F.collect_set('name').alias('person_names'))
    
# Count the number of occurences
df  = spark.createDataFrame(
  [('1','0'),('2','1'),('3','1'),('4','1'),('5','0'),('6','0')
   ,('7','1'),('8','1'),('9','1'),('10','1'),('11','0'),('12','0')], 
  ['Time','Tag1'])\
    .withColumn('Time', F.col('Time').cast('integer'))\
    .withColumn('Tag1', F.col('Tag1').cast('integer'))
```

## Advanced Operations

#### Repartitioning

```python
# Repartition – df.repartition(num_output_partitions)
df = df.repartition(1)
```

#### UDFs (User Defined Functions

```python
# Multiply each row's age column by two
times_two_udf = F.udf(lambda x: x * 2)
df = df.withColumn('age', times_two_udf(df.age))

# Randomly choose a value to use as a row's name
import random

random_name_udf = F.udf(lambda: random.choice(['Bob', 'Tom', 'Amy', 'Jenna']))
df = df.withColumn('name', random_name_udf())
```

#### Window Functions

```python
# Take the lastest row for each combination
from pyspark.sql import Window
w = Window.partitionBy("first_name", "last_name").orderBy(F.desc("date")
df.withColumn("row_number", F.row_number().over()))\
  .filter(F.col("row_number") == 1)\
  .drop("row_number")

# Cumulative Sum
from pyspark.sql import Window
w = Window.orderBy('id').rowsBetween(W.unboundedPreceding, 0)
df.withColumn('cumul_sum', F.sum(F.col('value')).over(w))

# Take previous day
from pyspark.sql import Window
w = Window.orderBy('date')
df.withColumn('previous_date', F.lag(F.col('date')).over(w))
```

#### Regular Expressions (RegEx)

```python
# Take whatever is between the parenthesis
df = spark.createDataFrame([('tx=Reach % (YouTube)',)]).toDF("col1")
import pyspark.sql.functions as F
df.withColumn("tx", F.regexp_extract(F.col("col1"), r"\(([\w]+)\)", 1)).show()
```
