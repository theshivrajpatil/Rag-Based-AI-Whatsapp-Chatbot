from flask import Flask, request, jsonify
from rag.generator import generate_answer

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message missing"}), 400

    response = generate_answer(user_message)

    return jsonify({
        "reply": response
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)