import bpy

def merge_similar_bones(armature_name):
    # Get the armature object
    armature = bpy.data.objects.get(armature_name)
    if not armature or armature.type != 'ARMATURE':
        print(f"Armature '{armature_name}' not found or is not an armature.")
        return

    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    edit_bones = armature.data.edit_bones

    # Helper function to find similar bone names
    def find_similar_bones(bones):
        similar_pairs = []
        for bone in bones:
            for other_bone in bones:
                # Check for similarity (e.g., "Shoulder_L" vs "Shoulder.L")
                if bone != other_bone and (bone.replace("_", ".") == other_bone or bone.replace(".", "_") == other_bone):
                    similar_pairs.append((bone, other_bone))
        return similar_pairs

    # Get all bone names
    bone_names = [bone.name for bone in edit_bones]
    similar_bone_pairs = find_similar_bones(bone_names)

    # Merge similar bones, prioritizing the one with more child bones
    for bone_a_name, bone_b_name in similar_bone_pairs:
        bone_a = edit_bones.get(bone_a_name)
        bone_b = edit_bones.get(bone_b_name)

        if not bone_a or not bone_b:
            print(f"Error: One of the bones '{bone_a_name}' or '{bone_b_name}' does not exist.")
            continue

        # Determine which bone has more child bones
        if len(bone_a.children) >= len(bone_b.children):
            target_bone = bone_a
            source_bone = bone_b
        else:
            target_bone = bone_b
            source_bone = bone_a

        print(f"Merging '{source_bone.name}' into '{target_bone.name}'")

        # Reparent all children of the source bone to the target bone
        for child in source_bone.children:
            child.parent = target_bone

        # Remove the source bone
        edit_bones.remove(source_bone)

    bpy.ops.object.mode_set(mode='OBJECT')
    print("Bone merging complete.")

# Call the function with the name of your armature
merge_similar_bones("Armature")  # Replace "Armature" with the name of your armature object
