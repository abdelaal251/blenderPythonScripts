import bpy

def uv_unwrap_objects(object_names):
    # Iterate over each object in the scene
    for object_name in object_names:
        # Check if the object exists in the scene
        if object_name in bpy.data.objects:
            # Select the object
            bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_name]
            bpy.context.view_layer.objects.active.select_set(True)

            # Switch to Edit mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Unwrap the UVs using Cube Projection
            bpy.ops.uv.cube_project(cube_size=1.0, correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)


            # Switch back to Object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect the object
            bpy.context.view_layer.objects.active.select_set(False)
        else:
            print(f"Object '{object_name}' not found in the scene.")


object_names_to_unwrap = ["Cube", "Cube.001", "Cube.002"]

# Call the UV unwrap function
uv_unwrap_objects(object_names_to_unwrap)
