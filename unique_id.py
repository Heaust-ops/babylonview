class BlenderUniqueId():
    @staticmethod
    def assign_unique_id(scene):
        for obj in scene.objects:
            BlenderUniqueId.assign_unique_id_if_not_present(obj)
    
    @staticmethod
    def ensure_unique_id_on_all(bpy):
        BlenderUniqueId.assign_unique_id(bpy.context.scene)
    
    @staticmethod
    def assign_unique_id_if_not_present(obj):
        if "blenderUniqueId" in obj:
            return
        
        obj["blenderUniqueId"] = obj.name_full
