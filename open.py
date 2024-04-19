from flask import Flask, request, jsonify
import openai
import os
app = Flask(__name__)

# Set up OpenAI API key

openai.api_key = os.environ.get("OPENAI_API_KEY")
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    prompt = data.get('prompt', '')
    age = data.get('age', '')
    company = data.get('company', '')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        messages = [
            {"role": "system", "content": f"You are responding on behalf of a person with age {age} who works at {company}."},
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=256,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        generated_text = response.choices[0].message.content.strip()
        return jsonify({'result': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)