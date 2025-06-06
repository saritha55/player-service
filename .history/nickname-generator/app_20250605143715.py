from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load TinyLlama model pipeline for text generation
chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

@app.route('/generate-nickname', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        country = data.get('country', '').strip()

        if not country:
            return jsonify({"error": "Missing 'country' field"}), 400

        prompt = (
    f"Nickname:"
    f" Provide ONE unique and creative nickname for a player from {country}."
    f" Output ONLY the nickname (one or two words), no explanation."
)

output = chat(prompt, max_new_tokens=20)[0]['generated_text']

# Remove the prompt from the output
nickname = output[len(prompt):].strip()

# Sometimes model adds quotes or punctuation; clean those
nickname = nickname.strip(' "\'.')

# If nickname still looks like instruction, fallback
if len(nickname) < 2 or any(word in nickname.lower() for word in ["ensure", "nickname", "player"]):
    nickname = "PlayerX"

return jsonify({"nickname": nickname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run Flask app with debug for easier troubleshooting
    app.run(host='0.0.0.0', port=5000, debug=True)
