### Dynamic conditions on PySpark DF

df_source = spark.createDataFrame(
  [
     ('Smith','Bob',100000,'B')
    ,('Barnes','Jim',90000,'B')
    ,('Rogers','Eric',120000,'A')
    ,('Carson','Ben',45000,'C')
  ], ['Emp_LName','Emp_FName','Sal','Sal_Grade']
)
                                           
lst_Conditions = [
    ('Cond_1', 'CASE WHEN Sal = 45000 THEN "E" END'),
    ('Cond_2', 'CASE WHEN Emp_FName = "Bob" THEN "V" END')
]

from pyspark.sql import functions as F

for c in lst_Conditions:
  df_source = df_source.withColumn(c[0], F.expr(c[1]))
  
df_source.show()

+---------+---------+------+---------+------+------+
|Emp_LName|Emp_FName|   Sal|Sal_Grade|Cond_1|Cond_2|
+---------+---------+------+---------+------+------+
|    Smith|      Bob|100000|        B|  null|     V|
|   Barnes|      Jim| 90000|        B|  null|  null|
|   Rogers|     Eric|120000|        A|  null|  null|
|   Carson|      Ben| 45000|        C|     E|  null|
+---------+---------+------+---------+------+------+
