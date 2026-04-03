import asyncio
import websockets
import json

async def test_connect():
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            # Send join message
            join_msg = {'type': 'join', 'name': 'TestPlayer', 'color': [0, 255, 0]}
            await websocket.send(json.dumps(join_msg))
            
            # Wait for init response
            response = await websocket.recv()
            print("Server responded:", response)
            
            print("✅ Connection works!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

asyncio.run(test_connect())