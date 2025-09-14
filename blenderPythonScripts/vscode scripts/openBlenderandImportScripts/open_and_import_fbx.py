import bpy

# Specify the Blender file and FBX file paths
blender_file_path = r"C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\openBlenderandImportScripts\template file.blend"
fbx_file_path = r"C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\openBlenderandImportScripts\template.fbx"

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=blender_file_path)

# Check if "SourceCollection" already exists; if not, create it
if "SourceCollection" not in bpy.data.collections:
    source_collection = bpy.data.collections.new("SourceCollection")
    bpy.context.scene.collection.children.link(source_collection)
else:
    source_collection = bpy.data.collections["SourceCollection"]

# Ensure the main layer collection is accessible
if bpy.context.view_layer and bpy.context.view_layer.layer_collection:
    layer_collection = bpy.context.view_layer.layer_collection
    
    # Function to find and return the layer collection by name
    def find_layer_collection(layer_coll, coll_name):
        """ Recursively search for a layer collection with the given name """
        if layer_coll and layer_coll.name == coll_name:
            return layer_coll
        for layer in layer_coll.children:
            found = find_layer_collection(layer, coll_name)
            if found:
                return found
        return None

    # Find and set "SourceCollection" as the active layer collection
    source_layer_collection = find_layer_collection(layer_collection, "SourceCollection")
    if source_layer_collection:
        bpy.context.view_layer.active_layer_collection = source_layer_collection
    else:
        print("SourceCollection layer not found in view layer.")
else:
    print("View layer or main layer collection not accessible.")

# Import the FBX file into "SourceCollection" with basic settings
bpy.ops.import_scene.fbx(filepath=fbx_file_path)

# Link imported objects to "SourceCollection" only if not already linked
for obj in bpy.context.selected_objects:
    if obj.name not in source_collection.objects:
        source_collection.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)  # Unlink from the main scene collection
    else:
        print(f"Object '{obj.name}' is already in 'SourceCollection'.")

# Enable "AutomationScript" collection if it exists
if "AutomationScript" in bpy.data.collections:
    automation_collection = bpy.data.collections["AutomationScript"]
    automation_collection.hide_viewport = False
else:
    print("AutomationScript collection not found.")

# Print operation completion message
print("Operation completed successfully.")
