bl_info = {
    "name": "Babylonjs View Addon",
    "blender": (4, 0, 0),
    "category": "System",
    "author": "Heaust",
    "description": "I wonder how this looks in babylonjs",
}

from .globals import GLB_PATH, COMMANDS_JSON_PATH
from .http_server import start_generic_http_server
from .http_server import stop_generic_http_server
from .glb_exporter import export_glb
from .socket_server import on_connect, on_disconnect, on_message, send_message_async, stop_socket_server, start_socket_server, broadcast
from .unique_id import BlenderUniqueId
from .color import Color
import json

import asyncio
import bpy # type: ignore

with open(COMMANDS_JSON_PATH, 'r') as file:
    global socket_commands_to_id, socket_commands_from_id
    socket_commands_to_id = json.load(file)
    socket_commands_from_id = {v: k for k, v in socket_commands_to_id.items()}

def scheduled_export_glb():
    export_glb(bpy, GLB_PATH)
    broadcast(socket_commands_to_id["sync glb"])
    broadcast([socket_commands_to_id["update world color"], Color.get_world_color(bpy)])
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
    if msg[0] not in socket_commands_from_id:
        print(f"Message from {client_id}: {msg}")
        print("malformed message, ignoring:")
        return
    
    msg[0] = socket_commands_from_id[msg[0]]
    print(f"Message from {client_id}: {msg}")

    if msg[0] == "sync glb":
        bpy.app.timers.register(scheduled_export_glb)
        
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
            stop_generic_http_server()
            stop_socket_server()
            is_running = False
            self.report({'INFO'}, "Stopped Babylon.js View Server!")
        else:
            export_glb(bpy, GLB_PATH)
            start_socket_server()
            start_generic_http_server()
            is_running = True
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

    # inits
    BlenderUniqueId.add_unique_id_handler(bpy)

def unregister():
    global is_running
    
    if is_running:
        stop_generic_http_server()
        stop_socket_server()
        is_running = False
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # cleanups
    BlenderUniqueId.remove_unique_id_handler(bpy)

bpy.app.debug = True
if __name__ == "__main__":
    register()
