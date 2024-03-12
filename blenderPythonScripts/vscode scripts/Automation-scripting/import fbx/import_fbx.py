import bpy
import sys

# Get the FBX file path and the save location from the command line arguments
fbx_file_path = sys.argv[-2]
save_file_path = sys.argv[-1]

# Delete the default cube (optional)
if bpy.context.scene.objects.get('Cube') is not None:
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete() 

# Import the FBX file
bpy.ops.import_scene.fbx(filepath=fbx_file_path)

# Save the Blender file
bpy.ops.wm.save_as_mainfile(filepath=save_file_path)
