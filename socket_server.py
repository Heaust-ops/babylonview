import json
import logging
import uuid
import threading
import hashlib
import base64
import asyncio

from .globals import SOCKET_PORT

# Configure logging
logger = logging.getLogger("websocket_server")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global variables
websocket_server = None
server_thread = None
server_loop = None
is_running = False
clients = {}
message_handlers = []
connection_handlers = []
disconnection_handlers = []

# WebSocket frame handling
def create_text_frame(message: str) -> bytes:
    """Create a WebSocket text frame from a message."""
    message_bytes = message.encode('utf-8')
    payload_length = len(message_bytes)
    
    # Create header
    if payload_length < 126:
        header = bytes([0b10000001, payload_length])
    elif payload_length < 65536:
        header = bytes([0b10000001, 126]) + payload_length.to_bytes(2, byteorder='big')
    else:
        header = bytes([0b10000001, 127]) + payload_length.to_bytes(8, byteorder='big')
    
    # Return the complete frame
    return header + message_bytes

async def perform_handshake(reader, writer):
    """Perform the WebSocket handshake."""
    # Read the HTTP request
    http_request = bytearray()
    while True:
        line = await reader.readline()
        http_request.extend(line)
        if line == b'\r\n' or not line:
            break
    
    http_request = http_request.decode('utf-8')
    
    # Extract the WebSocket key
    key = None
    for line in http_request.split('\r\n'):
        if line.startswith('Sec-WebSocket-Key:'):
            key = line.split(':', 1)[1].strip()
            break
    
    if not key:
        logger.error("WebSocket handshake failed: No Sec-WebSocket-Key found")
        writer.close()
        return False
    
    # Generate the accept key
    magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    accept_key = base64.b64encode(
        hashlib.sha1((key + magic_string).encode()).digest()
    ).decode()
    
    # Send the handshake response
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
    )
    writer.write(response.encode())
    await writer.drain()
    
    logger.debug("WebSocket handshake completed successfully")
    return True

async def receive_message(reader):
    """Receive and decode a WebSocket message."""
    # Read the first 2 bytes (header)
    header = await reader.read(2)
    if not header:
        return None
    
    # Parse the header
    fin = (header[0] & 0b10000000) != 0
    opcode = header[0] & 0b00001111
    masked = (header[1] & 0b10000000) != 0
    payload_length = header[1] & 0b01111111
    
    # Handle different opcodes
    if opcode == 0x8:  # Close frame
        return None
    elif opcode not in (0x1, 0x2):  # Only support text and binary frames
        logger.warning(f"Unsupported WebSocket opcode: {opcode}")
        return None
    
    # Get payload length
    if payload_length == 126:
        payload_length = int.from_bytes(await reader.read(2), byteorder='big')
    elif payload_length == 127:
        payload_length = int.from_bytes(await reader.read(8), byteorder='big')
    
    # Get masking key if message is masked
    mask = await reader.read(4) if masked else None
    
    # Read payload
    payload = await reader.read(payload_length)
    
    # Unmask the payload if necessary
    if masked:
        unmasked = bytearray(payload_length)
        for i in range(payload_length):
            unmasked[i] = payload[i] ^ mask[i % 4]
        payload = unmasked
    
    # Convert to string for text frames
    if opcode == 0x1:  # Text frame
        return payload.decode('utf-8')
    else:  # Binary frame
        return payload

async def handle_client(reader, writer):
    """Handle a new client connection."""
    global clients
    
    client_id = str(uuid.uuid4())
    addr = writer.get_extra_info('peername')
    
    logger.info(f"New connection from {addr}, assigned ID: {client_id}")
    
    # Perform WebSocket handshake
    if not await perform_handshake(reader, writer):
        return
    
    # Add client to clients dictionary
    clients[client_id] = writer
    
    # Notify connection handlers
    for handler in connection_handlers:
        try:
            handler(client_id)
        except Exception as e:
            logger.error(f"Error in connection handler: {e}")
    
    try:
        # Handle incoming messages
        while True:
            try:
                message = await receive_message(reader)
                if message is None:  # Connection closed
                    break
                
                # Process the message
                logger.debug(f"Received from {client_id}: {message}")
                
                # Schedule message handlers to run in the main thread
                for handler in message_handlers:
                    try:
                        # We use a simple approach here since we can't easily invoke 
                        # Blender's callback system from asyncio
                        handler(client_id, message)
                    except Exception as e:
                        logger.error(f"Error in message handler: {e}")
                        
            except ConnectionError:
                break
                
    finally:
        # Clean up when client disconnects
        await close_client(client_id, writer)

async def close_client(client_id, writer):
    """Close a client connection and clean up."""
    global clients
    
    if client_id in clients:
        logger.info(f"Client {client_id} disconnected")
        
        # Notify disconnection handlers
        for handler in disconnection_handlers:
            try:
                handler(client_id)
            except Exception as e:
                logger.error(f"Error in disconnection handler: {e}")
        
        # Remove from clients dictionary and close connection
        del clients[client_id]
        writer.close()
        await writer.wait_closed()

async def send_message_async(client_id, message):
    """Send a message to a specific client (async version)."""
    global clients
    
    if client_id not in clients:
        logger.error(f"Cannot send message: Client {client_id} not found")
        return False
    
    writer = clients[client_id]
    try:
        # Convert to string if not already
        if not isinstance(message, str):
            message = json.dumps(message)
        
        # Create a WebSocket frame
        frame = create_text_frame(message)
        writer.write(frame)
        await writer.drain()
        return True
    except Exception as e:
        logger.error(f"Error sending message to {client_id}: {e}")
        return False

def send_message(client_id, message):
    """Non-async wrapper for send_message_async."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(send_message_async(client_id, message))

async def broadcast_async(message, exclude=None):
    """Send a message to all connected clients (async version)."""
    global clients
    
    exclude = exclude or set()
    successful_sends = 0
    
    # Convert to string if not already
    if not isinstance(message, str):
        message = json.dumps(message)
    
    # Create the WebSocket frame once
    frame = create_text_frame(message)
    
    # Send to all clients
    for client_id, writer in list(clients.items()):
        if client_id in exclude:
            continue
            
        try:
            writer.write(frame)
            await writer.drain()
            successful_sends += 1
        except Exception as e:
            logger.error(f"Error broadcasting to {client_id}: {e}")
    
    return successful_sends

def broadcast(message, exclude=None):
    """Non-async wrapper for broadcast_async."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(broadcast_async(message, exclude))

def on_message(handler):
    """Register a handler for incoming messages."""
    message_handlers.append(handler)
    return handler

def on_connect(handler):
    """Register a handler for new connections."""
    connection_handlers.append(handler)
    return handler

def on_disconnect(handler):
    """Register a handler for client disconnections."""
    disconnection_handlers.append(handler)
    return handler

async def run_server_async():
    global websocket_server, is_running
    try:
        websocket_server = await asyncio.start_server(
            handle_client, "0.0.0.0", SOCKET_PORT
        )
        logger.info("Server started on 0.0.0.0:" + str(SOCKET_PORT))
        is_running = True
        
        async with websocket_server:
            try:
                await websocket_server.serve_forever()
            except asyncio.CancelledError:
                logger.info("serve_forever cancelled, shutting down server.")
                # This exception is expected during shutdown, so we simply exit the loop.
    except Exception as e:
        logger.error(f"Error running server: {e}")
    finally:
        is_running = False

def server_thread_function():
    """Function to run in the server thread."""
    global server_loop
    loop = asyncio.new_event_loop()
    server_loop = loop
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_server_async())
    loop.close()

def start_socket_server():
    """Start the WebSocket server in a separate thread."""
    global server_thread, is_running
    
    if not is_running:
        logger.info("Starting WebSocket server...")
        server_thread = threading.Thread(target=server_thread_function, daemon=True)
        server_thread.start()

async def close_server():
    global websocket_server
    if websocket_server is not None:
        websocket_server.close()
        await websocket_server.wait_closed()

def stop_socket_server():
    global websocket_server, is_running, server_loop

    if is_running and websocket_server and server_loop:
        logger.info("Stopping WebSocket server...")

        # Schedule the close coroutine on the server's event loop
        future = asyncio.run_coroutine_threadsafe(close_server(), server_loop)
        try:
            # Wait for the coroutine to finish (adjust timeout as needed)
            future.result(timeout=5)
        except Exception as e:
            logger.error(f"Error stopping server: {e}")

        is_running = False
        logger.info("WebSocket server stopped")
