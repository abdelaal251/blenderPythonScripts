import bpy
import bmesh
import logging
import math


    
def delete_objects_by_names(object_names):
    for obj_name in object_names:
        obj = create_blender_object(obj_name)
        if obj is not None:
            delete_recursive(obj)
            #bpy.data.objects.remove(obj, do_unlink=True)
            logging.info(f"object {obj_name} deleted from the scene")
        else:
            logging.info(f"object {obj_name} not found in the scene.")

def check_object_live(obj_name):
    mesh_object = bpy.data.objects.get(obj_name.lstrip('/'))
    if mesh_object.data:
        return True
    else:
        logging.warning(f"Object '{obj_name}' not found in the scene.")
        return False
    
def check_object_live_test(obj_name):
    try:
        mesh_object = bpy.data.objects.get(obj_name.lstrip('/'))
    except:
        mesh_object = None
        
    return mesh_object

    
def create_new_empty(empty_name):
    bpy.ops.object.empty_add(location=(0, 0, 0))
    bpy.context.object.name = empty_name


def print_selected_objects():
    # Get the selected objects
    selected_objects = bpy.context.selected_objects
    # Print the names of selected objects to the console
    for obj in selected_objects:
        print(obj.name)

def uv_unwrap_cube_projection(object_names, pojection_size, progress):
    
    # Log that the function starts 
    logging.info(f"unwrapping process starts")

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select mesh objects in the list
    for obj_name in object_names:
        #create blender object
        blender_object = create_blender_object(obj_name)
        if blender_object and blender_object.type == 'MESH':
            #mesh_object.select_set(True)
            unwrap(blender_object, pojection_size)
        progress.update(1)
    logging.info(f"unwrapping proess ends")
            
           
def unwrap(obj, projection_size):
    obj.select_set(True)
    x = bpy.ops.object.mode_set.poll()
    # Check if the UV map exists in the selected objects
    if x:
        # Check if the active object is a mesh before switching to 'EDIT' mode
        if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
            # Set the mode to Edit
            bpy.ops.object.mode_set(mode='EDIT')
            # Select all geometry in Edit Mode
            bpy.ops.mesh.select_all(action='SELECT')
            # Call the smart project operator
            bpy.ops.uv.cube_project(cube_size=projection_size, correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)
            #Log the unwraping state
            logging.info(f" unwraping completed for object: {obj.name}")
            # Set the mode back to Object
            bpy.ops.object.mode_set(mode='OBJECT')
            
def batch_uv_unwrap_with_batches(object_names, projection_size, progress, batch_size=10):
    """
    Applies UV unwrap with cube projection to objects in batches to reduce mode switching overhead.
    
    Parameters:
    - object_names (list): List of object names to process.
    - projection_size (float): The cube size to use for the UV projection.
    - batch_size (int): Number of objects to process per batch.
    """
    logging.info("Starting batched UV unwrapping process")

    # Calculate the total number of batches needed
    total_batches = math.ceil(len(object_names) / batch_size)
    
    for batch_index in range(total_batches):
        # Define the start and end indices for this batch
        start = batch_index * batch_size
        end = start + batch_size
        batch_objects = object_names[start:end]

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        # Select all objects in the current batch
        objects_to_unwrap = []
        for obj_name in batch_objects:
            obj = bpy.data.objects.get(obj_name)
            if obj and obj.type == 'MESH':
                obj.select_set(True)
                objects_to_unwrap.append(obj)

        # Only proceed if there are objects to unwrap
        if objects_to_unwrap:
            # Set an active object from the batch
            bpy.context.view_layer.objects.active = objects_to_unwrap[0]

            # Switch to Edit Mode for batch processing
            bpy.ops.object.mode_set(mode='EDIT')

            # Select all geometry and apply cube projection
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.cube_project(cube_size=projection_size, correct_aspect=True)
            logging.info(f"UV unwrapping completed for batch {batch_index + 1} of {total_batches}")
            progress.update(batch_size)

            # Switch back to Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
    
    logging.info("Batched UV unwrapping process completed")
    

def link_objects_with_material_categories(object_list, progress):

    # Log function state
    logging.info(f" link objects with material started")

    # Retrieve object names and material name from the dictionary
    object_names = object_list.get('objects', [])
    material_names = object_list.get('materials', [])

    # Assign the material name that will be used
    material_name = material_names[0] if material_names else None

    if material_name is not None:
        # Get the material by name
        material = bpy.data.materials.get(material_name.lstrip('/'))
        if material is not None:
            # Iterate through the provided list of mesh objects
            for object_name in object_names:
                blender_object = create_blender_object(object_name)
                if blender_object:
                    obj = blender_object
                    if obj is not None and obj.type == 'MESH':
                        # Clear any existing materials
                        obj.data.materials.clear()
                        # Link the object to the specified material
                        obj.data.materials.append(material)
                        logging.info(f"material attached to {object_name} - {material_name}")
                        #update progressbar
                        progress.update(1)
                else:
                    logging.debug(f"can't find object {object_name} to attach material ")

    # Log function state
    logging.info(f" link objects with material ended")    


def link_objects_with_material(object_list, material_name, progress):

    # Log the function is started 
    logging.info(f"linking objects material starts")
    
    if material_name is not None:
        # Get the material by name
        material = bpy.data.materials.get(material_name)
        if material is not None:
            # Iterate through the provided list of mesh objects
            for object_name in object_list:
                if object_name:
                    obj = create_blender_object(object_name)
                    if obj is not None and obj.type == 'MESH':
                        # Clear any existing materials
                        obj.data.materials.clear()
                        # Link the object to the specified material
                        obj.data.materials.append(material)
                        #print(f"Object '{object_name}' has material '{material_name}' linked.")
                        logging.info(f"object {object_name} has linked to material {material_name}")
                        progress.update(1)
    logging.info(f"linking objects material ends")
                        

def save_and_purge_memory():
    print("\r\n")
    # Get the current file path
    current_filepath = bpy.data.filepath

    # Save the current Blender file
    if current_filepath:
        bpy.ops.wm.save_as_mainfile(filepath=current_filepath)
        #bpy.types.RenderEngine.free_blender_memory()
        logging.info(f"file saved: {current_filepath}")
    else:
        print("File has not been saved yet.")       



def has_uv_map(mesh_obj):
    # Check if the object is a mesh
    if mesh_obj.type != 'MESH':
        return False

    # Get the mesh data
    mesh_data = mesh_obj.data

    # Check if the mesh data has UV layers
    return bool(mesh_data.uv_layers)

def join_meshes_for_empties(mesh_names, category,progress):

    # Log function state
    logging.info(f"joining meshes for empty stated.")

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')  


    # Ensure there is an active object before attempting to set the object mode
    if bpy.context.view_layer.objects.active is None:
        bpy.context.view_layer.objects.active = bpy.data.objects[mesh_names[0]]

    bpy.ops.object.mode_set(mode='OBJECT')

    selected_objects = []
    old_parent_object = create_blender_object(category)
    new_mesh_name = category
    
    for object_name in mesh_names:

        # Create blender object
        blender_object = create_blender_object(object_name)

        # Check if the object exists
        if blender_object:
            # Select the specified object
            blender_object.select_set(True)
            selected_objects.append(blender_object)

            # Set the active object to the selected object
            bpy.context.view_layer.objects.active = blender_object
            
    # Check if there are selected objects before joining
    if selected_objects:

        #print("pause")
        bpy.ops.object.join()

        # Update the mesh to reflect changes
        bpy.context.view_layer.update()

        # Assing name for the joined mesh
        bpy.context.active_object.name = new_mesh_name

        try:
            # Assign the old name
            old_parent_object.name = old_parent_object.name + ".old"
        except:
            pass
        # check if the name ends with ".001"
        if bpy.context.active_object.name.endswith(".001"):
            bpy.context.active_object.name = bpy.context.active_object.name[:-4]  # Remove the last 4 characters, which are ".001"
        
        logging.info(f"joined mesh named {bpy.context.active_object.name}")
        progress.update(1)
        # Return merged object name
        return bpy.context.active_object.name
    else:
        logging.debug("No valid objects selected for joining.")
    
    # Log function state
    logging.info(f"joining meshes for empty ended.")




def join_meshes(mesh_names, old_parent, progress):

    # Log the function starting
    logging.info(f"joining meshes started")

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')  


    # Ensure there is an active object before attempting to set the object mode
    if bpy.context.view_layer.objects.active is None:
        bpy.context.view_layer.objects.active = bpy.data.objects[mesh_names[0]]

    bpy.ops.object.mode_set(mode='OBJECT')

    selected_objects = []
    old_parent_object = create_blender_object(old_parent)
    new_mesh_name = old_parent + "."
    
    for object_name in mesh_names:

        # Create blender object
        blender_object = create_blender_object(object_name)

        # Check if the object exists
        if blender_object:
            # Select the specified object
            blender_object.select_set(True)
            selected_objects.append(blender_object)

            # Set the active object to the selected object
            bpy.context.view_layer.objects.active = blender_object
            
    # Check if there are selected objects before joining
    if selected_objects:

        # Joing selected meshes
        bpy.ops.object.join()

        # Update the mesh to reflect changes
        bpy.context.view_layer.update()

        # Assing name for the joined mesh
        bpy.context.active_object.name = new_mesh_name

        # Assign the old name
        #old_parent_object.name = old_parent_object.name + ".old"

        # check if the name ends with ".001"
        if bpy.context.active_object.name.endswith(".001"):
            bpy.context.active_object.name = bpy.context.active_object.name[:-4]  # Remove the last 4 characters, which are ".001"
        else:
            logging.info(f"joined mesh name: {bpy.context.active_object.name}")
        
        # Return merged object name
        progress.update(1)
        return bpy.context.active_object.name
    else:
        logging.debug("no objects are selected to be joined")
    # Log the function state
    logging.info(f"joining meshes ended")

def decimate_modifier(mesh_names, progress):

    # Log function state
    logging.info(f"decimating for list started.")

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')  
    
    angle_limit_degrees = 6   # in degrees

    # Iterate through the list of mesh names
    for mesh_name in mesh_names:
        # create blender object to be decimated
        blender_object = create_blender_object(mesh_name)
        #check if the mesh is in the scene
        try:
            if blender_object:
                # Check if the mesh is hidden
                if blender_object.hide_get():
                    logging.debug(f"mesh {mesh_name} is hidden, decimation skipped.")
                    continue  # Skip to the next iteration if the mesh is hidden

                # Select the mesh
                blender_object.select_set(True)

                # Set the active object
                bpy.context.view_layer.objects.active = blender_object

                # Create decimate modifier with planar type and angle limit
                # bpy.ops.object.modifier_add(type='DECIMATE')
                # bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
                # bpy.context.object.modifiers["Decimate"].angle_limit = angle_limit_degrees * (3.14159 / 180.0)
                
                # Apply the decimate modifier
                # bpy.ops.object.modifier_apply({"object": bpy.context.object}, modifier="Decimate")

                # incremnt progress
                progress.update(1)
            else:
                logging.debug(f"this mesh {mesh_name} couldn't be found in the model.")
        except:
            continue


def decimate_modifier_single_mesh(mesh_name, progress):

    # Log the function state
    logging.info(f"decimating function starts for object: {mesh_name}")

    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')

    blender_object = create_blender_object(mesh_name)
    
    angle_limit_degrees = 6   # in degrees
    try:
        # Check if the mesh is hidden
        if blender_object.hide_get():
            logging.debug(f" mesh {mesh_name} is hidden")

        # Select the mesh
        blender_object.select_set(True)

        # Set the active object
        bpy.context.view_layer.objects.active = blender_object
        #bpy.context.scene.objects[mesh_name]

        # Create decimate modifier with planar type and angle limit
        # bpy.ops.object.modifier_add(type='DECIMATE')
        # bpy.context.object.modifiers["Decimate"].decimate_type = 'DISSOLVE'
        # bpy.context.object.modifiers["Decimate"].angle_limit = angle_limit_degrees * (3.14159 / 180.0)
        
        # Apply the decimate modifier
        # bpy.ops.object.modifier_apply({"object": bpy.context.object}, modifier="Decimate")

        # increment the progress
        progress.update(1)
    except:
        logging.debug(f" mesh name: {mesh_name} not found for decimation.")
    
    # Log the function state
    logging.info(f"decimating function ended for object: {mesh_name}")

def create_collection(collection_name):
    # Check if the collection already exists
    if collection_name not in bpy.data.collections:
        # Create a new collection
        new_collection = bpy.data.collections.new(collection_name)
        
        # Link the new collection to the scene
        bpy.context.scene.collection.children.link(new_collection)

        print(f"Collection '{collection_name}' created.")
        return new_collection
    else:
        print(f"Collection '{collection_name}' already exists.")
        return bpy.data.collections.get(collection_name.lstrip('/'))

def create_empty_in_collection(collection_name, empty_name):

    new_collection = bpy.data.collections.new(collection_name)
    if new_collection:
        if empty_name not in bpy.data.objects:
            # Create a new empty object
            bpy.ops.object.empty_add(location=(0, 0, 0))
            new_empty = bpy.context.object
            new_empty.name = empty_name
            new_collection.objects.link(new_empty)

            print(f"Empty object '{empty_name}' created in collection '{collection_name}'.")
        else:
            print(f"Empty object '{empty_name}' already exists in collection '{collection_name}'.")
    else:
        print("you given collection doesn't exist")

def assign_new_parent(mesh_names, parent_name, collection_name, progress):

    # Log the function state
    logging.info(f"assining new parent for list starts")

    #create parent object
    parent_object = create_blender_object(parent_name)
    
    for mesh_name in mesh_names:
        # Create mesh object for the mesh to be assinged as a child
        mesh_object = create_blender_object(mesh_name)
        if mesh_object:
            # Store the original transformation matrix of the mesh object
            original_matrix = mesh_object.matrix_world.copy()

            # Change the parent of the mesh object
            mesh_object.parent = parent_object

            # make the mesh object as active object
            bpy.context.view_layer.objects.active = mesh_object
            
            # add object into collection
            bpy.ops.object.collection_link(collection = collection_name)

            # Apply the original transformation matrix to preserve the transform
            mesh_object.matrix_world = original_matrix

            #increment the progress
            progress.update(1)
        else:
            logging.debug(f" mesh object {mesh_object} not found")
            break
    logging.info(f"Assigning parent for a list finished")

def assign_new_parent_for_one_mesh(mesh_name, parent_name, collection_name, progress):

    # Log the function state
    logging.info(f" assigning new parent for mesh {mesh_name}")

    # Create blender object for the parent object
    parent_object = create_blender_object(parent_name)
    
    # Create blender object for the mesh to be linked
    mesh_object = create_blender_object(mesh_name)

    #check if the mesh object is in the scene
    if mesh_object:

        # Store the original transformation matrix of the mesh object
        original_matrix = mesh_object.matrix_world.copy()

        # Change the parent of the mesh object
        mesh_object.parent = parent_object

        # make the mesh object as active object
        bpy.context.view_layer.objects.active = mesh_object
        
        # add object into collection
        bpy.ops.object.collection_link(collection = collection_name)

        # Apply the original transformation matrix to preserve the transform
        mesh_object.matrix_world = original_matrix
        
        # increment the progress
        progress.update(1)

    else:
        logging.debug(f"mesh object: {mesh_name} not found for assigning new parent.")
    
    # Log the function state 
    logging.debug(f"finished assigning new parent for mesh object")


def check_and_delete_empty_objects(parent_object):

    # Log the function state
    logging.info(f"check and delete empty obejcts starts")

    blender_object = create_blender_object(parent_object)
    bpy.context.view_layer.objects.active = blender_object
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select empty objects under the parent
    if blender_object.children:
        for child_object in blender_object.children:
            if not child_object.data:
                child_object.select_set(True)
                bpy.ops.object.delete()
        logging.info(f"check and delete empty objects ends")

def unwrap_meshes_under_empty(empty_name):

    empty = bpy.context.scene.objects.get(empty_name.lstrip('/'))
    
    # Check if the empty exists and is of type 'EMPTY'
    if empty and empty.type == 'EMPTY':
        #print(f"Processing Empty: {empty.name}")
        
        # Get all meshes linked to the current empty
        meshes = [child for child in empty.children if child.type == 'MESH']
        

def select_childeren_under_empty(empty, childs_list):


    #Log that the function starts
    logging.info(f"selecting child starts under {empty}")

    #print(f"Processing Empty: ")
    blender_object = create_blender_object(empty)
    try:
        # Check if the object exists in bpy.data.objects
        if blender_object is not None:

            if blender_object:
                # Check if the empty has children
                if blender_object.children:
                    # Iterate over each child
                    for child in blender_object.children:
                        # Check if the child is a mesh
                        if child.type == 'MESH':
                            childs_list.append(child.name)
                        # Recursively process nested empties
                        elif child.type == 'EMPTY':
                            select_childeren_under_empty(child.name, childs_list)
                else:
                    logging.info(f"No childs founr for object {empty}")
            else:
                logging.info(f"object if not on the scene {empty}")
        else:
            logging.warning(f" objet {empty} not found in blender data")
    except Exception as e:
        logging.debug(f"an error occured while selecting childs under empty: {empty}")
    logging.info(f"selecting childs ends under {empty}")


def create_blender_object(object_name):
    object_name = str(object_name)
    try:
        # Check if the object_name is a non-empty string
        if not isinstance(object_name, str) or not object_name.strip():
            logging.info("Invalid object name provided. Must be a non-empty string.")
            return None
        
        logging.info(f'object named {object_name} provided to create a blender object for it ')

        # Attempt to find the object by name, with or without a leading '/'
        blender_object = bpy.data.objects.get(object_name) or bpy.data.objects.get("/" + object_name)

        if blender_object:
            logging.info(f"Object '{blender_object.name}' found in the scene and returned.")
            return blender_object
        else:
            logging.info(f"Object '{blender_object.name}' not found in the scene.")
            return None  # Explicitly return None if object isn't found

    except Exception as e:
        logging.error(f"Error while creating Blender object '{object_name}': {e}")
        return None


# Function to rename any existing object with the same name to avoid conflicts
def ensure_unique_name(obj: bpy.types.Object, target_object: bpy.types.Object):
    if not isinstance(target_object, bpy.types.Object):
        raise TypeError(f"Expected target_object to be a Blender Object, but got {type(target_object)} instead.")
    
    # Explicitly store a copy of the target object's name
    target_name = str(target_object.name)
    
    # Find an existing object by the target name
    existing_obj = bpy.data.objects.get(target_name)
    if existing_obj and existing_obj != target_object:
        # Modify the existing object’s name by adding an incrementing suffix until it is unique
        counter = 1
        new_name = f"{target_name}_old_{counter}"
        while new_name in bpy.data.objects:
            counter += 1
            new_name = f"{target_name}_old_{counter}"
        
        # Rename the existing object
        existing_obj.name = new_name
        logging.info(f"Renamed existing object '{target_name}' to '{existing_obj.name}' to avoid conflicts.")
    
    # Assign the target name to obj, ensuring no conflicts
    obj.name = target_name
    target_object.name = target_name
    logging.info(f"Assigned name '{target_name}' to object '{obj.name}'.")


def unlink_from_other_collections(object: bpy.types.Object, collection_name: str):
    # Check if the collection exists
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        logging.warning(f"Error: Collection '{collection_name}' not found.")
        return False
    
    # Flag to track if any unlinking occurred
    unlinked = False

    # Unlink the object from its original collections except the target one
    for col in object.users_collection:
        if col != collection:
            col.objects.unlink(object)
            logging.info(f'Object {object.name} has been unlinked from collection {col.name}')
            unlinked = True

    if unlinked:
        logging.info(f'Unlinking of object {object.name} has been completed.')
        return True
    else:
        logging.info(f'Object {object.name} was only linked to collection {collection_name}, no other unlinking needed.')
        return False


def merge_valve_meshes(valve_empty_name, valve_parent_name, collection_name):
    
    # Get the valve empty object
    valve_empty = create_blender_object(valve_empty_name)
    
    if valve_empty is None or valve_empty.type != 'EMPTY':
        logging.error(f"Error: Valve empty '{valve_empty_name}' not found or is not an EMPTY.")
        return None  # Return None to handle errors
    
    # Check if the collection exists
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        logging.warning(f"Error: Collection '{collection_name}' not found.")
        return None
    
    # Get or create the parent empty object (VALVES_PARENT)
    valve_parent = create_blender_object(valve_parent_name)
    if valve_parent is None:
        valve_parent = bpy.data.objects.new(valve_parent_name, None)  # Create new empty
        collection.objects.link(valve_parent)  # Link the new empty to the collection
        logging.info(f"Created and linked new parent empty: {valve_parent_name}")
    
    # Gather all child meshes under the valve empty
    child_meshes = [child for child in valve_empty.children if child.type == 'MESH']
    
    if not child_meshes:
        logging.info(f"No child meshes found under valve empty '{valve_empty_name}'.")
        return None
    
    # Select all child meshes
    bpy.ops.object.select_all(action='DESELECT')  # Deselect everything first
    for mesh in child_meshes:
        mesh.select_set(True)  # Select each mesh
    bpy.context.view_layer.objects.active = child_meshes[0]  # Set one active object
    
    # Join the selected meshes into a single mesh
    bpy.ops.object.join()
    
    # Get the newly joined mesh object
    joined_mesh = bpy.context.active_object
    
    # Store the original transformation matrix of the joined mesh
    original_matrix = joined_mesh.matrix_world.copy()
    
    # Ensure the new object has a unique name
    ensure_unique_name(joined_mesh, valve_empty)
    
    # Re-parent the joined mesh to the parent empty (VALVES_PARENT)
    joined_mesh.parent = valve_parent
    
    # Restore the original transformation to preserve location, rotation, and scale
    joined_mesh.matrix_world = original_matrix
    
    # Move the joined mesh to the AutomationScript collection (if not already linked)
    if joined_mesh.name not in collection.objects:
        collection.objects.link(joined_mesh)
    
    # Unlink the merged valve from its original collection
    for col in joined_mesh.users_collection:
        if col != collection:
            col.objects.unlink(joined_mesh)
    
    # Use delete_recursive to delete the valve empty and its entire hierarchy
    #delete_recursive(valve_empty)
    
    logging.info(f"Successfully merged and linked valve '{valve_empty_name}' to '{valve_parent_name}' with preserved transformation, and removed the entire original empty hierarchy.")
    return joined_mesh  # Return the joined mesh object for further use

    

def delete_recursive(obj):
    """Recursively delete the object and all of its children."""
    if obj is None:
        return

    # Capture the object's name before deletion for logging
    obj_name = obj.name

    # Delete all children recursively
    for child in obj.children:
        delete_recursive(child)

    # Delete the object itself
    bpy.data.objects.remove(obj, do_unlink=True)

    # Log after deletion using the stored name
    logging.info(f"Deleted '{obj_name}' and its hierarchy.")
