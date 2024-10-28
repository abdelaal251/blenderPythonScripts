import bpy
import pandas as pd

def get_all_children_recursive(obj, child_names, child_types, parent_paths, parent_name=""):
    """
    Recursively retrieves all child objects of the given object, linking them with a white material.
    """
    # Loop through each child of the current object
    for child in obj.children:
        # Append child's actual name, type, and its parent path
        child_names.append(child.name)  # Store the exact name
        child_types.append(child.type)
        parent_paths.append(parent_name)  # Track parent path for hierarchy

        # Debug statement to trace child object details
        print(f"Debug: Processing child '{child.name}' of type '{child.type}' under parent '{parent_name}'")

        # Assign white material to the child
        if child.type == 'MESH':
            assign_white_material(child)

        # Recurse into child if it's an empty
        if child.type == 'EMPTY':
            print(f"Debug: Recursing into empty '{child.name}'")  # Debug for recursion
            get_all_children_recursive(child, child_names, child_types, parent_paths, parent_name=child.name)

def assign_white_material(obj):
    """
    Assigns a basic white material to the given object for visual confirmation.
    """
    # Check if a white material already exists, otherwise create one
    material_name = "White_Material"
    if material_name not in bpy.data.materials:
        # Create a new material
        white_material = bpy.data.materials.new(name=material_name)
        white_material.use_nodes = True
        # Set the base color to white
        white_material.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 1, 1, 1)  # RGBA white
        print(f"Debug: Created new white material '{material_name}'")
    else:
        white_material = bpy.data.materials[material_name]
        print(f"Debug: Using existing white material '{material_name}'")
    
    # Assign the white material to the object
    if obj.data.materials:
        # If the object already has materials, replace the first slot with the white material
        obj.data.materials[0] = white_material
        print(f"Debug: Replaced material on object '{obj.name}' with white material")
    else:
        # Otherwise, add a new material slot with the white material
        obj.data.materials.append(white_material)
        print(f"Debug: Assigned white material to object '{obj.name}'")

def list_all_children():
    # Specify the empty object name
    empty_name = "/CDU2/EQUI/AREA_A/HVAC"

    # Get the empty object and check existence
    print(f"Debug: Attempting to get the empty object '{empty_name}'")
    empty_obj = bpy.data.objects.get(empty_name)
    if empty_obj is None or empty_obj.type != 'EMPTY':
        print(f"Error: Object '{empty_name}' not found or is not an EMPTY.")
        return None

    print(f"Debug: Found empty '{empty_name}', starting child retrieval")  # Debug for starting process

    # Initialize lists to store child data
    child_names = []
    child_types = []
    parent_paths = []

    # Start the recursive function to get all children
    get_all_children_recursive(empty_obj, child_names, child_types, parent_paths)

    # Create a DataFrame with the child data
    data = {
        "Object Name": child_names,
        "Type": child_types,
        "Parent Path": parent_paths  # Include parent path for hierarchical reference
    }
    df = pd.DataFrame(data)
    
    # Save the DataFrame to an Excel file on the E drive
    excel_path = "E:/child_objects.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Debug: DataFrame saved to '{excel_path}'")

    # Print the DataFrame to show results
    print("Debug: Final DataFrame with all child objects")
    print(df)
    return df

# Run the function and save results
df = list_all_children()
