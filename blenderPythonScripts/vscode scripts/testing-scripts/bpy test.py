import bpy
import pandas as pd

scene = bpy.context.scene

visibleObjects = 0
invisivleObjects = 0
empties = []
file_path = "C://Users/Ahmed Abdelaal/Desktop/python script for blender revolution/new names.txt"
excel_file_path = "D://projects/NPC/20221117 3d model/automation phase/new naming templates/NamingTemplate.xlsx"
sheet_name = "meshes"

try:
    df = pd.read_excel(excel_file_path, sheet_name)
    print("Excel File Content:")
    print(df)
except Exception as e:
    print("Error reading Excel file:", e)


#for obj in scene.objects:
#    if obj.type == 'MESH':
#        empties.append(obj.name)
        

#with open(file_path, 'w') as file:
#    file.write("List of Empty Objects:\n")
#    for empty in empties:
#        file.write(empty + "\n")

#print("Results written to:", file_path)

#print(empties)

