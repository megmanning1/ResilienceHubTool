#!/usr/bin/env python
# coding: utf-8

# # <u>Sea Level Rise Inundation Tool </u>
# 
# #### Meg Manning -- *Duke University, Fall 2024*
# 
# ► **Description:** this script can be used to identify an area in the coastal plain of North Carolina and assess it's risk to sea level rise. This tool creates three layers of inundation under 1ft, 2ft, and 3ft of SLR. Methods for forecasting sea level rise inundation were taken from the National Oceanic and Atmospheric detailed methology for sea level rise inundation (NOAA, 2017). A threat index tool is in the process of being built to consider different environmental factors, coupled with SLR, including storm surge of category 1-5 hurricanes, flood prone areas, soil erodibility, drainage, and areas of low slope. This tool will use the National Fish and Wildlife Service's Coastal Resilience and Siting Tool (CREST) methodology for calculations (Dobson et al., 2019).

# ### 1. Digital Elevation Model from LiDAR 
# 
# *Download LiDAR point data and process into a 1m DEM.*
# 
# #### LiDAR data must be downloaded following these steps *prior* to running the rest of this script. 
# 
# <u> Step 1: Download LiDAR Data </u> 
# 
# Click the link below to open the Digital Coast Topobathy LiDAR Web Interface: https://coast.noaa.gov/dataviewer/#/lidar/search/ 
# 
# <u>Step 1.1:</u> Zoom in to a scale of at least 1000ft, if not 500ft, and draw a box around the area of interest
# 
# <u>Step 1.2:</u> In the panel on the right, select the most recent *point* data that corresponds to the area of interest
# 
# <u>Step 1.3:</u> Click "Add to Cart" 
# 
# <u>Step 1.4:</u> In your cart, set the following parameters for your point data:
# * Projection = UTM
# * Zone = Zone 18 Range 078W-072W
# * Horizontal Datum = NAD83
# * Horizontal Units = Meters
# * Vertical Datum = NADV88
# * Vertical Units = Meters
# * Output Product = Point
# * Output Format = Points - LAS
# * Data Classes = Ground 
# 
# <u>Step 1.5:</u> Click next, add email, review and submit
# 
# *It may take a few minutes for the data to process but you will recieve an email with the link to download the data. Once it downloads, extract the data to your machine and note the file path.*
# 
# <u> Step 2: Process into a 1m DEM</u> 

# In[107]:


# Load Necessary Packages
import arcpy
import os
from arcpy.ia import *
from arcpy.sa import *
from arcgis.gis import GIS
from arcgis.raster import Raster
from arcpy.sa import Raster as ARCPY_Raster

# Set the workspace 
output_directory = arcpy.GetParameterAsText(0)
#output_directory = arcpy.env.workspace = "z:\MP\Scratch" #used to test script
arcpy.env.overwriteOutput = True


# In[ ]:


# Define LAS data and LAS dataset paths 
las_folder = arcpy.GetParameterAsText(1) 
las_dataset = arcpy.GetParameterAsText(2) 
arcpy.AddMessage(f"Output directory: {output_directory}")
arcpy.AddMessage(f"LAS Folder: {las_folder}")
arcpy.AddMessage(f"LAS Dataset: {las_dataset}")
#las_folder = "z://MP//DATA//Lidar//nc2019_dunex_Job1104540" - used to test script
#las_dataset = "z://MP//DATA//Lidar//nc2019_dunex_Job1104540//nc2019_dunex_Job1104540.lasd"

# Create a LAS Dataset using Create LAS Dataset Tool 
arcpy.management.CreateLasDataset(las_folder, las_dataset)


# In[106]:


# Define output raster (DEM) path 
ground_DEM_output = os.path.join(output_directory,"DEM_1m.tif")


# In[4]:


# Create 1m DEM using LAS Dataset to Raster tool 
arcpy.conversion.LasDatasetToRaster(las_dataset, ground_DEM_output, 
                                    'ELEVATION', 
                                    'BINNING AVERAGE LINEAR', 
                                    'FLOAT', 
                                    'CELLSIZE', 1, 1)
arcpy.AddMessage(f"LAS Dataset successfully created.")
arcpy.AddError(f'LAS Dataset creation failed.')

# In[5]:


DEM_1m = Raster(ground_DEM_output)


# ### 2. Tidal Variability Surface Using Vertical Datum Tool
# 
# *Use the Vertical Datum tidal surface raster provided by NOAA to create a baseline for water surface to add sea level onto. This tool will clip the tidal surface from NOAA (50-100m resolution) to the area of interest. Since this tidal grid is very coarse resolution, in order to get the most accurate projection of SLR, I recommend following the steps in the appendix to create a tidal surface that is higher resolution prior to running the sea level rise inundation model. See the detailed steps in Appendix A.

# In[36]:


# Authenticate ArcGIS Online Account
gis = GIS("home")


# In[ ]:


# For user input 
# gis = GIS("https://www.arcgis.com", "username", "password")


# In[38]:


# Load tidal surface grid from NOAA VDatum 
tidal_url = "https://chs.coast.noaa.gov/htdata/Inundation/SLR/BulkDownload/Tidal_Surfaces/NC_MHHW_GCS_50m_NAVDm.tif"
tidal_raster = Raster(tidal_url)


# In[49]:


# Create output file 
tidal_raster_path = os.path.join(output_directory, "tidal_raster.tif")
#tidal_raster_path
arcpy.AddMessage(f"Tidal raster successfully loaded")

# In[ ]:


# Get the bounding box of the ground DEM to clip to this extent 
desc = arcpy.Describe(DEM_1m)
extent = desc.extent
xmin = extent.XMin
xmax = extent.XMax
ymin = extent.YMin
ymax = extent.YMax

#Save extent to a bounding extent
rectangle_extent = f"{xmin}, {ymin}, {xmax}, {ymax}"
rectangle_extent_clip = f"{xmin} {ymin} {xmax} {ymax}"


# In[53]:


# Use ExtractByRectangle to export raster to local file
extracted_tidal_raster = arcpy.sa.ExtractByRectangle(tidal_raster_path, 
                                                     rectangle_extent)

arcpy.AddMessage(f"Tidal raster successfully exported to {tidal_raster_path}")
# In[ ]:


# Convert the arcgis.raster._layer.Raster object into a arcpy.sa.Raster local object
extracted_tidal_raster.save(tidal_raster_path)


# In[57]:


#Reload the tidal raster as a spatial raster for geoprocessing 
tidal_raster_sa = ARCPY_Raster(tidal_raster_path)


# In[58]:


#type(tidal_raster_sa)


# In[65]:


# Project this into WKID 6347 - same as DEM layer
tidal_projected_output = os.path.join(output_directory, "tidal_raster_NAD83.tif")
UTM_NAD83 = arcpy.SpatialReference(6347)

# Project tidal raster to new crs
arcpy.management.ProjectRaster(tidal_raster_sa,
                               tidal_projected_output,
                               UTM_NAD83)

arcpy.AddMessage(f"Tidal raster successfully projected into {UTM_NAD83}")
# In[66]:


# Create raster output
tidal_NAD83_raster = ARCPY_Raster(tidal_projected_output)


# In[ ]:


# Check CRS of both rasters 
#print(tidal_NAD83_raster.spatialReference, DEM_1m.spatialReference)


# In[ ]:


# Set local parameters 
tidal_clip_output = os.path.join(output_directory, "tidal_raster_clip.tif")


# In[74]:


# Clip tidal raster to area of interest
arcpy.management.Clip(in_raster=tidal_NAD83_raster, 
                      rectangle=rectangle_extent_clip, 
                      out_raster=tidal_clip_output, 
                      in_template_dataset=DEM_1m, 
                      nodata_value="-3.402823e+38", 
                      clipping_geometry="NONE", 
                      maintain_clipping_extent="NO_MAINTAIN_EXTENT")

tidal_clip = ARCPY_Raster(tidal_clip_output)
arcpy.AddMessage(f"Tidal raster successfully clipped to DEM extent.")

# In[ ]:


# load preprocessed tidal surface for test to see if model works 
#tidal_test = Raster("z:\MP\DATA\Tidal_Surface\SP_tidalsurface.tif")
#type(tidal_test)
#DEM_clip_test = os.path.join(output_directory, "DEM_tidal_clip.tif")


# In[ ]:


# Get the bounding box of the ground DEM to clip to this extent 
#desc = arcpy.Describe(tidal_test)
#extent = desc.extent
#xmin = extent.XMin
#xmax = extent.XMax
#ymin = extent.YMin
#ymax = extent.YMax

#Save extent to a bounding extent
#tidal_extent_clip = f"{xmin} {ymin} {xmax} {ymax}"


# In[ ]:


#Clip tidal raster to preprocessed tidal surface raster for test 
#arcpy.management.Clip(in_raster=DEM_1m, 
#                      rectangle=tidal_extent_clip, 
#                      out_raster=DEM_clip_test, 
#                      in_template_dataset=tidal_test, 
#                      nodata_value="-3.402823e+38", 
#                      clipping_geometry="NONE", 
#                      maintain_clipping_extent="NO_MAINTAIN_EXTENT")

#tidal_test_clip = Raster(DEM_clip_test)


# In[ ]:


#DEM_clip_test


# https://github.com/noaa-ocs-hydrography/vyperdatum/blob/main/vyperdatum/points.py
# https://coast.noaa.gov/slrdata/Tidal_Surfaces/URLlist_Tidal_Surfaces.txt
# https://vdatum.noaa.gov/docs/gtx_info.html

# ### 3. Inundation Extent under 1-3ft SLR
# 
# *Use both the DEM in step 1 and the tidal variabliity surface in step 2 to model the desired amount of sea level rise at 1 meter resolution on top of the area of interest. For detailed methods see Detailed Method for Mapping Sea Level Rise Inundation (NOAA, 2017).*

# <u> Iterate through sea level rise of 1ft (0.3048m), 2ft (0.6096m), and 3ft (0.9144m) for area of interest using tidal variability surface.</u>

# In[ ]:


# Load necessary packages 
import arcpy
from arcpy.ia import *
from arcpy.sa import *
import os

# Allow outputs to be overwritten
arcpy.env.overwriteOutput = True

# Check out any necessary licenses.
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("spatial")
arcpy.CheckOutExtension("ImageAnalyst")

# Create function to iterate through SLR of 1-3ft
SLR_values = [0.3048, 0.6096, 0.9144]

# Convert to feet 
SLR_names = {0.3048: "1ft", 0.6096: "2ft", 0.9144: "3ft"}

# If using a higher resolution tidal raster uncomment this script
#tidal_raster_updated = arcpy.GetParameterAsText(3)
#tidal_raster_updated_path = os.path.join(output_directory, tidal_raster_updated)
#tidal_high_res = Raster(tidal_raster_updated_path)

# Load local tidal surface in 

# Create a function to process inundation for all SLR values 
def process_inundation(SLR_value, DEM_1m, output_directory) :
    # Add SLR amount to surface 
    surface_raster = tidal_clip + SLR_value
    surface_raster_output = os.path.join(output_directory, f'surface_{SLR_value}m.tif')
    surface_raster.save(surface_raster_output)

    # Load ground DEM as Raster 
    input_con = DEM_1m

    # Raster Calculator - create single value DEM to show inundation extent
    single = Con(input_con <= surface_raster, 1)
    single_output = os.path.join(output_directory, f'single_{SLR_value}m.tif')
    single.save(single_output)

    # Region Group - Evaluate connectivity of extent raster using region group
    clumped = arcpy.sa.RegionGroup(single, "EIGHT", "WITHIN", "NO_LINK", None)
    clumped_output = os.path.join(output_directory, f'clumped_{SLR_value}m.tif')
    clumped.save(clumped_output)

    # Extract by Attributes - Extract connected inundation surface to be used as a mask for the original depth grid
    lowlying = arcpy.sa.ExtractByAttributes(clumped, "Count < 10000")
    lowlying_output = os.path.join(output_directory, f'lowlying_{SLR_value}m.tif')
    lowlying.save(lowlying_output)

    # Raster Calculator (2) - Subtract DEM values from water surface to derive initial inundatino depth grid
    depth =  Con(input_con <= surface_raster, surface_raster - input_con) 
    depth_output = os.path.join(output_directory, f'depth_{SLR_value}m.tif')
    depth.save(depth_output)
    
    # Extract by Attributes (2) - Derive low-lying areas 
    connect = arcpy.sa.ExtractByAttributes(clumped, "Count > 10000")
    connect_output = os.path.join(output_directory, f'connect_{SLR_value}m.tif')
    connect.save(connect_output)

    # Extract by Mask - Create depth grid for connected areas
    SLR_in_feet = SLR_names[SLR_value]
    con_depth = arcpy.sa.ExtractByMask(depth, connect)
    con_depth_output = os.path.join(output_directory, f'SLR_Inundation_{SLR_in_feet}.tif')
    con_depth.save(con_depth_output)

    print(f"Processed SLR = {SLR_value}m, saved as {con_depth_output}")

# Iterate through each SLR value (1ft, 2ft, 3ft)
for SLR_value in SLR_values:
    process_inundation(SLR_value, DEM_1m, output_directory)
arcpy.AddMessage(f"SLR inundation successfully forecasted. Outputs stored in {output_directory}.")

# ### Appendix A: Steps to build a higher resolution tidal surface using VDatum Tool & ArcGIS Pro
# 
# *For a description of the metadata of NOAA's Tidal Surfaces use this link to the Digital Coast Sea Level Rise Viewer: https://coast.noaa.gov/slrdata/Tidal_Surfaces/index.html*
# 
# ► **Description:** The use of a vertical datum is critical when mapping sea level rise since it ensures any rise in water levels are accurately referenced to a consistent vertical datum. A vertical datum is a reference system that is used to measure elevations or depths on the Earth's surface. NAVD88 is the most commonly used vertical datum and it is what is used through this model. For the purposes of creating a tidal variability surface in this analysis, a vertical datum transformation using point values in MHHW transformed to NAVD88 was employed to extract nuances in tidal surfaces at the area of interest. By creating point values with a value of 0 for MHHW, the VDatum tool could transform these points into NAVD88 in the appropriate value that corresponds to an assumed water level of 0 meters at a given location. By extrapolating these tidal changes across the entire area of interest, an accurate tidal variability surface was created that could then act as the baseline for mapping a desired SLR projection. 
# 
# 
# <u> Step 1:</u> Create point features across area of interest
# * Use the *Create Features* tool to create a series of points along coastline
# * Only 10-20 points are needed and can be made in a grid pattern across water
# 
# <u> Step 2:</u> Use *Calculate Geometry Attributes* to create field for x, y fields
# * Input Features = point features 
# * Field (Exisiting or New) = x ; Property = Point x-coordinate
# * Repeat to create field for y ; Property = Point y-coordinate
# 
# <u> Step 3:</u> Create field for z values from gridcode and calculate value of 0 MHHW
# * *Calculate Field* for the attribute *grid_code* to equal 0
# 
# <u> Step 4:</u> Save the resulting table as a .csv file
# * Use *Export Table* to export the attribute table as a csv
# * Input Table = point features 
# * Output Table = location to folder for table - *make sure to extension .csv*
# 
# <u> Step 5:</u> Using the VDatum interface, imput csv to transform points into NAVD88
# * Follow this link to the online interface for VDatum: https://vdatum.noaa.gov/vdatumweb/
# 
# * Region = "Contiguous United States"
# 
# * Source Reference Frame:
#     * Reference System = "NAD83(2011)"
#     * Coor. System = "Projected UTM (Easting, Northing)" 
#     * Unit = "meter (m)"
#     * Zone = "18"
# 
# * Target Reference Frame:
#     * Reference System = "NAD83(2011)"
#     * Coor. System = "Projected UTM (Easting, Northing)" 
#     * Unit = "meter (m)"
#     * Zone = "18"
# 
# * Vertical Information 
#     * Source Reference Frame: "MHHW", Unit = "meter (m)"
#     * Target Reference Frame: "NAVD88", Unit = "meter (m)"
# 
# * *Click "ASCII File Conversation"*
#     * File Name: *map to path of .csv table*
#     * Delimiter: *leave as comma, or change if you'd like the output to include a space*
#     * Easting (longitude) = x column, input "2"
#     * Northing (latitude) = y column, input "3"
#     * Height (grid_code) = z column, input "1"
#     * Skip (lines) = "0"
#     * Click *Save to a New Filename and map to appropriate folder, saving as .csv*
# 
# * Click *Transform*
# 
# <u> Step 6:</u> Take transformed point values and add them back into AcrGIS Pro
# * Use the *Table to Point* tool to add the x, y, z values to the map 
#     * x = "x"
#     * y = "y" 
#     * z = "*grid_code*"
# 
# <u> Step 7:</u> Create a raster surface from the point features 
# * Use *Point to Raster* to create a surface from transformed point values 
#     * Value field = "grid_code" (elevation)
#     * Cell Size = "1" (matches the DEM)
# 
# <u> Step 8:</u> Add the new tidal variability surface to the map
# * To use this newly created tidal surface, use *Export Raster* to map to the folder where the DEM is saved 
# * This new tidal surface can then be used to replace the entire North Carolina Grid used in the model above 
# 

# ### REFERENCES
# 
# #### Dobson, G., Johnson, I., Rhodes, K., Hutchins, M., & Chesnutt, M. (2019). Regional coastal resilience assessment: Methodology. National Fish and Wildlife Foundation. Retrieved November 21, 2024, from https://www.nfwf.org/sites/default/files/coastalresilience/Documents/regional-coastal-resilience-assessment.pdf
# 
# #### National Oceanic and Atmospheric Administration (NOAA), Office for Coastal Management. "NOAA Digital Coast Sea Level Rise and Coastal Flooding Impacts Viewer." Retrieved December 6, 2024, https://coast.noaa.gov/slr/.
# 
# #### National Oceanic and Atmospheric Administration. (2017, January). Sea level rise inundation methods: Technical documentation. NOAA Office for Coastal Management. Retrieved November 21, 2024, from https://coast.noaa.gov/data/digitalcoast/pdf/slr-inundation-methods.
# 
