from .glb_exporter import export_glb
from .debounce import debounce
from .globals import SOCKET_COMMANDS_TO_ID
from .socket_server import broadcast

class CreationDeletionTracker:
    _known_objects = set()
    
    _export_state = 0 # 0 = idle, 1 = in-progress
    _update_queued = False

    _created = set()
    _deleted = set()

    @staticmethod
    @debounce(0.1)
    def update(bpy):
        if CreationDeletionTracker._export_state == 1:
            CreationDeletionTracker._update_queued = True
            return
            
        current_objects = { obj.name_full for obj in bpy.data.objects }
        
        created = current_objects - CreationDeletionTracker._known_objects
        deleted = CreationDeletionTracker._known_objects - current_objects
        
        CreationDeletionTracker._known_objects = current_objects

        if len(list(created)) == 0 and len(list(deleted)) == 0:
            return
        
        CreationDeletionTracker.broadcast_update(bpy, created, deleted);

    @staticmethod
    def broadcast_update(bpy, created, deleted):
        CreationDeletionTracker._export_state = 1
        # ==== ==== ==== ====
        export_glb(bpy, names=created)
        
        broadcast([
            SOCKET_COMMANDS_TO_ID["creation deletion update"],
            list(deleted)
        ])
        
        # ==== ==== ==== ====
        if CreationDeletionTracker._update_queued:
            CreationDeletionTracker.update(bpy)
        CreationDeletionTracker._update_queued = False

        CreationDeletionTracker._export_state = 0

class RealtimeSync:
    isEnabled = False
    handler = None
    _bpy = None  # store bpy if you want to use it outside handler
    _known_objects = set()  # track known object names

    @staticmethod
    def make_handler(bpy):
        # Initialize known objects on first handler creation
        if not RealtimeSync._known_objects:
            RealtimeSync._known_objects = {obj.name_full for obj in bpy.data.objects}

        def handler(_, depsgraph):
            if not RealtimeSync.isEnabled:
                return

            # --- Detect creation and deletion of objects ---
            CreationDeletionTracker.update(bpy)

            # --- transform updates ---
            for update in depsgraph.updates:
                if isinstance(update.id, bpy.types.Object) and update.is_updated_transform:
                    obj = update.id
                    matrix = obj.matrix_world
                    pos = list(matrix.to_translation())
                    scale = list(matrix.to_scale())
                    q = list(matrix.to_quaternion())
                    broadcast([
                        SOCKET_COMMANDS_TO_ID["transform update"],
                        obj.name_full,
                        pos,
                        scale,
                        q
                    ])

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
        RealtimeSync._known_objects.clear()  # reset known objects
