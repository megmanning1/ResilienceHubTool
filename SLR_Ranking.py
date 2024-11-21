# Sea Level Rise Ranking 
## Meg Manning - Fall 2024


#Import packages
import pandas as pd
import geopandas as gpd
import arcpy
import os
import rasterio as ras

# Get working directory 
os.getcwd()

# Set acrpy workspace to Data folder
arcpy.env.workspace = "z:\\MP\\DATA\\Model_Inputs\\Threat_Index\\SLR"

# Overwrite output files
arcpy.env.overwriteOutput = True

# Read in files for Plum Creek 
pc_SLR1 = ras.open('.\\SLR_tiffs\\PC_1ft.tfw')
