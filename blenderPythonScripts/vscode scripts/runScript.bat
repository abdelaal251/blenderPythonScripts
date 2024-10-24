@echo off
set MODULE_DIR=C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\blender orders test
set COMPONENT_EXCEL_PATH=D:\projects\NPC\20221117 3d model\optimizationV3\CD2\CDU-2.xlsx
set LOGGING_PATH=D:\projects\NPC\20221117 3d model\optimizationV3\CD2 area A\CD2Area-A-z-up-try1.txt

cd "C:\Program Files\Blender Foundation\Blender 3.6"
blender --background "D:\projects\NPC\20221117 3d model\optimizationV3\CD2 area A\CD2Area-A-z-up-try1.blend" --python "C:\Users\Ahmed Abdelaal\source\repos\blenderPythonScripts\blenderPythonScripts\blenderPythonScripts\vscode scripts\blender orders test\blender_orders.py" -- --module_dir "%MODULE_DIR%" --component_excel_path "%COMPONENT_EXCEL_PATH%" --logging_path "%LOGGING_PATH%"

pause