# blender_orders.py
import bpy
import sys
import os
import logging
import pandas as pd
from tqdm import tqdm





# Add the directory containing your modules to sys.path
script_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.join(script_dir, 'C://Users/Ahmed Abdelaal/Desktop/python script for blender revolution/vscode scripts/blender orders test')
sys.path.append(module_dir)

# Load the Excel file that contains valves        -----> make sure to change the comment later if this directory will contains equipment and piping too
component_excel_path = 'D://projects/NPC/20221117 3d model/automation phase/CDU1/cdu-1a.xlsx'

# Logging file path
logging_path = 'C://Users/Ahmed Abdelaal/Desktop/python script for blender revolution/vscode scripts/cdu1.txt'

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
from sql_connection import connect_to_database, close_database_connection, retrieve_data
from config import DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD
from alive_progress import alive_bar
from blender_actions import (delete_objects_by_names, 
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
                             save_and_purge_memory)


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
    # UV projection size // default 2.0
    pojection_size = 2.0
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
        uv_unwrap_cube_projection(data['objects'], pojection_size, uv_progress_bar)

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

def perform_action_for_pipes_and_valves(pipes,valves):

    

    # Log function state
    logging.info(f"perform action for pipes and valves.")


    
    # UV projection size // default 2.0
    pojection_size = 2.0

    # Default material for piping and valves
    material_name = "00-piping grey"

    # valves with slash
    valves_with_slash = ['/' + valve for valve in valves]



    # Counters 
    no_of_pipes = len(pipes)
    no_of_valves = len(valves)
    i = 0
    print("\r\n")
    # Initializing progress bars
    with tqdm(total=no_of_pipes, desc="UV Progress", unit="objects") as uv_progress_bar, \
            tqdm(total=no_of_pipes, desc="Assigning Material", unit="objects") as assign_material_progress, \
            tqdm(total=1, desc="Combining Meshes", unit="objects") as combining_meshes_progress, \
            tqdm(total=1, desc="Assigning New Parent for pipe", unit="objects") as assign_parent_progress, \
            tqdm(total=1, desc="Assigning New Parent for valves", unit="objects") as assign_parent_progress_valves, \
            tqdm(total=1, desc="Decimation", unit="objects") as decimation_progress,\
            tqdm(total=no_of_valves, desc="Decimation for valves", unit="objects") as decimation_progress_valves:
        print("\r\n")   

        for pipe in pipes:

            # Counter increases every pipe
            i += 1
            logging.info(f"##############################################   {pipe}  // {i} of {no_of_pipes}    ##################")
            blender_object = create_blender_object(pipe)
            if blender_object:
                #check if the equipment is visivle
                if not blender_object.hide_get():

                    # initiate new list to contains meshes inside the equipment
                    child_list = []

                    # select all childerens
                    select_childeren_under_empty(pipe, child_list)
                    

                    #unwrap all meshes
                    uv_unwrap_cube_projection(child_list, pojection_size, uv_progress_bar)
                    
                    # Assign material
                    link_objects_with_material(child_list, material_name, assign_material_progress)
                    
                    # generate piping list without valves
                    piping_list = [item for item in child_list if item not in valves and item not in valves_with_slash]

                    # Joing all meshes
                    new_joined_mesh = join_meshes(piping_list,pipe, combining_meshes_progress)

                    # assign new parent
                    assign_new_parent_for_one_mesh(new_joined_mesh, piping_parent_name, collection_name, assign_parent_progress)
            else:
                logging.debug(f"pipe {pipe} not found in the scene.")

            # decimate piping mesh
            #decimate_modifier_single_mesh(new_joined_mesh, decimation_progress)


            # assign new parent for the valves
            assign_new_parent(valves, valves_oparent_name, collection_name, assign_parent_progress_valves)

            # Delete unnecessary childs
            check_and_delete_empty_objects(valves_oparent_name)
            
            #decimate valves mesh
            #decimate_modifier(valves,decimation_progress_valves)

            # save the current state
            save_and_purge_memory()
            
            # Close ProgressBar
            uv_progress_bar.close()
            assign_material_progress.close()
            combining_meshes_progress.close()
            assign_parent_progress.close()
            assign_parent_progress_valves.close()
            decimation_progress.close()
            decimation_progress_valves.close()

            # Log function state
            logging.info(f"perform action for pipes and ended.")




# Perform actions for all equipment list 
def perform_action_for_equi(equipments):

    # Log function state
    logging.info(f"performing action for equi started")

    # UV projection size // default 2.0
    pojection_size = 2.0

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


def assign_categories():

    # Log function state
    logging.info(f"assining categories for model suffix.")
    
    # Connect to the SQL Server database
    conn, cursor = connect_to_database()

    # Retrieve data from the table
    rows = retrieve_data(cursor)

    # Create lists based on categories
    category_lists = {}

    for row in rows:
        id_, category, suffix, material = row
        if category not in category_lists:
            category_lists[category] = {'objects': [], 'keywords': set(), 'materials': []}

        suffixes = [s.strip() for s in suffix.split(',')]

        for obj_name in bpy.data.objects:
            # Check if the object is a mesh and matches any suffix in the list
            if obj_name.type == 'MESH' and any(sfx in obj_name.name for sfx in suffixes):
                category_lists[category]['objects'].append(obj_name.name)
                keywords = [keyword.strip() for keyword in obj_name.name.split(',')]
                category_lists[category]['keywords'].update(keywords)

                # Append material information to the materials list for the category
                category_lists[category]['materials'].append(material)

    # Execute commands for each category
    for category, data in category_lists.items():
        logging.info(f" excuting commands for {category} category.")
        execute_commands_for_category(category, data)

    # Close the connection
    close_database_connection(conn)

    # Initialize a list to store valve, equipments and pipes names
    valves = []
    equipments = []
    pipes = []

    # get valve list from the givn excel sheet
    df = pd.read_excel(component_excel_path)
    valves = df.loc[df['Type'] == 'VALV', 'Name'].tolist()
    equipments = df.loc[df['Type'] == 'EQUI', 'Name'].tolist()
    pipes = df.loc[df['Type'] == 'PIPE', 'Name'].tolist()

    #perform_action_for_valves(valves)
    perform_action_for_equi(equipments)
    perform_action_for_pipes_and_valves(pipes, valves)

    # Log function state
    logging.info(f"assining categories for model suffix.")


## here the code starts
create_collection(collection_name)
assign_categories()



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