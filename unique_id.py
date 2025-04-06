uniqueId = 0
class BlenderUniqueId():
    @staticmethod
    def assign_unique_id(scene):
        global uniqueId
        for obj in scene.objects:
            BlenderUniqueId.assign_unique_id_if_not_present(obj)
    
    @staticmethod
    def ensure_unique_id_on_all(bpy):
        BlenderUniqueId.assign_unique_id(bpy.context.scene)
    
    @staticmethod
    def assign_unique_id_if_not_present(obj):
        global uniqueId
        if "blenderUniqueId" not in obj:
            obj["blenderUniqueId"] = uniqueId
            uniqueId += 1
    
    @staticmethod
    def add_unique_id_handler(bpy):
        if BlenderUniqueId.assign_unique_id not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(BlenderUniqueId.assign_unique_id)
    
    @staticmethod
    def remove_unique_id_handler(bpy):
        if BlenderUniqueId.assign_unique_id in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(BlenderUniqueId.assign_unique_id)
