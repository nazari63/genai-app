from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"response": response['choices'][0]['message']['content'].strip()})
    except openai.error.InvalidRequestError as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
    except openai.error.AuthenticationError as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    except openai.error.APIConnectionError as e:
        return jsonify({"error": f"API connection error: {str(e)}"}), 503
    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
