import bpy

def remove_all_uv_maps():
    # Iterate through all mesh objects in the scene
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            # Select the object
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)

            # Switch to Edit mode
            bpy.ops.object.mode_set(mode='EDIT')

            # Select all faces
            bpy.ops.mesh.select_all(action='SELECT')

            # Delete all UV maps
            bpy.ops.uv.unwrap(method='RESET')

            # Switch back to Object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect the object
            obj.select_set(False)


# Call the function to remove UV maps
remove_all_uv_maps()
