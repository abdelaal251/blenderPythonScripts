import bpy
import os
import sys

excel_utils_path = "C://Users/Ahmed Abdelaal/Desktop/python script for blender revolution/vscode scripts/Automation-scripting"
if excel_utils_path not in sys.path:
    sys.path.append(excel_utils_path)
from excel_utils import load_excel_data, filter_objects_by_column

def main(excel_file, sheet_name, filter_column_name, target_column_name, filter_values):
    df = load_excel_data(excel_file, sheet_name)

    object_names_to_show = filter_objects_by_column(df, filter_column_name, filter_values, target_column_name)

    scene = bpy.context.scene

    # Reset visibility of all objects
    for obj in scene.objects:
        obj.hide_viewport = False

    # Iterate through all objects in the scene
    for obj in scene.objects:
        # Check if the object name is in the list from the Excel file
        if obj.name in object_names_to_show:
            # Show the object
            obj.hide_viewport = False
        else:
            # Hide the object
            obj.hide_viewport = True

    print("Objects visibility updated based on the filtered Excel column.")



# Specify the parameters
excel_file = "D://projects/NPC/20221117 3d model/automation phase/new naming templates/namin.xlsx"
sheet_name = "meshes"
filter_column_name = "category"
target_column_name = "objects"
filter_values = ["handrail"]

# Run the main script
main(excel_file, sheet_name, filter_column_name, target_column_name, filter_values)
