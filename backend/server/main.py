from flask import Flask, request, jsonify
from model import TextAnalyzer

app = Flask(__name__)

@app.route("/", methods=["POST"])
def get_metadata():
    # Retrieve text from the request body
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text parameter is required"}), 400

    analyzer = TextAnalyzer()
    metadata_instance = analyzer.get_metadata(
        text,
        model="llama3-70b-8192", 
        temperature=0.7, 
        max_tokens=150, 
        top_p=1
    )
    
    response_data = {
        "general": metadata_instance.general.__dict__,
        "lifeCycle": metadata_instance.lifeCycle.__dict__,
        "tehnical": metadata_instance.tehnical.__dict__,
        "educational": metadata_instance.educational.__dict__,
        "rights": metadata_instance.rights.__dict__,
        "relation": metadata_instance.relation.__dict__,
        "classification": metadata_instance.classification.__dict__,
    }

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
