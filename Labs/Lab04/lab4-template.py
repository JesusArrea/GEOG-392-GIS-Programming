
import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

### >>>>>> Add your code here
INPUT_DB_PATH = os.path.join(BASE_DIR, "Lab04_data", "Campus.gdb")
CSV_PATH = os.path.join(BASE_DIR, "Lab04_data", "garages.csv")
OUTPUT_DB_PATH = os.path.join(BASE_DIR, "my_lab04_output.gdb")
### <<<<<< End of your code here

arcpy.env.workspace = INPUT_DB_PATH

# Layers need to be kept
layers_to_keep = ["GaragePoints", "LandUse", "Structures", "Trees"]

# list all feature clases
feature_classes = arcpy.ListFeatureClasses()

# delete other classes
for fc in feature_classes:
    if fc not in layers_to_keep:
        arcpy.management.Delete(fc)

# create GDB management
if not os.path.exists(OUTPUT_DB_PATH):
    ### >>>>>> Add your code here
    arccpy.management.CreateFileGDB(os.path.dirname(OUTPUT_DB_PATH), os.path.basename(OUTPUT_DB_PATH))
    print(f"Created GDB: {OUTPUT_DB_PATH}")
    
    ### <<<<<< End of your code here

# Load .csv file to input GDB
GARAGES_FC = os.path.join(arcpy.env.workspace, "garages_points")

if not arcpy.Exists(GARAGES_FC):
### >>>>>> Add your code here
    arccpy.management.XYTableToPoint(
        in_table=CSV_PATH,
        out_feature_class=GARAGES_FC,
        x_field="LONGITUDE",
        y_field="LATITUDE",
        coordinate_system=arcpy.SpatialReference(4326) # WGS 1984
    )
    print(f"Loaded CSV to {GARAGES_FC}")
### <<<<<< End of your code here




# Print spatial references before re-projection
print(f"Before Re-Projection...")
print(f"garages layer spatial reference: {arcpy.Describe(GARAGES_FC).spatialReference.name}.")
print(f"Structures layer spatial reference: {arcpy.Describe( 'Structures').spatialReference.name}.")



GARAGES_PROJ = os.path.join(arcpy.env.workspace, "garages_proj")
STRUCTURES_PROJ = os.path.join(arcpy.env.workspace, "Structures_proj")


# Re-project
## >>>>>>>>> change the codes below
target_ref = arcpy.SpatialReference(2277)

arcpy.management.Project(
   GARAGES_FC,
   GARAGES_PROJ,
   target_ref
)


# Project Structures and Trees
arccpy.management.Project("Structures", STRUCTURES_PROJ, target_ref)
arccpy.management.Project("Trees", os.path.join(arcpy.env.workspace, "Trees_proj"), target_ref)


## <<<<<<<< End of your code here


# print spatial references after re-projection
print(f"After Re-Projection...")
print(f"garages layer spatial reference: {arcpy.Describe(GARAGES_PROJ).spatialReference.name}.")
print(f"re-projected Structures layer spatial reference: {arcpy.Describe(STRUCTURES_PROJ).spatialReference.name}")





### >>>>>> Add your code here
# Buffer analysis
radiumStr = "150 meters"
BUFFER_FC = os.path.join(OUTPUT_DB_PATH, "garages_buffered")




arccpy.analysis.Buffer(
    in_features=GARAGES_PROJ,
    out_feature_class=BUFFER_FC,
    buffer_distance_or_field=radiusStr,
    dissolve_option="ALL"
)
print(f"Created Buffer Layer: {BUFFER_FC}")

# Intersect analysis
INTERSECT_FC = os.path.join(OUTPUT_DB_PATH, "intersected")




arccpy.analysis.Intersect(
    in_features=[BUFFER_FC, STRUCTURES_PROJ],
    out_feature_class=INTERSECT_FC,
    output_type="INPUT" # Keep the features from the original Structure layer
)
print(f"Created Intersect Layer: {INTERSECT_FC}")


# Output features to the created GDB

