# Meg Manning, Fall 2024
# meg.manning@duke.edu
# Description: Select SLR parameters to model areas of greater resilience.

# Import arcpy
import arcpy
import os

# Set acrpy workspace to Scratch folder 
arcpy.env.workspace = "Z:/MP/Scratch"

# Overwrite output files
arcpy.env.overwriteOutput = True

# Modify feature class to file name
fc = ""

# Make user inputs for SLR, storm surge, soil erodibility, and accretion
SLR_amount = arcpy.GetParameterAsText(0)
storm_surge = arcpy.GetParameterAsText(1)
soil_erodibility = arcpy.GetParameterAsText(2)
soil_accretion = arcpy.GetParameterAsText(3)

# Generate output feature class by splitting path and file name 
base_name = os.path.splitext(fc)[0]
output_fc = f"{base_name}_{SLR_amount}_{}.shp"