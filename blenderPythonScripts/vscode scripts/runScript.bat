@echo off
set MODULE_DIR=C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\blender orders test
set COMPONENT_EXCEL_PATH=D:\projects\NPC\20221117 3d model\automation phase\API SEPARATOR\APISEPARATOR.xlsx
set LOGGING_PATH=D:\projects\NPC\20221117 3d model\automation phase\API SEPARATOR\API SEPARATOR.txt

cd "C:\Program Files\Blender Foundation\Blender 3.6"
blender --background "D:\projects\NPC\20221117 3d model\automation phase\AirCompressors\AirComp - Copy.blend" --python "C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\blender orders test\blender_orders.py" -- --module_dir "%MODULE_DIR%" --component_excel_path "%COMPONENT_EXCEL_PATH%" --logging_path "%LOGGING_PATH%"

pause