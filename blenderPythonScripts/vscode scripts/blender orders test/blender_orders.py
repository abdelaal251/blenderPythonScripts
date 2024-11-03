# blender_orders.py
import csv
import bpy
import sys
import os
import logging
import pandas as pd
from tqdm import tqdm
import argparse

# Parse command-line arguments
if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]
else:
    argv = []

parser = argparse.ArgumentParser(description='Blender Python Script')
parser.add_argument('--module_dir', required=True, help='Directory containing the modules')
parser.add_argument('--component_excel_path', required=True, help='Path to the component Excel file')
parser.add_argument('--logging_path', required=True, help='Path to the logging file')
args = parser.parse_args(argv)

# Add the directory containing your modules to sys.path
module_dir = args.module_dir
sys.path.append(module_dir)

# Load the Excel file that contains valves
component_excel_path = args.component_excel_path

# Logging file path
logging_path = args.logging_path


# Identify logging settings
# Configure the logging settings
logging.basicConfig(filename=logging_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Mention new collection for blender automation excution
collection_name = "AutomationScript"
equipment_parent_name = "EQUI"
piping_parent_name = "PIPE"
valves_oparent_name = "valves"
parent_name = "civ"

# import needed funtions from other classess
from config import DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD
from sql_connection import connect_to_database, close_database_connection, retrieve_data

from alive_progress import alive_bar
from blender_actions import (batch_uv_unwrap_with_batches, delete_objects_by_names, 
                             check_object_live, 
                             create_new_empty, 
                             uv_unwrap_cube_projection, 
                             link_objects_with_material, 
                             join_meshes, 
                             decimate_modifier,
                             create_collection,
                             create_empty_in_collection,
                             assign_new_parent,
                             select_childeren_under_empty,
                             assign_new_parent_for_one_mesh,
                             decimate_modifier_single_mesh,
                             create_blender_object,
                             check_and_delete_empty_objects,
                             link_objects_with_material_categories,
                             join_meshes_for_empties,
                             save_and_purge_memory,
                             merge_valve_meshes, 
                             ensure_unique_name)


def execute_commands_for_category(category, data):
    if category == 'dublicated':
        perform_action_for_category_duplicated(data)

    # Ordering is important while implementing steps into these categories
    elif category == 'foundation' or category == 'gaugeLadder' or category == 'ground' or category == 'handrail' or category == 'panel' or category == 'stair' or category == 'steel':
        perform_action_for_category_misc(data, category)


# dublicated category steps
def perform_action_for_category_duplicated(data):
    print(f"")

    # Delete Objects
    delete_objects_by_names(data['objects'])

    # Save changes
    save_and_purge_memory()

    #... add more steps if needed



def perform_action_for_category_misc(data, category):

    logging.info(f"perform action for category {category}")
    print(f"\n perform action for category {category}")
    print(f"{category} data for {data}\n")
    # UV projection size // default 2.0
    pojection_size = 600
    new_mesh_name = "civil"
    length_for_progress_bar = len(data['objects'])
    print("\r\n")
    # Initializing progress bars
    with tqdm(total=length_for_progress_bar, desc="UV Progress", unit="objects") as uv_progress_bar, \
            tqdm(total=length_for_progress_bar, desc="Assigning Material", unit="objects") as assign_material_progress, \
            tqdm(total=1, desc="Combining Meshes", unit="objects") as combining_meshes_progress, \
            tqdm(total=1, desc="Assigning New Parent", unit="objects") as assign_parent_progress, \
            tqdm(total=1, desc="Decimation", unit="objects") as decimation_progress:

        print("\r\n")
        # Make UVUnwrap using cube projection method
        #uv_unwrap_cube_projection(data['objects'], pojection_size, uv_progress_bar)
        
        # Make UVUnwrap using cube projection method in batchs!
        batch_uv_unwrap_with_batches(data['objects'], pojection_size, uv_progress_bar)

        #assign material to list of objects 
        link_objects_with_material_categories(data,assign_material_progress)

        #join meshes and rename the final object
        joined_mesh = join_meshes_for_empties(data['objects'], category,combining_meshes_progress)

        # Assign new parent
        assign_new_parent_for_one_mesh(joined_mesh,parent_name,collection_name,assign_parent_progress)
        

        # Apply decimation
        #decimate_modifier_single_mesh(joined_mesh,decimation_progress)

        # Close progressBar
        uv_progress_bar.close()
        assign_material_progress.close()
        combining_meshes_progress.close()
        assign_parent_progress.close()
        decimation_progress.close()

        # Save changes
        save_and_purge_memory()

def perform_action_for_valves(valves):

    print("perform action for valves")

    #assign name for the empty parent for all valves
    parent_empty = "valves"

    # Create empty named as the parent empty
    #create_empty_in_collection(collection_name, parent_empty)

    # Assing all valves to the new parent
    #assign_new_parent(valves, parent_empty, collection_name)

    # Save changes
    #save_and_purge_memory()

def perform_action_for_pipes_and_valves(pipes, valves):
    # Log function state
    logging.info(f"perform action for pipes and valves.")
    
    # UV projection size // default 2.0
    pojection_size = 600

    # Default material for piping and valves
    material_name = "00-piping grey"

    # Valves with slash
    valves_with_slash = ['/' + valve for valve in valves]

    # Counters maximum limits
    no_of_pipes = len(pipes)
    no_of_valves = len(valves)

    # counters initialization
    i = 0
    j = 0

    # Progress bars for various steps
    with tqdm(total=no_of_pipes, desc="UV Progress", unit="objects") as uv_progress_bar, \
        tqdm(total=no_of_pipes, desc="Assigning Material", unit="objects") as assign_material_progress, \
        tqdm(total=1, desc="Combining Meshes", unit="objects") as combining_meshes_progress, \
        tqdm(total=1, desc="Assigning New Parent for pipe", unit="objects") as assign_parent_progress, \
        tqdm(total=1, desc="Assigning New Parent for valves", unit="objects") as assign_parent_progress_valves, \
        tqdm(total=1, desc="Decimation", unit="objects") as decimation_progress, \
        tqdm(total=no_of_valves, desc="Decimation for valves", unit="objects") as decimation_progress_valves:
    
        

        # Step 1: Process each pipe after the valve meshes have been merged
        for pipe in pipes:
            i += 1
            logging.info(f"Processing pipe {pipe} // {i} of {no_of_pipes}")
            
            # try to get pipe with same name as it is
            blender_object = create_blender_object(pipe)

            
            if blender_object:
                # Check if the pipe object is visible
                if not blender_object.hide_get():
                    child_list = []  # List to store child meshes
                    
                    # Select child meshes
                    select_childeren_under_empty(pipe, child_list)
                    
                    # UV unwrap all child meshes
                    #uv_unwrap_cube_projection(child_list, pojection_size, uv_progress_bar)
                    
                    # Make UVUnwrap using cube projection method in batchs!
                    batch_uv_unwrap_with_batches(child_list, pojection_size, uv_progress_bar)

                    # Assign material to the child meshes
                    link_objects_with_material(child_list, material_name, assign_material_progress)
            else:
                logging.debug(f"Pipe {pipe} not found in the scene.")
        
        # Step 2: Merge valve meshes before processing pipes
        for valve in valves:
            # Call the valve merging function before doing any pipe processing
            logging.info(f"Merging valve meshes for {valve}.")

            valve_empty_object = create_blender_object(valve)
            merge_valve_meshes(valve_empty_object, valves_oparent_name, collection_name)

        
        for pipe in pipes:
            
            # List to store child meshes
            child_list = []  
                    
            # Select child meshes
            select_childeren_under_empty(pipe, child_list)

            # create list of piping items underneathe the pipe we are looping for
            piping_list = [item for item in child_list if item not in valves and item not in valves_with_slash]
            
            # increase counter by 1 for each loop
            j += 1
            logging.info(f"Processing pipe {pipe} // {i} of {no_of_pipes} joining an assigning new parent")
            if piping_list:
                new_joined_mesh = join_meshes(piping_list, pipe, combining_meshes_progress)
                print(f"new joined mesh is {new_joined_mesh}")
                
                # Assign new parent to the joined mesh
                assign_new_parent_for_one_mesh(new_joined_mesh, piping_parent_name, collection_name, assign_parent_progress)
            else:
                logging.debug(f"No valid meshes found for joining for pipe {pipe}.")
            save_and_purge_memory()

        # Final steps: assign parents for valves, save progress, etc.
        assign_new_parent(valves, valves_oparent_name, collection_name, assign_parent_progress_valves)
        check_and_delete_empty_objects(valves_oparent_name)
        save_and_purge_memory()

    # Close Progress Bars
    uv_progress_bar.close()
    assign_material_progress.close()
    combining_meshes_progress.close()
    assign_parent_progress.close()
    assign_parent_progress_valves.close()
    decimation_progress.close()
    decimation_progress_valves.close()

    logging.info(f"Performed action for pipes and valves completed.")


def rename_blender_object(equi_object, new_name):
    # This function uses Blender's API to rename the object
    if new_name.startswith('/'):
        new_name = new_name[1:]
    equi_object.name = new_name
    return new_name

def perform_action_for_equi_testing_only(equipments, output_csv='D:/projects/NPC/20221117 3d model/automation phase/cdu1b/equipment_output2.csv'):
    # counter for the logging 
    i = 1
    logging.debug(f"searching for equipments started: {len(equipments)}")
    
    output_data = []
    
    for equi in equipments:
        i += 1
        logging.debug("equipment number in sheet, equipment name in sheet, equipment name in model")
        
        equi_object = create_blender_object(equi)
        new_equi = equi  # Default to original name
        found_in_model = False
        
        if equi_object:
            found_in_model = True
        else:
            if '-' in equi:
                parts = equi.split('-')
                if len(parts) == 2 and parts[1].startswith('0'):
                    # Remove zero if found after the minus
                    new_equi = parts[0] + '-' + parts[1][1:]
                    equi_object = create_blender_object(new_equi)
                    if equi_object:
                        found_in_model = True
                        rename_blender_object(equi_object, equi)
                elif len(parts) == 2 and not parts[1].startswith('0'):
                    # Add zero if not found after the minus
                    new_equi = parts[0] + '-' + '0' + parts[1]
                    equi_object = create_blender_object(new_equi)
                    if equi_object:
                        found_in_model = True
                        rename_blender_object(equi_object, equi)
        
        if not equi_object:
            equi_object = 'notFound'
        
        logging.debug(f"{i},{equi},{equi_object}")
        if new_equi == equi:
            output_data.append([i, equi, equi_object, "", found_in_model])
        else:
            output_data.append([i, equi, equi_object, new_equi, found_in_model])
    
    # Write to CSV
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Equipment Name", "Equipment Object", "New Equipment Name", "Found In Model"])
        writer.writerows(output_data)
    save_and_purge_memory()


# Perform actions for all equipment list 
def perform_action_for_equi(equipments):

    # Log function state
    logging.info(f"performing action for equi started")
    print("performing action for equi started")

    # UV projection size // default 2.0
    pojection_size = 600

    # Material name
    material_name = "00-EQUIPMENTS"

    # print number of equipments
    no_of_equipments = len(equipments)

    # Counter
    i = 0
    print("\r\n")
    # Initializing progress bars
    with tqdm(total=no_of_equipments, desc="UV Progress", unit="objects") as uv_progress_bar, \
            tqdm(total=no_of_equipments, desc="Assigning Material", unit="objects") as assign_material_progress, \
            tqdm(total=1, desc="Combining Meshes", unit="objects") as combining_meshes_progress, \
            tqdm(total=1, desc="Assigning New Parent for pipe", unit="objects") as assign_parent_progress, \
            tqdm(total=1, desc="Decimation", unit="objects") as decimation_progress:
        print("\r\n")
        # do for each equipment
        for equi in equipments:
            # Inrease counter by 1
            i += 1 

            logging.info(f"##############################################   {equi}  // {i} of {no_of_equipments}    ##################")
            
            # Create blender object
            blender_object = create_blender_object(equi)

            if blender_object:
                
                #check if the equipment is visivle
                if not blender_object.hide_get():

                    # initiate new list to contains meshes inside the equipment
                    child_list = []

                    # select all childerens
                    select_childeren_under_empty(equi, child_list)
                    

                    #unwrap all meshes
                    uv_unwrap_cube_projection(child_list, pojection_size, uv_progress_bar)
                    
                    # Assign material
                    link_objects_with_material(child_list, material_name, assign_material_progress)

                    # Joing all meshes
                    new_joined_mesh = join_meshes(child_list,equi, combining_meshes_progress)
                    

                    # assign new parent
                    assign_new_parent_for_one_mesh(new_joined_mesh, equipment_parent_name, collection_name, assign_parent_progress)
            else:
                logging.debug(f"equipment {equi} not found in the scene.")
            
            # decimate equipment mesh
            #decimate_modifier_single_mesh(new_joined_mesh, decimation_progress)

            # save the current state
            save_and_purge_memory()
        #End ProgressBar
        uv_progress_bar.close()
        assign_material_progress.close()
        combining_meshes_progress.close()
        assign_parent_progress.close()
        decimation_progress.close()
        # Log function state
        logging.info(f"performing action for equi ended")




def perform_action_for_piping_equi_valves(data):
    print("performing action in piping, equipments and valves region")

def test_equipments_names():
    equipments = []
    df = pd.read_excel(component_excel_path)
    equipments = df.loc[df['Type'] == 'EQUI', 'Name'].tolist()
    perform_action_for_equi_testing_only(equipments)
    
def assign_categories():
    # Log function state
    logging.info(f"Assigning categories based on model suffix.")
    
    # Connect to the SQL Server database
    conn, cursor = connect_to_database()

    # Retrieve data from the table
    rows = retrieve_data(cursor)

    # Initialize dictionary to organize objects by category
    category_lists = {}

    for row in rows:
        id_, category, suffix, material = row
        if category not in category_lists:
            category_lists[category] = {'objects': [], 'keywords': set(), 'materials': []}

        # Split the suffixes and strip whitespace
        suffixes = [s.strip() for s in suffix.split(',')]

        # Iterate through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object is a mesh and matches any suffix in the list
            if obj.type == 'MESH' and any(sfx in obj.name for sfx in suffixes):
                # Add the matching mesh itself
                category_lists[category]['objects'].append(obj.name)
                keywords = [keyword.strip() for keyword in obj.name.split(',')]
                category_lists[category]['keywords'].update(keywords)
                category_lists[category]['materials'].append(material)
                
                # Retrieve all child meshes of this matching mesh
                all_child_meshes = get_all_child_meshes_recursive(obj)
                
                # Add each child mesh to the category
                for child_mesh in all_child_meshes:
                    category_lists[category]['objects'].append(child_mesh.name)
                    child_keywords = [keyword.strip() for keyword in child_mesh.name.split(',')]
                    category_lists[category]['keywords'].update(child_keywords)
                    category_lists[category]['materials'].append(material)

            # Check if the object is an empty and matches any suffix
            elif obj.type == 'EMPTY' and any(sfx in obj.name for sfx in suffixes):
                # Retrieve all child meshes recursively
                matched_meshes = get_all_child_meshes_recursive(obj)

                # Add all matched child meshes to the category
                for mesh in matched_meshes:
                    category_lists[category]['objects'].append(mesh.name)
                    keywords = [keyword.strip() for keyword in mesh.name.split(',')]
                    category_lists[category]['keywords'].update(keywords)
                    category_lists[category]['materials'].append(material)

    # Execute commands for each category
    for category, data in category_lists.items():
        logging.info(f"Executing commands for {category} category.")
        logging.debug(f"Data for category {category}: {data}")
        #execute_commands_for_category(category, data)

    # Close the connection
    close_database_connection(conn)

    # Initialize lists for valves, equipment, and pipes
    valves = []
    equipments = []
    pipes = []

    # Get lists from the given Excel sheet
    df = pd.read_excel(component_excel_path)
    valves = df.loc[df['Type'] == 'VALV', 'Name'].tolist()
    equipments = df.loc[df['Type'] == 'EQUI', 'Name'].tolist()
    pipes = df.loc[df['Type'] == 'PIPE', 'Name'].tolist()
    logging.info(f"valves extracted {valves}")
    logging.info(f"pipes extracted {pipes}")

    # Perform actions for equipment, pipes, and valves
    #perform_action_for_equi(equipments)
    perform_action_for_pipes_and_valves(pipes, valves)

    # Final log statement
    logging.info(f"Finished assigning categories for model suffixes.")

def get_all_child_meshes_recursive(obj):
    """
    Recursively retrieves all child meshes under a given object, regardless of suffix.
    This is used to collect all direct and nested child meshes when a parent mesh matches the suffix.
    """
    matched_meshes = []

    for child in obj.children:
        if child.type == 'MESH':
            matched_meshes.append(child)
        elif child.type == 'EMPTY':
            # Recursively call to get meshes under nested empties
            matched_meshes.extend(get_all_child_meshes_recursive(child))

    return matched_meshes


    
## here the code starts
#create_collection(collection_name)
assign_categories()
#print("Hello, World!")
#test_equipments_names()
print("script finished")



class ProgressBar:
    def __init__(self, total, desc="Processing", unit="item"):
        self.total = total
        self.desc = desc
        self.unit = unit
        self.pbar = tqdm(total=total, desc=desc, unit=unit)

    def update(self, increment=1):
        self.pbar.update(increment)

    def close(self):
        self.pbar.close()