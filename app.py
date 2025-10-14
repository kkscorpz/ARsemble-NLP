import os
from flask import Flask, render_template, request, jsonify
import sys
import traceback

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Print all files in directory for debugging
print("=== FILES IN DIRECTORY ===")
for file in os.listdir('.'):
    print(f"  - {file}")
print("==========================")

chatbot = None

try:
    print("🔄 Attempting to import ARsemble_ai...")
    from ARsemble_ai import PCChatbot
    print("✅ ARsemble_ai imported successfully!")

    print("🔄 Initializing PCChatbot...")
    chatbot = PCChatbot()
    print("✅ PCChatbot initialized successfully!")

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Available files:")
    for file in os.listdir('.'):
        print(f"  - {file}")
except Exception as e:
    print(f"❌ Initialization Error: {e}")
    traceback.print_exc()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    if chatbot is None:
        return jsonify({'response': 'Chatbot not initialized. Check server logs.'})

    try:
        user_message = request.json.get('message', '')
        print(f"📨 Received message: {user_message}")

        if not user_message:
            return jsonify({'response': 'Please enter a message'})

        response = chatbot.generate_response(user_message)
        print(f"🤖 Response: {response}")

        return jsonify({'response': response})

    except Exception as e:
        print(f"💥 Error in chat: {e}")
        traceback.print_exc()
        return jsonify({'response': f'Sorry, there was an error: {str(e)}'})


@app.route('/health')
def health():
    status = 'healthy' if chatbot else 'unhealthy'
    return jsonify({
        'status': status,
        'chatbot_loaded': chatbot is not None
    })


@app.route('/test')
def test():
    if chatbot is None:
        return jsonify({'message': 'ARsemble AI is not loaded'})

    try:
        # Test the chatbot
        test_response = chatbot.generate_response("price RTX 4060")
        return jsonify({
            'message': 'ARsemble AI is working!',
            'test_response': test_response
        })
    except Exception as e:
        return jsonify({
            'message': 'ARsemble AI test failed',
            'error': str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)
