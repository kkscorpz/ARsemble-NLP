import os
import sys
from flask import Flask, render_template, request, jsonify

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ARsemble_ai import PCChatbot
    chatbot = PCChatbot()
    print("✓ ARsemble AI loaded successfully")
except ImportError as e:
    print(f"✗ Error importing ARsemble_ai: {e}")
    print("Make sure ARsemble_ai.py exists in the same directory")
    chatbot = None

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
        if not user_message:
            return jsonify({'response': 'Please enter a message'})

        response = chatbot.generate_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Sorry, there was an error: {str(e)}'})


if __name__ == '__main__':
    print("Starting ARsemble AI Chatbot...")
    print(" Current directory:", os.getcwd())
    print(" Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
