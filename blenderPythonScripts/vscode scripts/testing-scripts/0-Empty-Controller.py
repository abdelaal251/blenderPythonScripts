import bpy
import pandas as pd


def hide_all_objects():
    for obj in bpy.context.scene.objects:
        obj.hide_set(True)

def show_objects_and_children(object_names):
    for obj_name in object_names:
        obj_name = "/" + obj_name
        obj = bpy.data.objects.get(obj_name)
        if obj:
            obj.hide_set(False)
            for child in obj.children_recursive:
                child.hide_set(False)

def main(excel_file, sheet_name, empty_column, keyword_column, keyword):
    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Filter DataFrame based on the keyword condition
    filtered_df = df[df[keyword_column] == keyword]

    # Get the names of empties
    empty_names = filtered_df[empty_column].astype(str).tolist()

    # Hide all objects in Blender
    hide_all_objects()

    # Show empties and their children
    show_objects_and_children(empty_names)

# Specify the Excel file, sheet, columns, and keyword
excel_file = "D://projects/NPC/20221117 3d model/automation phase/new naming templates/namin.xlsx"
sheet_name = "empties"
empty_column = "Name"
keyword_column = "Type"
keyword = "PIPE"

# Run the main script
main(excel_file, sheet_name, empty_column, keyword_column, keyword)
