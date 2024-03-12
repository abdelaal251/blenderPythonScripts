import bpy
import csv
import os

# Set the path to the CSV file containing mesh names
csv_file_path = "C:/Users/Ahmed Abdelaal/Desktop/python script for blender revolution/valve lis.csv"

# Set the name of the parent object
parent_name = "valves"

# Check if the parent object exists in the scene
parent_object = bpy.data.objects.get(parent_name)
if not parent_object:
    print("Parent object not found in the scene.")

# Check if the CSV file exists
if not os.path.isfile(csv_file_path):
    print("CSV file not found.")
    

# Read mesh names from the CSV file
mesh_names = []
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) > 0:
            mesh_names.append(row[0])
    print(mesh_names)
try:
    for mesh_name in mesh_names:
        mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH' and obj.name == mesh_name]
        if mesh_objects:
            for mesh_object in mesh_objects:
                # Store the original transformation matrix of the mesh object
                original_matrix = mesh_object.matrix_world.copy()

                # Change the parent of the mesh object
                mesh_object.parent = parent_object

                # Apply the original transformation matrix to preserve the transform
                mesh_object.matrix_world = original_matrix

                
        
except Exception as e:
    print("Error:", str(e))
finally:
    print("Script execution completed.")