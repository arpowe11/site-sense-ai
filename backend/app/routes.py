from typing import Any
from flask import Blueprint, request, jsonify, current_app
from .agent_logic import SiteSenseAI

import markdown


bp: Blueprint = Blueprint("main", __name__)

@bp.route("/chat", methods=["POST"])
def get_response():
    agent_emily: SiteSenseAI = SiteSenseAI(temp=0.8, config=current_app.config)

    try:
        data: Any = request.json
        question: str = data.get("question")

        if not question:
            return jsonify({"error": "Missing 'question' field"}), 400

        ai_response: dict = agent_emily.engage(question)
        converted_response_text: str = markdown.markdown(
            ai_response["output"], extensions=["extra", "nl2br"]
        )

        return jsonify({"ai_response": converted_response_text}), 200

    except Exception as ex:
        return jsonify({"error": f"Something went wrong: {str(ex)}"}), 400
