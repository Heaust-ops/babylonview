import os

from .globals import GLB_PATH

from .tmpFolder import TmpFolder

from .color import Color
from .unique_id import BlenderUniqueId

GLB_SETTINGS = {
    "export_import_convert_lighting_mode": "COMPAT",
    "export_draco_mesh_compression_enable": False,
    "export_apply": True,
    "export_lights": True,
    "export_cameras": True,
    "export_extras": True,
    "export_yup": False
}

def export_glb(bpy, filepath = GLB_PATH, export_settings={}, names = None):
    """
    Export a Blender scene or selected objects to a GLB file.
    
    Args:
        filepath (str): Output file path for the GLB file
        export_settings (dict, optional): Dictionary containing export options
    
    Returns:
        bool: True if export was successful, False otherwise
    """
    TmpFolder.ensure()
    if os.path.exists(filepath):
        os.remove(filepath)
    
    try:
        GLB_SETTINGS["filepath"] = filepath
        final_settings = {**GLB_SETTINGS, **export_settings}

        # export only selected
        original_selected = [obj for obj in bpy.context.selected_objects]
        original_active = bpy.context.view_layer.objects.active

        if names is not None:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in bpy.context.scene.objects:
                if obj.name in names:
                    obj.select_set(True)
            final_settings['use_selection'] = True
        # ==== ==== ==== ====
        
        print("\nGLB Export Settings:")
        for key, value in final_settings.items():
            print(f"  {key}: {value} ({type(value).__name__})")

        BlenderUniqueId.ensure_unique_id_on_all(bpy)
        result = bpy.ops.export_scene.gltf(**final_settings)
        success = (result == {'FINISHED'})
        
        if not success:
            print(f"GLB Export failed with result: {result}")

        # export only selected - restore selection
        if names is not None:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selected:
                obj.select_set(True)
            if original_active:
                bpy.context.view_layer.objects.active = original_active
        # ==== ==== ==== ====
        
        return success
        
    except Exception as e:
        print(f"GLB Export Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def export_extra_scene_data(bpy):
    """
    Gather extra scene data not covered by glTF export:
      - AREA lights (name, full transform, size, color, energy, shape)
      - World background (flat color or environment texture settings)
    """
    # Initialize default result
    result = {
        'areaLights': [],
        'world': {'type': 'color', 'info': '#000000'}
    }

    # Get active scene
    scene = bpy.context.scene
    if scene is None:
        return result

    # Collect AREA-type lights
    for obj in scene.objects:
        if obj.type != 'LIGHT' or obj.data.type != 'AREA':
            continue
        ld = obj.data
        # Decompose world matrix for full transform
        matrix = obj.matrix_world
        pos = list(matrix.to_translation())
        scale = list(matrix.to_scale())
        rot = list(matrix.to_quaternion())

        result['areaLights'].append({
            'name': obj.name,
            'location': pos,
            'scale': scale,
            'rotation': rot,
            'size': [ld.size, getattr(ld, 'size_y', ld.size)],
            'color': '#{0:02x}{1:02x}{2:02x}'.format(
                int(ld.color[0] * 255), int(ld.color[1] * 255), int(ld.color[2] * 255)
            ),
            'energy': ld.energy,
            'shape': ld.shape
        })

    # World background
    world = scene.world
    if world is None:
        return result

    # Node-based world
    if world.use_nodes and world.node_tree:
        bg_node = next(
            (n for n in world.node_tree.nodes if n.type == 'BACKGROUND'), None
        )
        if bg_node:
            color_in = bg_node.inputs.get('Color')
            if color_in and color_in.is_linked:
                tex = color_in.links[0].from_node
                if tex.type == 'TEX_ENVIRONMENT' and tex.image:
                    img = tex.image
                    image_path = TmpFolder.mirror(bpy.path.abspath(img.filepath))
                    result['world'] = {
                        'type': 'image',
                        'info': [
                            image_path,
                            tex.interpolation,
                            tex.projection,
                            img.source,
                            img.colorspace_settings.name,
                            img.alpha_mode
                        ]
                    }
                    return result

    result['world'] = {'type': 'color', 'info': Color.get_world_color(bpy)}
    return result
