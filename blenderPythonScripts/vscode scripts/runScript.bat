@echo off
set MODULE_DIR=C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\blender orders test
set COMPONENT_EXCEL_PATH=D:\projects\NPC\20221117 3d model\optimizationV3\airCompressor\AIR COMP exist.xlsx
set LOGGING_PATH=D:\projects\NPC\20221117 3d model\optimizationV3\airCompressor\air-compressors-log.txt

cd "C:\Program Files\Blender Foundation\Blender 3.6"
blender --background "D:\projects\NPC\20221117 3d model\optimizationV3\airCompressor\air-compressors.blend" --python "C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\blender orders test\blender_orders.py" -- --module_dir "%MODULE_DIR%" --component_excel_path "%COMPONENT_EXCEL_PATH%" --logging_path "%LOGGING_PATH%"

pause