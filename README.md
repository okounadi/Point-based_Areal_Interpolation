# Point-based Areal Interpolation

## Introduction

Areal interpolation implies re-aggregating data from one set of polygons (the source zones) to another set of polygons (the target zones). In spatial disaggregation the target zones are of smaller spatial resolution than the source zones; a downscaling process that aims to maintain consistency and quality of data as much as possible.

_Point-based Areal Interpolation_ uses zero-dimensional (0-D) points as ancillary information that are spatially associated with the variable of interest (i.e. values within polygons to be interpolated/disaggregated). The connection between zonal variables and point locations can be modelled using different functions, so that the information of the target zones is influenced by the spatial distribution of the point locations (also called control points).

When _ancillary information (control points)_ are available at a point resolution (0-D) they pose a significant advantage. Original data can be disaggregated into zonal systems of finer resolutions. Given the fact that there is _spatial heterogeneity_ in various geo-domains at a &quot;micro&quot; level (e.g., crime and health phenomena), trends can be examined at larger scales (i.e. &quot;micro places&quot;).

## To apply the codes you need the following datasets:

1. _Source zones_: a polygon shapefile of the original set of polygons containing the variable whose values are to be disaggregated.

1. _Control points_: a point shapefile that will act as ancillary information for the disaggregation function.

1. _Target zones_: a polygon shapefile of the new set of polygons (smaller units than source zones). These polygons will get the disaggregated variable values.


## A brief description of the codes

1. _PAI\_density_ [_density weighted point-based areal interpolation_]: At first, each target zone is assigned to one source zone using a point-in-polygon operation, where the point is the centre of the target zone and the polygon is the source zone that contains that point. The variable value for each target zone is a function of the ratio of the variable value and the sum of weights of the source zone, and the weight of the target zone within the source zone. The weight is calculated using a density function that assigns weights proportionally to the control points&#39; density in each target zone.

1. _PAI\_distance_ [_distance weighted point-based areal interpolation_]: The process is similar to the one described above but the weights are calculated using a distance instead of a density function [_distance from target zone to the closest control point_ Vs _number of control points within target zone_].


## Further information

- The codes are written in Python and use the ArcPy package: [https://pro.arcgis.com/en/pro-app/arcpy/get-started/what-is-arcpy-.htm](https://pro.arcgis.com/en/pro-app/arcpy/get-started/what-is-arcpy-.htm)

- Data should be in a shapefile format: [https://desktop.arcgis.com/en/arcmap/10.3/manage-data/shapefiles/what-is-a-shapefile.htm](https://desktop.arcgis.com/en/arcmap/10.3/manage-data/shapefiles/what-is-a-shapefile.htm)

- Data should additionally be copied into a personal database (.mdb): [https://desktop.arcgis.com/en/arcmap/latest/manage-data/administer-file-gdbs/create-personal-geodatabase.htm](https://desktop.arcgis.com/en/arcmap/latest/manage-data/administer-file-gdbs/create-personal-geodatabase.htm)


## References

Kounadi, O., Ristea, A., Leitner, M., &amp; Langford, C. (2018). [Population at risk: using areal interpolation and Twitter messages to create population models for burglaries and robberies](https://www.tandfonline.com/doi/pdf/10.1080/15230406.2017.1304243). Cartography and Geographic Information Science, 45(3), 205-220.

Zhang, C., &amp; Qiu, F. (2011). [A point-based intelligent approach to areal interpolation](https://www.tandfonline.com/doi/abs/10.1080/00330124.2010.547792). The Professional Geographer, 63(2), 262-276.
