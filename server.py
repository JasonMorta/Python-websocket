import websockets
import asyncio
import json

this_dict = {
    "counter": 1,
}

# List of connected clients
connected_clients = set()

# increment the counter
def increment_counter():
    if this_dict["counter"] < 10000:  # Example: Stop incrementing after reaching 100
        this_dict["counter"] += 1
        print("Counter incremented to", this_dict["counter"])
        return True
    return False

# Notify all connected clients about dictionary update
async def notify_clients():
    if connected_clients:  # If there are connected clients
        msg = json.dumps(this_dict)  # Make sure msg is valid JSON
        tasks = [client.send(msg) for client in connected_clients]
        await asyncio.gather(*tasks)

# Define a coroutine to handle each client connection
async def handle_client(websocket):
    connected_clients.add(websocket)
    try:
        # This function handles messages from the client
        async for message in websocket:
            # When a message is received from the client, print it
            print("Received message from client:", message)
            # Prepare a response message
            response = "Server received: " + json.dumps(message)
            # Send the response back to the client
            await websocket.send(response)
    finally:
        # Remove client from the set when the connection is closed
        connected_clients.remove(websocket)

# Define the main coroutine
async def main():
    # Start a WebSocket server on localhost, port 3002
    async with websockets.serve(handle_client, "localhost", 3002):
        # Print a message when the server is started
        print("WebSocket server started")
        # Call increment_counter function to start incrementing the counter
        while True:
            if increment_counter():
                await notify_clients()  # Notify clients about dictionary update
            await asyncio.sleep(1)  # Increment the counter every second

# Run the main coroutine
asyncio.run(main())
