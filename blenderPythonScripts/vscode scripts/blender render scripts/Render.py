import bpy

# Set the render engine and output format
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.filepath = 'C://Users/Ahmed Abdelaal/Desktop/render output/rendered_image.jpg'

# Set other render settings as needed

# Render the scene
bpy.ops.render.render(write_still=True)
