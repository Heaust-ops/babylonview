import os

GLB_SETTINGS = {
    "export_import_convert_lighting_mode": "COMPAT",
    "export_draco_mesh_compression_enable": False,
    "export_apply": True,
    "export_lights": True,
    "export_cameras": True,
    "export_extras": True
}

def export_glb(bpy, filepath, export_settings={}):
    """
    Export a Blender scene or selected objects to a GLB file.
    
    Args:
        filepath (str): Output file path for the GLB file
        export_settings (dict, optional): Dictionary containing export options
    
    Returns:
        bool: True if export was successful, False otherwise
    """
    if os.path.exists(filepath):
        os.remove(filepath)
    
    try:
        GLB_SETTINGS["filepath"] = filepath
        final_settings = {**GLB_SETTINGS, **export_settings}
        
        print("\nGLB Export Settings:")
        for key, value in final_settings.items():
            print(f"  {key}: {value} ({type(value).__name__})")
        
        result = bpy.ops.export_scene.gltf(**final_settings)
        success = (result == {'FINISHED'})
        
        if not success:
            print(f"GLB Export failed with result: {result}")
        
        return success
        
    except Exception as e:
        print(f"GLB Export Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
