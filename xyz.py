import arcpy
from arcpy import env
env.workspace = "C:/AddXYZ"

# Import KMZ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Name: BatchKML_to_GDB.py
# Description: Converts a directory of KMLs and copies the output into a single fGDB.
#              A 2 step process: first convert the KML files, and then copy the featureclases

# Import system models
import arcpy, os

# Set workspace (where all the KMLs are)
arcpy.env.workspace="C:/AddXYZ"

# Set local variables and location for the consolidated file geodatabase
outLocation = r"C:/AddXYZ/FGDBs/"
MasterGDB = 'ConvertedKMZs.gdb'
MasterGDBLocation = os.path.join(outLocation, MasterGDB)

# Create the master FileGeodatabase
arcpy.CreateFileGDB_management(outLocation, MasterGDB)

# Convert all KMZ and KML files found in the current workspace
for kmz in arcpy.ListFiles('*.KM*'):
  print ("CONVERTING: {0}".format(os.path.join(arcpy.env.workspace, kmz)))
  arcpy.KMLToLayer_conversion(kmz, outLocation)

# Change the workspace to fGDB location
arcpy.env.workspace = outLocation

# Loop through all the FileGeodatabases within the workspace
wks = arcpy.ListWorkspaces('*', 'FileGDB')
# Skip the Master GDB
wks.remove(MasterGDBLocation)

for fgdb in wks:

  # Change the workspace to the current FileGeodatabase
  arcpy.env.workspace = fgdb

  # For every Featureclass inside, copy it to the Master and use the name from the original fGDB
  featureClasses = arcpy.ListFeatureClasses('*', '', 'Placemarks')
  for fc in featureClasses:
    print ("COPYING: {0} FROM: {1}".format(fc, fgdb))
    fcCopy = os.path.join(fgdb, 'Placemarks', fc)
    arcpy.FeatureClassToFeatureClass_conversion(fcCopy, MasterGDBLocation, fgdb[fgdb.rfind(os.sep)+1:-4])

# Clean up
del kmz, wks, fc, featureClasses, fgdb

# Add XYcoordinates >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Name: AddXY_Example2.py
# Description: Adding XY points to the climate dataset

# Set local variables
in_data= r"C:/AddXYZ/FGDBs/ConvertedKMZs.gdb"
in_features = r"C:/AddXYZ/FGDBs/ConvertedKMZs.gdb/XY_Points"

# Copying data to preserve original dataset
# Execute Copy
arcpy.Copy_management(in_data, in_features)

# Execute AddXY
arcpy.AddXY_management(in_features)

# Add elevation >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import time
import arcpy
arcpy.ImportToolbox("http://elevation.arcgis.com/arcgis/services;Tools/Elevation", "elev")
result = arcpy.SummarizeElevation_elev(r"C:/AddXYZ/FGDBs/ConvertedKMZs.gdb/XY_Points", "#", "#", "False")

while result.status < 4:
    print result.status
    time.sleep(0.2)
print "Execution Finished"

arcpy.CopyFeatures_management(result.getOutput(0), r'C:/AddXYZ/FGDBs/ConvertedKMZs.gdb/XYZ_Points')
