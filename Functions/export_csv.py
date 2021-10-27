def export_csv(df, fileName, filePath):
  
  filePathDestTemp = filePath + ".dir/" 

  df\
    .repartition(1)\
    .write\
    .save(filePathDestTemp) 

  listFiles = dbutils.fs.ls(filePathDestTemp)
  for subFiles in listFiles:
    if subFiles.name[-4:] == ".csv":
      
      dbutils.fs.cp (filePathDestTemp + subFiles.name,  filePath + fileName+ '.csv')

  dbutils.fs.rm(filePathDestTemp, recurse=True)
