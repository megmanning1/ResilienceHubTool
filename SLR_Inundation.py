# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2024-11-23 17:49:14
"""
import arcpy
from arcpy.ia import *
from arcpy.ia import *
from arcpy.sa import *
from arcpy.sa import *
from arcpy.sa import *
from arcpy.sa import *

def Model():  # Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")

    BNP_mosiac_1m = arcpy.Raster("BNP_mosiac_1m")
    BNP_Tidal_DEM_3_ = arcpy.Raster("BNP_Tidal_DEM")
    Input_raster_or_constant_value_2_3_ = 0.3048

    # Process: Plus (3) (Plus) (3d)
    surface_1ft_3_ = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\surface_1ft"
    arcpy.ddd.Plus(in_raster_or_constant1=BNP_Tidal_DEM_3_, in_raster_or_constant2=Input_raster_or_constant_value_2_3_, out_raster=surface_1ft_3_)
    surface_1ft_3_ = arcpy.Raster(surface_1ft_3_)

    # Process: Raster Calculator (5) (Raster Calculator) (ia)
    single_1ft = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\single_1ft"
    Raster_Calculator_5_ = single_1ft
    single_1ft =  Con(BNP_mosiac_1m <= surface_1ft_3_, 1)
    single_1ft.save(Raster_Calculator_5_)


    # Process: Region Group (3) (Region Group) (sa)
    clumped_1ft = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\clumped_1ft"
    Region_Group_3_ = clumped_1ft
    clumped_1ft = arcpy.sa.RegionGroup(single_1ft, "EIGHT", "WITHIN", "NO_LINK", None)
    clumped_1ft.save(Region_Group_3_)


    # Process: Extract by Attributes (5) (Extract by Attributes) (sa)
    lowlying_1ft = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\lowlying_1ft"
    Extract_by_Attributes_5_ = lowlying_1ft
    lowlying_1ft = arcpy.sa.ExtractByAttributes(clumped_1ft, "Count < 1000000")
    lowlying_1ft.save(Extract_by_Attributes_5_)


    # Process: Raster Calculator (6) (Raster Calculator) (ia)
    depth_1ft = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\depth_1ft"
    Raster_Calculator_6_ = depth_1ft
    depth_1ft =  Con(BNP_mosiac_1m <= surface_1ft_3_, surface_1ft_3_ - BNP_mosiac_1m) 
    depth_1ft.save(Raster_Calculator_6_)


    # Process: Extract by Attributes (6) (Extract by Attributes) (sa)
    connect_1ft = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\connect_1ft"
    Extract_by_Attributes_6_ = connect_1ft
    connect_1ft = arcpy.sa.ExtractByAttributes(clumped_1ft, "Count > 1000000")
    connect_1ft.save(Extract_by_Attributes_6_)


    # Process: Extract by Mask (3) (Extract by Mask) (sa)
    con_depth_1ft = "C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb\\con_depth_1ft"
    Extract_by_Mask_3_ = con_depth_1ft
    con_depth_1ft = arcpy.sa.ExtractByMask(depth_1ft, connect_1ft, "INSIDE", "221627.8233 3780773.4727 224415.3247 3783394.4331 PROJCS[\"NAD_1983_2011_UTM_Zone_18N\",GEOGCS[\"GCS_NAD_1983_2011\",DATUM[\"D_NAD_1983_2011\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-75.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]],VERTCS[\"NAVD_1988\",VDATUM[\"North_American_Vertical_Datum_1988\"],PARAMETER[\"Vertical_Shift\",0.0],PARAMETER[\"Direction\",1.0],UNIT[\"Meter\",1.0]]")
    con_depth_1ft.save(Extract_by_Mask_3_)


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(cellSize="1", extent="220246.841639323 3779832.80155198 228673.871126132 3784263.28409885 PROJCS[\"NAD_1983_2011_UTM_Zone_18N\",GEOGCS[\"GCS_NAD_1983_2011\",DATUM[\"D_NAD_1983_2011\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-75.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]],VERTCS[\"NAVD_1988\",VDATUM[\"North_American_Vertical_Datum_1988\"],PARAMETER[\"Vertical_Shift\",0.0],PARAMETER[\"Direction\",1.0],UNIT[\"Meter\",1.0]]", outputCoordinateSystem="PROJCS[\"NAD_1983_2011_UTM_Zone_18N\",GEOGCS[\"GCS_NAD_1983_2011\",DATUM[\"D_NAD_1983_2011\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-75.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]],VERTCS[\"NAVD_1988\",VDATUM[\"North_American_Vertical_Datum_1988\"],PARAMETER[\"Vertical_Shift\",0.0],PARAMETER[\"Direction\",1.0],UNIT[\"Meter\",1.0]]", 
                          scratchWorkspace="C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb", workspace="C:\\Users\\MegManning\\North Carolina Coastal Land Trust\\North Carolina Coastal Land Trust Team Site - GIS\\2024 Stanback Fellowship - Meg Manning\\SLR_Brunswick\\SLR_Brunswick.gdb"):
        Model()
