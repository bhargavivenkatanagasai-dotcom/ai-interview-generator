from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import time

app = Flask(__name__)
CORS(app)

client = genai.Client(
    api_key=""
)

@app.route("/")
def home():
    return "Backend Working"


# Generate Interview Questions
@app.route("/get-question", methods=["POST"])
def get_question():

    try:

        data = request.json

        role = data.get("role", "")
        difficulty = data.get("difficulty", "Easy")

        prompt = f"""
Generate exactly 3 {difficulty} interview questions for {role}.

Rules:
- Each question must be one line only.
- Maximum 15 words per question.
- No explanations.
- No answers.
- No extra text.

Format:

1.
2.
3.
"""

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                return jsonify({
                    "question": response.text
                })

            except Exception as e:

                if "503" in str(e) and attempt < 2:
                    time.sleep(5)
                else:
                    raise e

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "question": "Backend error occurred",
            "error": str(e)
        })


# Evaluate User Answer
@app.route("/evaluate-answer", methods=["POST"])
def evaluate_answer():

    try:

        data = request.json

        question = data.get("question", "")
        answer = data.get("answer", "")

        prompt = f"""
Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Format exactly:

Score: X/10

Strengths:
• Point 1
• Point 2

Improvements:
• Point 1
• Point 2

Missing Points:
• Point 1
• Point 2

Rules:
- Keep response under 100 words.
- Use bullet points only.
- No paragraphs.
- Be concise.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "evaluation": response.text
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "evaluation": "Evaluation failed",
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)