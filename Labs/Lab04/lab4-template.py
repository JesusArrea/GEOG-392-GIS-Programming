import arcpy
import os

# 1. PATHS AND LICENSES (FIXED)
BASE_DIR = r"C:\Users\jarreaga\Desktop"  # Correct path on Windows Desktop
arcpy.SetProduct("ArcInfo")              # License is active due to open ArcGIS Pro

INPUT_DB_PATH = os.path.join(BASE_DIR, "Campus.gdb")
CSV_PATH = os.path.join(BASE_DIR, "garages.csv")
OUTPUT_DB_PATH = os.path.join(BASE_DIR, "my_lab04_output.gdb")

# 2. CREATE OUTPUT GDB (CLEANED BLOCK)
if not arcpy.Exists(OUTPUT_DB_PATH):
    arcpy.management.CreateFileGDB(os.path.dirname(OUTPUT_DB_PATH), os.path.basename(OUTPUT_DB_PATH))
    print(f"Created GDB: {OUTPUT_DB_PATH}")
else:
    print(f"GDB already exists: {OUTPUT_DB_PATH}")
    
# Clean up any existing layers in the output GDB if you are running the script multiple times
# This is where your original cleanup code would go

# Set the environment workspace to the input GDB
arcpy.env.workspace = INPUT_DB_PATH

# Layers need to be kept
layers_to_keep = ["garages_points", "Structures", "Trees"] 

# 3. LOAD CSV FILE TO INPUT GDB (FIXED arccpy TO arcpy)
GARAGES_FC_NAME = "garages_points"
garages_fc = os.path.join(INPUT_DB_PATH, GARAGES_FC_NAME)

if not arcpy.Exists(garages_fc):
    # 3. Load the CSV file into a Point Feature Class
    arcpy.management.XYTableToPoint(  # CORRECTED: arcpy
        in_table=CSV_PATH,
        out_feature_class=garages_fc,
        x_field="X",
        y_field="Y",
        coordinate_system=arcpy.SpatialReference(4326) 
    )
    print(f"Created Point Feature Class: {garages_fc}")
else:
    print(f"Point Feature Class already exists: {garages_fc}")

# 4. RE-PROJECTION (FIXED: The helper function is good)
structures_fc = os.path.join(INPUT_DB_PATH, "Structures")
trees_fc = os.path.join(INPUT_DB_PATH, "Trees")
target_ref = arcpy.SpatialReference(2277) 

garages_projected_fc = os.path.join(INPUT_DB_PATH, "garages_projected")
structures_projected_fc = os.path.join(INPUT_DB_PATH, "Structures_projected")
trees_projected_fc = os.path.join(INPUT_DB_PATH, "Trees_projected")

def project_if_needed(in_fc, out_fc, target_sr):
    if not arcpy.Exists(out_fc):
        arcpy.management.Project(in_fc, out_fc, target_sr)
        print(f"Re-projected '{os.path.basename(in_fc)}' to '{os.path.basename(out_fc)}'")
    else:
        print(f"Projected FC already exists: {out_fc}")
    return out_fc

garages_proj = project_if_needed(garages_fc, garages_projected_fc, target_ref)
structures_proj = project_if_needed(structures_fc, structures_projected_fc, target_ref)
trees_proj = project_if_needed(trees_fc, trees_projected_fc, target_ref)
print(f"After Re-Projection: {target_ref.name}")

# 5. BUFFER AND INTERSECT ANALYSIS (FIXED arccpy TO arcpy)
radiusStr = "150 meters"
garages_buffer_fc = os.path.join(OUTPUT_DB_PATH, "garages_buffered") 

if not arcpy.Exists(garages_buffer_fc):
    arcpy.analysis.Buffer( # CORRECTED: arcpy
        in_features=garages_proj,
        out_feature_class=garages_buffer_fc,
        buffer_distance_or_field=radiusStr,
        dissolve_option="ALL" 
    )
    print(f"Created Buffer Layer: {garages_buffer_fc}")

intersect_input = [garages_buffer_fc, structures_proj]
intersect_fc = os.path.join(OUTPUT_DB_PATH, "intersected")

if not arcpy.Exists(intersect_fc):
    arcpy.analysis.Intersect( # CORRECTED: arcpy
        in_features=intersect_input,
        out_feature_class=intersect_fc,
        output_type="INPUT"
    )
    print(f"Created Intersect Layer: {intersect_fc}")

# 6. COPY FINAL LAYERS (FIXED arccpy TO arcpy)
output_garages = os.path.join(OUTPUT_DB_PATH, "garages")
output_structures = os.path.join(OUTPUT_DB_PATH, "Structure")

if not arcpy.Exists(output_garages):
    arcpy.management.CopyFeatures(garages_proj, output_garages) # CORRECTED: arcpy

if not arcpy.Exists(output_structures):
    arcpy.management.CopyFeatures(structures_proj, output_structures) # CORRECTED: arcpy

output_trees = os.path.join(OUTPUT_DB_PATH, "Trees")
if not arcpy.Exists(output_trees):
    arcpy.management.CopyFeatures(trees_proj, output_trees) # CORRECTED: arcpy
    
print("\n---  Lab 04 execution complete. Check 'my_lab04_output.gdb' for final features. ---")

print(OUTPUT_DB_PATH)











