import os
from flask import Flask, render_template, request, jsonify

try:
    from ARsemble_ai import PCChatbot
    chatbot = PCChatbot()
    print("✓ ARsemble AI loaded successfully")
except ImportError as e:
    print(f"✗ Error importing ARsemble_ai: {e}")
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


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'chatbot_loaded': chatbot is not None})

# Add this to help with port detection


@app.route('/test')
def test():
    return jsonify({'message': 'ARsemble AI is working!'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
