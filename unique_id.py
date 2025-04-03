class BlenderUniqueId():
    @staticmethod
    def assign_unique_id(scene):
        if "next_unique_id" not in scene:
            scene["next_unique_id"] = 0

        for obj in scene.objects:
            if "blenderUniqueId" not in obj:
                obj["blenderUniqueId"] = scene["next_unique_id"]
                scene["next_unique_id"] += 1
    
    @staticmethod
    def add_unique_id_handler(bpy):
        if BlenderUniqueId.assign_unique_id not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(BlenderUniqueId.assign_unique_id)
    
    @staticmethod
    def remove_unique_id_handler(bpy):
        """Remove the handler to prevent multiple registrations."""
        if BlenderUniqueId.assign_unique_id in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(BlenderUniqueId.assign_unique_id)
