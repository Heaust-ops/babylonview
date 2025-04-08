from .globals import SOCKET_COMMANDS_TO_ID
from .socket_server import broadcast

class RealtimeSync:
    isEnabled = False
    handler = None
    _bpy = None  # store bpy if you want to use it outside handler

    @staticmethod
    def make_handler(bpy):
        def handler(_, depsgraph):
            if not RealtimeSync.isEnabled:
                return
            for update in depsgraph.updates:
                if isinstance(update.id, bpy.types.Object) and update.is_updated_transform:
                    obj = update.id
                    
                    pos = [round(v, 5) for v in obj.location]
                    scale = [round(v, 5) for v in obj.scale]
                    q = [round(v, 5) for v in obj.rotation_quaternion]
                    
                    broadcast([SOCKET_COMMANDS_TO_ID["transform update"], obj.original.as_pointer(), pos, scale, q])
        return handler

    @staticmethod
    def attach(bpy):
        if RealtimeSync.handler is None:
            RealtimeSync.handler = RealtimeSync.make_handler(bpy)
            RealtimeSync._bpy = bpy
        if RealtimeSync.handler not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(RealtimeSync.handler)
            print("RealtimeSync handler attached.")

    @staticmethod
    def detach(bpy):
        if RealtimeSync.handler in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(RealtimeSync.handler)
            print("RealtimeSync handler detached.")
        RealtimeSync.handler = None
        RealtimeSync._bpy = None
