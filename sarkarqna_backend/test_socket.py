#!/usr/bin/env python3
"""
Test script for Socket.IO functionality
"""

import socketio
import asyncio
import json

# Create a Socket.IO client
sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("Connected to server!")

@sio.event
async def disconnect():
    print("Disconnected from server!")

@sio.event
async def message(data):
    print(f"Received message: {data}")

@sio.event
async def response(data):
    print(f"Received response: {json.dumps(data, indent=2)}")

@sio.event
async def error(data):
    print(f"Received error: {data}")

@sio.event
async def message_ack(data):
    print(f"Message acknowledged: {data}")

@sio.event
async def status(data):
    print(f"Status: {data}")

async def test_socket():
    """Test Socket.IO connection and messaging"""
    try:
        # Connect to server
        await sio.connect('http://localhost:8000')
        
        # Test ping
        await sio.emit('ping')
        await asyncio.sleep(1)
        
        # Test status
        await sio.emit('get_status')
        await asyncio.sleep(1)
        
        # Test message
        test_message = {
            'id': 'test_123',
            'text': 'मुझे प्रधानमंत्री आवास योजना के लिए क्या योग्यता चाहिए?',
            'sender': 'Test User',
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        print("Sending test message...")
        await sio.emit('message', test_message)
        
        # Wait for response
        await asyncio.sleep(5)
        
        # Disconnect
        await sio.disconnect()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_socket())
