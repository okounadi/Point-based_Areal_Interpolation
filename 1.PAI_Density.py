# Name: Density Weighted Point-based Aerial Interpolation
# Description: spatial disaggregation technique that works with point data as control points/ancillary information (0-D)
# Author of the code: O. Kounadi, 25/02/2016

# Reference: This code is part of a code written for a research study that is published in:
# Kounadi, O., Ristea, A., Leitner, M., & Langford, C. (2018).
# Population at risk: using areal interpolation and Twitter messages to create population models for burglaries and robberies.
# Cartography and Geographic Information Science, 45(3), 205-220.

# Note 1. Necessary fields: target- targetID/ source- sourceID, Spop
# Note 2. Copy all input files to a new personal geodatabase
# Note 3. Output file will be saved in the geodatabase
# --------------------------------------------

# Set variables for workspace and paths
workspace = r"D:\density.mdb"
path1= r"D:\density.mdb\targetPoint2"
path2= r"\density.mdb\cs"
path3= r"\density.mdb\targetPoint"
path4= r"\density.mdb\target2"
path5= r"\density.mdb\Fr"

# 1.0 = q: power parameter that controls the degree of local influence - defined by user
w ="[cratio]^ 1.0"

# Set workspace
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# csi: number of control points in target zone i
arcpy.SpatialJoin_analysis("target","control","target2","JOIN_ONE_TO_ONE","KEEP_ALL","pop pop true true false 8 Double 0 0 \
,First,#,target,pop,-1,-1;Shape_Length Shape_Length false true true 8 Double 0 0 \
,First,#,target,Shape_Length,-1,-1;Shape_Area Shape_Area false true true 8 Double 0 0 \
,First,#,target,Shape_Area,-1,-1;targetID targetID true true false 8 Double 0 0 \
,First,#,target,targetID,-1,-1","INTERSECT","#","#")
arcpy.AddField_management("target2","csi","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management("target2","csi","[Join_Count]","VB","#")
arcpy.DeleteField_management("target2","Join_Count;TARGET_FID")

# Transfer source info (source ID, Spop) and control info (csi) to targetPoint
arcpy.FeatureToPoint_management("target2","targetPoint","CENTROID")
arcpy.SpatialJoin_analysis("targetPoint","source","targetPoint2","JOIN_ONE_TO_ONE","KEEP_ALL","pop pop true true false 8 Double 0 0 \
,First,#,targetPoint,pop,-1,-1;targetID targetID true true false 8 Double 0 0 \
,First,#,targetPoint,targetID,-1,-1;csi csi true true false 4 Long 0 0 \
,First,#,targetPoint,csi,-1,-1;ORIG_FID ORIG_FID true true false 4 Long 0 0 \
,First,#,targetPoint,ORIG_FID,-1,-1;sourceID sourceID true true false 8 Double 0 0 \
,First,#,source,sourceID,-1,-1;Spop Spop true true false 4 Long 0 0 \
,First,#,source,Spop,-1,-1;Shape_Length Shape_Length false true true 8 Double 0 0 \
,First,#,source,Shape_Length,-1,-1;Shape_Area Shape_Area false true true 8 Double 0 0 \
,First,#,source,Shape_Area,-1,-1","INTERSECT","#","#")
arcpy.DeleteField_management("targetPoint2","Join_Count;TARGET_FID;ORIG_FID")

# cs: number of control points within all target zones in source zone s
arcpy.Statistics_analysis("targetPoint2","cs","csi SUM","sourceID")
arcpy.AddField_management("cs","cs","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management("cs","cs","[SUM_csi]","VB","#")
arcpy.JoinField_management("targetPoint2","sourceID","cs","sourceID","cs")

# Add fields that are necessary for calculating the equations of:
# 1: Vsi= Estimated value for target zone i within source zone s
# 2: Wsi= weight of target zone i within source zone s 
# 3: As= constant parameter for source zone s
# The necessary fields are: 
# cratio: ratio of csi/cs
# Wsi: cratio ^ q
# As: Spop/ sum(Wsi)
# Vsi: As * Wsi
arcpy.AddField_management("targetPoint2","cratio","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("targetPoint2","Wsi","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("targetPoint2","Vsi","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("targetPoint2","As_","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
# Calculate dratio
arcpy.CalculateField_management("targetPoint2","cratio","[csi] / [cs]","VB","#")
# Calculate Wsi 
arcpy.CalculateField_management("targetPoint2","Wsi", w ,"VB","#")                           
# Calculate As
arcpy.Frequency_analysis("targetPoint2","Fr","sourceID","Wsi")
arcpy.AddField_management("Fr","SumWsi","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management("Fr","SumWsi","[Wsi]","VB","#")
arcpy.JoinField_management("targetPoint2","sourceID","Fr","sourceID","SumWsi")
arcpy.CalculateField_management("targetPoint2","As_","[Spop] / [SumWsi]","VB","#")
# Calculate Vsi
arcpy.CalculateField_management("targetPoint2","Vsi","[As_] * [Wsi]","VB","#")

# Move all values (fields) from the targetPoint to the target polygon file
arcpy.CopyFeatures_management("target","targetNew","#","0","0","0")
arcpy.JoinField_management("targetNew","targetID","targetPoint2","targetID","csi;sourceID;Spop;cs;cratio;Wsi;Vsi;As_;SumWsi")

# Delete unnecessary files
arcpy.Delete_management(path1)
arcpy.Delete_management(path2)
arcpy.Delete_management(path3)
arcpy.Delete_management(path4)
arcpy.Delete_management(path5)

# End of Code
arcpy.RefreshCatalog(workspace)
print "Process completed. The dissagregated variable is named 'Vsi' in file 'targetNew'"