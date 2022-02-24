from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from .file_validation import jhove_validation
import configparser
import os


def start():
    config = configparser.ConfigParser()
    config.read("./config")

    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = config["API"]["UploadFolder"]
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1GB

    @app.route("/api/validate", methods=["POST"])
    def validate():
        # check if there is a file
        if "file" not in request.files:
            return Response('{error: "no file provided"}', status=400)

        file = request.files["file"]

        # check if the file has a name
        if file.filename == "":
            return Response('{error: "invalid file name"}', status=400)

        # check if file has valid extension
        file_ext = os.path.splitext(file.filename)[1]
        if file_ext not in {".jpeg", ".jpg", ".tiff", ".tif"}:
            return Response('{error: "invalid file type"}', status=400)

        # lets go upload time!
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # check file
        validation_output = jhove_validation(
            os.path.join(config["API"]["UploadFolder"], filename),
            config["JHOVE"]["JhoveInstallPath"],
        )

        # return result
        return Response("{isValid:" + str(validation_output[1]) + "}", status=200)

    app.run()
