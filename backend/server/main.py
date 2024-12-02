from flask import Flask, request, jsonify
from model import TextAnalyzer
from sql_service import *
from flask_cors import CORS
from sql_service import get_all_files, get_file_by_id, get_file_path
import base64
import mimetypes

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def get_metadata():
    if "file" not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files["file"]

    if not file:
        return jsonify({"error": "No file provided"}), 400
    folder_id = request.args.get("folderId")
    
    analyzer = TextAnalyzer()
    metadata_instance = analyzer.get_metadata(
        file, temperature=0.7, max_tokens=1000, top_p=1, folder_id=folder_id
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
    return jsonify(get_all_files("db_config.json"))


@app.route("/<int:file_id>", methods=["GET"])
def get_file(file_id):
    metadata_instance = get_file_by_id("db_config.json", file_id)
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


@app.route("/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    response = delete_file_by_id("db_config.json", file_id)
    return response


@app.route("/file/<int:file_id>", methods=["GET"])
def get_blob_file(file_id):
    file_path = get_file_path("db_config.json", file_id)

    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404

    _, file_extension = os.path.splitext(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    if not mime_type:
        return {"error": "Unable to determine file type"}, 400

    with open(file_path, "rb") as file:
        file_content = file.read()

    encoded_file = base64.b64encode(file_content).decode("utf-8")

    return {"file_type": mime_type, "file_data": encoded_file}


@app.route("/folders", methods=["GET"])
def get_folders():
    try:
        folders = get_all_folders("db_config.json")
        print(folders)
        return jsonify(folders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/folders", methods=["POST"])
def create_folder_route():
    try:
        data = request.get_json()
        name = data.get("name")
        parent_folder_id = data.get("parent_folder_id")

        if not name:
            return jsonify({"error": "Folder name is required"}), 400

        new_folder = create_folder("db_config.json", name, parent_folder_id)
        return jsonify(new_folder), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/folders/<int:folder_id>", methods=["DELETE"])
def delete_folder_route(folder_id):
    try:
        response = delete_folder("db_config.json", folder_id)
        if "error" in response:
            return jsonify(response), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # create_tables('../db_scripts/create_tables.sql', 'db_config.json')
    # insert_user('db_config.json')
    app.run(debug=True)
