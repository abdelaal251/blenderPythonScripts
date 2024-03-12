import bpy

def assign_material_to_object(source_blend_file, material_name, target_object_name):
    # Link/Append the material from the source file to the current scene
    with bpy.data.libraries.load(source_blend_file, link=True) as (data_from, data_to):
        data_to.materials = [mat for mat in data_from.materials if mat == material_name]

    # Get the target object in the current scene
    target_object = bpy.data.objects.get(target_object_name)

    if target_object:
        # Assign the material to the target object
        target_object.data.materials.clear()
        target_object.data.materials.append(bpy.data.materials[material_name])
        print(f"Material '{material_name}' assigned to object '{target_object_name}'")
    else:
        print(f"Error: Object '{target_object_name}' not found in the scene.")

# Example usage
source_blend_file = "path/to/source.blend"  # Replace with the path to your source file
material_name = "MaterialName"  # Replace with the name of the material in the source file
target_object_name = "Cube"  # Replace with the name of the target object in the current scene

assign_material_to_object(source_blend_file, material_name, target_object_name)
