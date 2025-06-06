from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load TinyLlama model pipeline for text generation
chat = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

@app.route('/generate-nickname', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = f"Suggest a nickname for a player from {data['country']}."
    output = chat(prompt, max_new_tokens=20)[0]['generated_text']
    return jsonify({"nickname": output.strip()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
