def export_csv(  
  fileName: String,
  filePath: String
  ) = {

  val filePathDestTemp = filePath + ".dir/"
  val merstageout_df = spark.sql(merstageout)

  merstageout_df
    .coalesce(1)
    .write
    .option("header", "true")
    .mode("overwrite")
    .csv(filePathDestTemp)
  
  val listFiles = dbutils.fs.ls(filePathDestTemp)

  for(subFiles <- listFiles){
      val subFiles_name: String = subFiles.name
      if (subFiles_name.slice(subFiles_name.length() - 4,subFiles_name.length()) == ".csv") {
        dbutils.fs.cp (filePathDestTemp + subFiles_name,  filePath + fileName+ ".csv")
        dbutils.fs.rm(filePathDestTemp, recurse=true)
      }}} 
