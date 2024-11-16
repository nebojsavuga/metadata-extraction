from flask import Flask, request, jsonify
from model import TextAnalyzer
import pyodbc
import json

app = Flask(__name__)

def load_db_config():
    with open('db_config.json', 'r') as file:
        config = json.load(file)
    return config

@app.route("/", methods=["POST"])
def get_metadata():
    if "file" not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files["file"]

    if not file:
        return jsonify({"error": "No file provided"}), 400

    analyzer = TextAnalyzer()
    metadata_instance = analyzer.get_metadata(
        file, model="llama3-8b-8192", temperature=0.7, max_tokens=1000, top_p=1
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
    db_config = load_db_config()
    server = db_config['server']
    database = db_config['database']
    driver = db_config['driver']
    connection = pyodbc.connect(
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )

    app.run(debug=True)
