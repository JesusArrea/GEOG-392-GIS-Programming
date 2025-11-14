import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox."""
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"
        # List the tool class in the toolbox
        self.tools = [Lab5_Tool]

class Lab5_Tool(object):
    def __init__(self):
        """Define the tool properties."""
        self.label = "Lab5_Tool"
        self.description = "Buffers a selected parking garage and clips nearby structures."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define all parameters for the user interface."""
        
        # . Folder location for the new GDB
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdb_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        
        # 1. Name of the new GDB
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="gdb_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        # 2. Input CSV file
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garage_csv_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param2.filter.list = ['csv']

        # 3. Input GDB containing the Structures data
        param3 = arcpy.Parameter(
            displayName="Campus GDB",
            name="campus_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        
        # 4. Name of the specific garage
        param4 = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selected_garage_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        
        # 5. Buffer distance
        param5 = arcpy.Parameter(
            displayName="Buffer Radius (e.g., 150)",
            name="buffer_radius",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )
        
        # 6. Output feature class result
        param6 = arcpy.Parameter(
            displayName="Output Clip Feature Class",
            name="output_clip_fc",
            datatype="DEFeatureClass", 
            parameterType="Derived",
            direction="Output"
        )

        return [param0, param1, param2, param3, param4, param5, param6]

    def isLicensed(self):
        return True
    
    def updateParameters(self, parameters):
        # Calculate the full path to the new GDB
        if parameters[0].value and parameters[1].value:
            gdb_folder = parameters[0].valueAsText
            gdb_name = parameters[1].valueAsText
            full_gdb_path = os.path.join(gdb_folder, gdb_name)
            
            # Set the derived output path for the clip result
            parameters[6].value = os.path.join(full_gdb_path, "clip")
            
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        """The main execution code for the tool."""
        
        # Get parameter values
        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        Campus_GDB = parameters[3].valueAsText
        Selected_Garage_Name = parameters[4].valueAsText
        Buffer_Radius = parameters[5].valueAsText 

        GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)
        
        # Define feature class paths
        garages_name = "garages"
        clip_name = "clip"
        structures = os.path.join(Campus_GDB, "Structures")
        garages = os.path.join(GDB_Full_Path, garages_name)

        arcpy.env.overwriteOutput = True
        
        try:
            # Create the File GDB
            arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
            arcpy.AddMessage(f"Created/Verified GDB at: {GDB_Full_Path}")

            # Note: CSV to Feature Class conversion goes here.
            arcpy.AddMessage("Assuming Garage CSV conversion to 'garages' FC is handled.")
            
            # --- Check if the selected garage exists ---
            where_clause = f"BldgName = '{Selected_Garage_Name}'"
            shouldProceed = False
            
            arcpy.AddMessage(f"Searching for garage: {Selected_Garage_Name}")

            # Use SearchCursor to check for existence
            with arcpy.da.SearchCursor(garages, ["BldgName"], where_clause=where_clause) as cursor:
                for row in cursor:
                    shouldProceed = True
                    break
            
            # --- Run Geoprocessing if Garage Exists ---
            if shouldProceed:
                
                # Define temporary output paths
                garage_selected_name = "garage_selected"
                building_buffed_name = "building_buffed"
                
                garage_selected = os.path.join(GDB_Full_Path, garage_selected_name)
                building_buffed = os.path.join(GDB_Full_Path, building_buffed_name)
                output_clip_fc = os.path.join(GDB_Full_Path, clip_name)

                # Select the garage feature
                arcpy.analysis.Select(garages, garage_selected, where_clause)
                
                # Buffer the selected building
                buffer_distance_unit = f"{Buffer_Radius} Meters"
                arcpy.analysis.Buffer(garage_selected, building_buffed, buffer_distance_unit)
                
                # Clip the structures feature class
                arcpy.analysis.Clip(structures, building_buffed, output_clip_fc)
                
                # Cleanup temporary files
                arcpy.management.Delete(garage_selected)
                arcpy.management.Delete(building_buffed)
                
                # Report success
                arcpy.AddMessage("SUCCESS")
                
                # Set the output parameter value
                parameters[6].value = output_clip_fc 

            else:
                # Report failure
                arcpy.AddError("Seems we couldn't find the building name you entered")
                arcpy.AddError(f"FAILED: Garage '{Selected_Garage_Name}' not found.")
                
        except arcpy.ExecuteError:
            # Handle ArcPy tool errors
            arcpy.AddError("ArcPy Error during execution:")
            arcpy.AddError(arcpy.GetMessages(2))
            return
        except Exception as e:
            # Handle general errors
            arcpy.AddError(f"An unexpected error occurred: {str(e)}")
            return
            
        return# -*- coding: utf-8 -*-
import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox."""
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"
        # List the tool class in the toolbox
        self.tools = [Lab5_Tool]

class Lab5_Tool(object):
    def __init__(self):
        """Define the tool properties."""
        self.label = "Lab5_Tool"
        self.description = "Buffers a selected parking garage and clips nearby structures."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define all parameters for the user interface."""
        
        # 0. Folder location for the new GDB
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdb_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        
        # 1. Name of the new GDB
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="gdb_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        # 2. Input CSV file
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garage_csv_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param2.filter.list = ['csv']

        # 3. Input GDB containing the Structures data
        param3 = arcpy.Parameter(
            displayName="Campus GDB",
            name="campus_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        
        # 4. Name of the specific garage
        param4 = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selected_garage_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        
        # 5. Buffer distance
        param5 = arcpy.Parameter(
            displayName="Buffer Radius (e.g., 150)",
            name="buffer_radius",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )
        
        # 6. Output feature class result
        param6 = arcpy.Parameter(
            displayName="Output Clip Feature Class",
            name="output_clip_fc",
            datatype="DEFeatureClass", 
            parameterType="Derived",
            direction="Output"
        )

        return [param0, param1, param2, param3, param4, param5, param6]

    def isLicensed(self):
        return True
    
    def updateParameters(self, parameters):
        # Calculate the full path to the new GDB
        if parameters[0].value and parameters[1].value:
            gdb_folder = parameters[0].valueAsText
            gdb_name = parameters[1].valueAsText
            full_gdb_path = os.path.join(gdb_folder, gdb_name)
            
            # Set the derived output path for the clip result
            parameters[6].value = os.path.join(full_gdb_path, "clip")
            
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        """The main execution code for the tool."""
        
        # Get parameter values
        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        Campus_GDB = parameters[3].valueAsText
        Selected_Garage_Name = parameters[4].valueAsText
        Buffer_Radius = parameters[5].valueAsText 

        GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)
        
        # Define feature class paths
        garages_name = "garages"
        clip_name = "clip"
        structures = os.path.join(Campus_GDB, "Structures")
        garages = os.path.join(GDB_Full_Path, garages_name)

        arcpy.env.overwriteOutput = True
        
        try:
            # Create the File GDB
            arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)
            arcpy.AddMessage(f"Created/Verified GDB at: {GDB_Full_Path}")

            # Note: CSV to Feature Class conversion goes here.
            arcpy.AddMessage("Assuming Garage CSV conversion to 'garages' FC is handled.")
            
            # --- Check if the selected garage exists ---
            where_clause = f"BldgName = '{Selected_Garage_Name}'"
            shouldProceed = False
            
            arcpy.AddMessage(f"Searching for garage: {Selected_Garage_Name}")

            # Use SearchCursor to check for existence
            with arcpy.da.SearchCursor(garages, ["BldgName"], where_clause=where_clause) as cursor:
                for row in cursor:
                    shouldProceed = True
                    break
            
            # --- Run Geoprocessing if Garage Exists ---
            if shouldProceed:
                
                # Define temporary output paths
                garage_selected_name = "garage_selected"
                building_buffed_name = "building_buffed"
                
                garage_selected = os.path.join(GDB_Full_Path, garage_selected_name)
                building_buffed = os.path.join(GDB_Full_Path, building_buffed_name)
                output_clip_fc = os.path.join(GDB_Full_Path, clip_name)

                # Select the garage feature
                arcpy.analysis.Select(garages, garage_selected, where_clause)
                
                # Buffer the selected building
                buffer_distance_unit = f"{Buffer_Radius} Meters"
                arcpy.analysis.Buffer(garage_selected, building_buffed, buffer_distance_unit)
                
                # Clip the structures feature class
                arcpy.analysis.Clip(structures, building_buffed, output_clip_fc)
                
                # Cleanup temporary files
                arcpy.management.Delete(garage_selected)
                arcpy.management.Delete(building_buffed)
                
                # Report success
                arcpy.AddMessage("SUCCESS")
                
                # Set the output parameter value
                parameters[6].value = output_clip_fc 

            else:
                # Report failure
                arcpy.AddError("Seems we couldn't find the building name you entered")
                arcpy.AddError(f"FAILED: Garage '{Selected_Garage_Name}' not found.")
                
        except arcpy.ExecuteError:
            # Handle ArcPy tool errors
            arcpy.AddError("ArcPy Error during execution:")
            arcpy.AddError(arcpy.GetMessages(2))
            return
        except Exception as e:
            # Handle general errors
            arcpy.AddError(f"An unexpected error occurred: {str(e)}")
            return
            
        return



"""
You can change the `workspace` path as your wish.
"""
"""
Here are some hints of what values the following variables should accept.
When running, the following code section will accept user input from terminal
Use `input()` method.
