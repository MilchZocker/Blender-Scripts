import bpy

# Iterate through selected objects in the scene
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':  # Only consider mesh objects
        if obj.material_slots:  # Check if the object has materials
            first_material = obj.material_slots[0].material
            if first_material:  # Check if the first material exists
                material_name = first_material.name
                # Prepend material name to the object's name
                obj.name = f"[{material_name}] {obj.name}"
            else:
                print(f"Object '{obj.name}' has an empty material slot.")
        else:
            print(f"Object '{obj.name}' has no materials.")
