import bpy
import pyodbc

# Connection parameters
server = 'AHMED-ABDELAAL\SQLEXPRESS'
database = 'NPC-blender-scripts'
username = 'sa'
password = 'AAbdelaal98@gmail.com1'

# Create a connection string
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect to the SQL Server database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Retrieve data from the table
cursor.execute('SELECT * FROM "mesh-categorization"')
rows = cursor.fetchall()

# Create lists based on categories
category_lists = {}

for row in rows:
    id_, category, suffix = row
    if category not in category_lists:
        category_lists[category] = {'objects': [], 'keywords': set()}
    category_lists[category]['objects'].append(suffix)  # Fix here, append the suffix directly
    # Split the comma-separated suffix into keywords
    keywords = [keyword.strip() for keyword in suffix.split(',')]
    category_lists[category]['keywords'].update(keywords)

# Search and associate Blender objects based on keywords
for category, data in category_lists.items():
    for keyword in data['keywords']:
        for obj in bpy.data.objects:
            # Check if the keyword is present in the object name
            if keyword.lower() in obj.name.lower():
                # Add the object name to the category
                data['objects'].append(obj.name)
                break

# Print the updated lists
for category, data in category_lists.items():
    print(f"{category} list:")
    print(f"Objects: {', '.join(data['objects'])}")

# Close the connection
conn.close()