# Name: Distance Weighted Point-based Aerial Interpolation
# Description:  spatial disaggregation technique that works with point data as control points/ancillary information (0-D)
# Author of the code: O. Kounadi, 25/02/2016

# Reference: This code is an implementation the method "point-based intelligent approach" developed and applied in a research study that is published in:
# Zhang, C., & Qiu, F. (2011).
# A point-based intelligent approach to areal interpolation.
# The Professional Geographer, 63(2), 262-276.

# Note 1. Necessary fields: target- targetID/ source- sourceID, Spop
# Note 2. Copy all input files to a new personal geodatabase
# Note 3. Output file will be saved in the geodatabase
# --------------------------------------------

# Set variables for workspace and paths
workspace = r"D:\distance.mdb"
path1= r"D:\distance.mdb\targetPoint2"
path2= r"D:\distance.mdb\Fr"
path3= r"D:\distance1.mdb\dsmax"
path4= r"D:\distance.mdb\targetPoint"

# 1.0 = q: power parameter that controls the degree of local influence - defined by user
w ="(1- [dratio]) ^ 0.2"

# Set workspace
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# Transfer source info (ID and Spop)to targetPoint
arcpy.FeatureToPoint_management("target","targetPoint","CENTROID")
arcpy.SpatialJoin_analysis("targetPoint","source","targetPoint2","JOIN_ONE_TO_ONE","KEEP_ALL","pop pop true true false 8 Double 0 0,First,#,targetPoint\
,pop,-1,-1;targetID targetID true true false 8 Double 0 0 ,First,#,targetPoint,targetID,-1,-1;sourceID sourceID true true false 8 Double 0 0 ,First,#,source\
,sourceID,-1,-1;Spop Spop true true false 4 Long 0 0,First,#,source,Spop,-1,-1","WITHIN","#","#")
arcpy.DeleteField_management("targetPoint2","Join_Count;TARGET_FID;ORIG_FID;OBJECTID_1")

# dsi: distance from target zone i within source zone s to the closest control point
arcpy.Near_analysis("targetPoint","control","#","LOCATION","NO_ANGLE")
arcpy.JoinField_management("targetPoint","NEAR_FID","control","controlID","controlID")
arcpy.DeleteField_management("targetPoint","NEAR_FID")

# dsmax: maximum distance for all target zones within a source zone s
arcpy.MakeQueryTable_management("targetPoint","QueryTable","USE_KEY_FIELDS","#","targetPoint.sourceID #;targetPoint.NEAR_DIST #",
"[NEAR_DIST] in (SELECT MAX ( [NEAR_DIST] ) FROM targetPoint GROUP BY [sourceID] )")
arcpy.TableToTable_conversion("QueryTable",workspace,"dsmax","#","targetPoint_sourceID targetPoint_sourceID true true false 4 Float 0 0 \
,First,#,QueryTable,targetPoint.sourceID,-1,-1;targetPoint_NEAR_DIST targetPoint_NEAR_DIST true true false 8 Double 0 0 \
,First,#,QueryTable,targetPoint.NEAR_DIST,-1,-1","#")
arcpy.AddField_management("dsmax","dsmax","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management("dsmax","dsmax","[targetPoint_NEAR_DIST]","VB","#")
arcpy.JoinField_management("targetPoint","sourceID","dsmax","targetPoint_sourceID","dsmax")

# Add fields that are necessary for calculating the equations of:
# 1: Vsi= Estimated value for target zone i within source zone s
# 2: Wsi= weight of target zone i within source zone s 
# 3: Cs= constant parameter for source zone s
# The necessary fields are: 
# dratio: ratio of dsi/dsmax
# Wsi: (1 - dratio)^ q
# Cs: Spop/ sum(Wsi)
# Vsi: Cs * Wsi
arcpy.AddField_management("targetPoint","dratio","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("targetPoint","Wsi","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("targetPoint","Cs","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("targetPoint","Vsi","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")

# Calculate dratio
arcpy.CalculateField_management("targetPoint","dratio","[NEAR_DIST] / [dsmax]","VB","#")

# Calculate q
arcpy.CalculateField_management("targetPoint","q",q,"VB","#")

# Calculate Wsi and define power parameter (q) that controls the degree of local influence
arcpy.CalculateField_management("targetPoint2","Wsi", w ,"VB","#")

# Calculate Cs
arcpy.Frequency_analysis("targetPoint","Fr","sourceID","Wsi")
arcpy.AddField_management("Fr","SumWsi","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management("Fr","SumWsi","[Wsi]","VB","#")
arcpy.JoinField_management("targetPoint","sourceID","Fr","sourceID","SumWsi")
arcpy.SelectLayerByAttribute_management ("targetPoint2", "NEW_SELECTION",'[SumWsi]= 0')
arcpy.CalculateField_management("targetPoint2","SumWsi",'1')
arcpy.CalculateField_management("targetPoint2","Wsi",'1')
arcpy.SelectLayerByAttribute_management("targetPoint2","CLEAR_SELECTION","#")
arcpy.CalculateField_management("targetPoint","Cs","[Spop] / [SumWsi]","VB","#")

# Calculate Vsi
arcpy.CalculateField_management("targetPoint","Vsi","[Cs] * [Wsi]","VB","#")

# Move all values (fields) from the targetPoint to the target polygon file
arcpy.CopyFeatures_management("target","targetNew","#","0","0","0")
arcpy.JoinField_management("targetNew","targetID","targetPoint","targetID",\
"Spop;sourceID;NEAR_DIST;NEAR_X;NEAR_Y;controlID;dsmax;dratio;Wsi;Cs;Vsi;SumWsi")

# Delete unnecessary files
arcpy.Delete_management(path1)
arcpy.Delete_management(path2)
arcpy.Delete_management(path3)
arcpy.Delete_management(path4)

# End of Code
arcpy.RefreshCatalog(workspace)
print "Process completed. The dissagregated variable is named 'Vsi' in file 'targetNew'"