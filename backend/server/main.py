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
    keywords = analyzer.get_metadata(
        text,
        model="llama3-70b-8192", 
        temperature=0.7, 
        max_tokens=150, 
        top_p=1
    )
    
    return jsonify({"keywords": keywords})
if __name__ == "__main__":
    app.run(debug=True)
