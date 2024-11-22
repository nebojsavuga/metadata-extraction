from flask import Flask, request, jsonify
from model import TextAnalyzer
from sql_service import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


@app.route("/", methods=["GET"])
def get_files():
    return ''

@app.route("/file/<int:file_id>", methods=["GET"])
def get_file(file_id):
    return ''

if __name__ == "__main__":
    #create_tables('../db_scripts/create_tables.sql', 'db_config.json')
    #insert_user('db_config.json')
    app.run(debug=True)
