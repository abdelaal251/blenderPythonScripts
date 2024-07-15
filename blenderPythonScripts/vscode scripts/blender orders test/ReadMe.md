# Blender Automation Scripts

This repository contains two Python scripts designed to automate tasks within Blender: `blender_actions.py` and `blender_orders.py`.

## Prerequisites

- Blender installed on your system
- Python 3.x
- Required Python packages: `bpy`, `bmesh`, `logging`, `pandas`, `tqdm`, `argparse`

## Script Descriptions

### `blender_actions.py`

This script contains functions to perform various actions within Blender. Below are the key functionalities:

- **delete_objects_by_names(object_names)**: Deletes objects in the Blender scene by their names.
- **check_object_live(obj_name)**: Checks if an object with the given name exists in the Blender scene.
- **check_object_live_test(obj_name)**: Similar to `check_object_live` but returns the object if it exists, or `None` otherwise.
- **create_new_empty(empty_name)**: Creates a new empty object in the Blender scene.
- **print_selected_objects()**: Prints the names of the currently selected objects in the Blender scene.

#### Usage

To use any of the functions in `blender_actions.py`, you can import the script into your Blender Python environment and call the desired function. For example:

```python
import bpy
import blender_actions as ba

# Delete objects by names
ba.delete_objects_by_names(['Cube', 'Sphere'])

# Check if an object is live
is_live = ba.check_object_live('Cube')
print(f'Is Cube live: {is_live}')

# Create a new empty object
ba.create_new_empty('NewEmpty')

# Print selected objects
ba.print_selected_objects()
```

### `blender_orders.py`

This script is designed to process orders and perform bulk operations in Blender. It reads from an Excel file and logs the operations performed.

#### Command-Line Arguments

- `--module_dir`: Directory containing the modules.
- `--component_excel_path`: Path to the component Excel file.
- `--logging_path`: Path to the logging file.

#### Usage

To run the script, use Blender's Python environment with the following command:

```sh
blender --background --python blender_orders.py -- --module_dir /path/to/modules --component_excel_path /path/to/excel/file.xlsx --logging_path /path/to/log/file.log
```

#### Example

```sh
blender --background --python blender_orders.py -- --module_dir ./modules --component_excel_path ./data/components.xlsx --logging_path ./logs/operations.log
```

## Logging

Both scripts utilize Python's logging module to log their operations. Ensure that the logging path provided in `blender_orders.py` is writable and accessible.

## Contributing

If you would like to contribute to these scripts, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
```

This `README.md` file provides a brief overview of each script, their key functions, and how to use them, both as part of a script and from the command line. If you need any further customization or additional details, please let me know!