bl_info = {
    "name": "Babylonjs View Addon",
    "blender": (4, 0, 0),
    "category": "System",
    "author": "Heaust",
    "description": "I wonder how this looks in babylonjs",
}

from .globals import GLB_PATH, SOCKET_COMMANDS_FROM_ID, SOCKET_COMMANDS_TO_ID
from .http_server import start_generic_http_server
from .http_server import stop_generic_http_server
from .glb_exporter import export_extra_scene_data, export_glb
from .socket_server import on_connect, on_disconnect, on_message, send_message_async, stop_socket_server, start_socket_server, broadcast
from .realtime_sync import RealtimeSync
import json

import asyncio
import bpy # type: ignore


def scheduled_export_glb():
    export_glb(bpy, GLB_PATH)
    broadcast([SOCKET_COMMANDS_TO_ID["sync glb"], export_extra_scene_data(bpy)])
    return None  # Return None to unregister the timer

"""
SOCKET HANDLERS START
"""

@on_connect
def handle_connect(client_id):
    print(f"Client connected: {client_id}")
    # Update UI
    bpy.app.timers.register(lambda: None)

@on_message
def handle_message(client_id, message):
    msg = json.loads(message)
    if msg[0] not in SOCKET_COMMANDS_FROM_ID:
        print(f"Message from {client_id}: {msg}")
        print("malformed message, ignoring:")
        return
    
    msg[0] = SOCKET_COMMANDS_FROM_ID[msg[0]]
    print(f"Message from {client_id}: {msg}")

    if msg[0] == "sync glb":
        bpy.app.timers.register(scheduled_export_glb)
    if msg[0] == "realtime sync":
        RealtimeSync.isEnabled = msg[1] == 1
        
    # Echo back to the client
    asyncio.run_coroutine_threadsafe(
        send_message_async(client_id, f"Echo: {message}"),
        asyncio.get_event_loop()
    )

@on_disconnect
def handle_disconnect(client_id):
    print(f"Client disconnected: {client_id}")
    # Update UI
    bpy.app.timers.register(lambda: None)

"""
SOCKET HANDLERS END
"""

"""
GUI START
"""

is_running = False
class ToggleServerOperator(bpy.types.Operator):
    """Start / Stop Server"""
    global is_running
    
    bl_idname = "toggle_server.server_custom"
    bl_label = "Toggle Babylon.js Server"

    def execute(self, context):
        global is_running
        if is_running:
            RealtimeSync.detach(bpy)
            stop_generic_http_server()
            stop_socket_server()
            is_running = False
            self.report({'INFO'}, "Stopped Babylon.js View Server!")
        else:
            export_glb(bpy, GLB_PATH)
            RealtimeSync.attach(bpy)
            start_socket_server()
            start_generic_http_server()
            is_running = True
            print(export_extra_scene_data(bpy))
            self.report({'INFO'}, "Started Babylon.js View Server!")
        return {'FINISHED'}

class ToggleServerPanel(bpy.types.Panel):
    bl_label = "Babylon.js View"
    bl_idname = "VIEW3D_PT_toggle_server"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Babylon.js View'

    def draw(self, context):
        layout = self.layout
        layout.operator("toggle_server.server_custom", text="Stop Server" if is_running else "Start Server")

# Register/unregister functions
classes = (ToggleServerOperator, ToggleServerPanel)

"""
GUI END 
"""

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    global is_running
    
    if is_running:
        stop_generic_http_server()
        stop_socket_server()
        is_running = False
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

bpy.app.debug = True
if __name__ == "__main__":
    register()
