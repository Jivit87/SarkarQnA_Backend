# socket_handlers.py

import socketio
from datetime import datetime
from core.services.rag_service import RAGService
from core.services.langgraph_service import LangGraphService
from core.utils.logger import logger

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25,
    transports=['websocket', 'polling']
)

# Initialize services
rag_service = None
langgraph_service = None
gemini_model = None

def initialize_services():
    """Initialize Gemini, RAG and LangGraph services"""
    global rag_service, langgraph_service, gemini_model
    try:
        from core.models.gemini_model import GeminiModel
        from config import Settings
        
        settings = Settings()
        gemini_model = GeminiModel()
        rag_service = RAGService()
        langgraph_service = LangGraphService(api_key=settings.LANGGRAPH_API_KEY)
        
        logger.info("Socket services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize socket services: {e}")

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    logger.info(f"Client {sid} connected")
    await sio.emit('connect', {'message': 'Connected to SarkarQnA server'}, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client {sid} disconnected")

@sio.event
async def message(sid, data):
    """Handle incoming messages - main message handler"""
    await handle_chat_message(sid, data)

@sio.event
async def chat_message(sid, data):
    """Handle chat messages - alternative handler"""
    await handle_chat_message(sid, data)

@sio.event
async def send_message(sid, data):
    """Handle send message - alternative handler"""
    await handle_chat_message(sid, data)

async def handle_chat_message(sid, data):
    """Process chat message and send response"""
    try:
        logger.info(f"Received message from {sid}: {data}")
        
        # Extract message data
        message_text = data.get('text', '') if isinstance(data, dict) else str(data)
        message_id = data.get('id') if isinstance(data, dict) else None
        
        if not message_text.strip():
            await sio.emit('error', {'message': 'Empty message received'}, room=sid)
            return
        
        # Send acknowledgment
        if message_id:
            await sio.emit('message_ack', {'messageId': message_id}, room=sid)
        
        if not gemini_model:
            raise Exception("Gemini model not initialized")
        
        # First, get Gemini's response
        gemini_response = await gemini_model.generate_response(message_text)
        
        # Prepare base response
        response_data = {
            'id': f"response_{datetime.now().timestamp()}",
            'text': gemini_response["text"],
            'sender': 'Assistant',
            'timestamp': datetime.now().isoformat(),
            'responseTo': message_id
        }
        
        # If it's an eligibility query and RAG service is available
        if gemini_response["is_eligibility_query"] and rag_service:
            try:
                # Get RAG response for eligibility
                rag_result = rag_service.answer_query(message_text)
                
                # Get web results if available
                web_results = []
                if langgraph_service:
                    try:
                        web_results = langgraph_service.search_scheme(message_text)
                    except Exception as e:
                        logger.warning(f"LangGraph service failed: {e}")
                
                # Merge sources
                all_sources = list(dict.fromkeys(rag_result["sources"] + web_results))
                
                # Add eligibility info to response
                response_data.update({
                    'eligible': rag_result.get("eligible", False),
                    'confidence': rag_result.get("confidence", 0.0),
                    'sources': all_sources
                })
                
                        # Send eligibility response
                await sio.emit('response', response_data, room=sid)
                await sio.emit('message', response_data, room=sid)
                await sio.emit('chat_message', response_data, room=sid)
                
                logger.info(f"Sent response to {sid}: {response_data['text'][:100]}...")
                
            except Exception as e:
                logger.error(f"Error processing message with RAG: {e}")
                error_response = {
                    'id': f"error_{datetime.now().timestamp()}",
                    'text': f"Sorry, I encountered an error processing your request: {str(e)}",
                    'sender': 'System',
                    'timestamp': datetime.now().isoformat(),
                    'responseTo': message_id
                }
                await sio.emit('error', error_response, room=sid)
        # For non-eligibility queries or when RAG isn't needed, send the Gemini response directly
        await sio.emit('response', response_data, room=sid)
        await sio.emit('message', response_data, room=sid)
        await sio.emit('chat_message', response_data, room=sid)
        
        logger.info(f"Sent response to {sid}: {response_data['text'][:100]}...")
            
    except Exception as e:
        logger.error(f"Error in handle_chat_message: {e}")
        await sio.emit('error', {
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }, room=sid)

@sio.event
async def error(sid, data):
    """Handle error messages"""
    logger.error(f"Error from client {sid}: {data}")
    await sio.emit('error', {'message': 'Error received and logged'}, room=sid)

@sio.event
async def ping(sid):
    """Handle ping for connection testing"""
    await sio.emit('pong', {'timestamp': datetime.now().isoformat()}, room=sid)

@sio.event
async def get_status(sid):
    """Handle status requests"""
    status = {
        'rag_available': rag_service is not None,
        'langgraph_available': langgraph_service is not None,
        'gemini_available': gemini_model is not None,
        'timestamp': datetime.now().isoformat()
    }
    await sio.emit('status', status, room=sid)

# Initialize services when module is imported
initialize_services()
