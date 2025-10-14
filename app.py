import os
from flask import Flask, render_template, request, jsonify
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Import and initialize the REAL AI from ARsemble_ai.py
try:
    from ARsemble_ai import PCChatbot
    chatbot = PCChatbot()
    print("✅ ARsemble AI loaded successfully!")
except ImportError as e:
    print(f"❌ Error importing ARsemble_ai: {e}")
    chatbot = None
except Exception as e:
    print(f"❌ Error initializing chatbot: {e}")
    chatbot = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    if chatbot is None:
        return jsonify({'response': 'Chatbot not initialized. Check server logs.'})

    try:
        user_message = request.json.get('message', '')
        print(f"📨 Received: {user_message}")

        response = chatbot.generate_response(user_message)
        print(f"🤖 Response: {response}")

        return jsonify({'response': response})

    except Exception as e:
        print(f"💥 Error: {e}")
        return jsonify({'response': 'Sorry, there was an error.'})


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'ai_loaded': chatbot is not None})


@app.route('/test')
def test():
    if chatbot:
        test_response = chatbot.generate_response("price RTX 4060")
        return jsonify({
            'message': 'ARsemble AI Working!',
            'test_response': test_response
        })
    return jsonify({'message': 'AI not loaded'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
