from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from root.create_app import app
import uuid
import os
import time
import calendar


def create_app():
    @app.route("/")
    def upload_file():
        return render_template("index.html")

    @app.route("/upload_by_url", methods=["GET", "POST"])
    def save_file():
        if request.method == "POST":
            try:
                print(request.files, flush=True)
                f = request.files["file"]
                filename = secure_filename(f.filename)
                current_GMT = time.gmtime()

                time_stamp = calendar.timegm(current_GMT)
                dir = (
                    str(time_stamp)
                    + str(uuid.uuid4())
                    + "-"
                    + str(uuid.uuid4())
                    + "-"
                    + str(uuid.uuid4())
                )
                os.mkdir("/app/store/" + dir)

                url = dir + "/" + filename
                f.save(
                    "/app/store/" + url,
                )

                file = open("/app/store/" + url, "rb")
                content = file.read()
            except Exception as e:
                print(e, flush=True)
                return render_template("content.html", content="error")

        return render_template(
            "content.html",
            content="http://save.mock-interview.orby-tech.space/static/" + url,
        )

    @app.route("/upload_by_url_json", methods=["GET", "POST"])
    def save_file_json():
        if request.method == "POST":
            f = request.files["file"]
            filename = secure_filename(f.filename)
            current_GMT = time.gmtime()

            time_stamp = calendar.timegm(current_GMT)
            dir = (
                str(time_stamp)
                + str(uuid.uuid4())
                + "-"
                + str(uuid.uuid4())
                + "-"
                + str(uuid.uuid4())
            )
            os.mkdir("/app/store/" + dir)

            url = dir + "/" + filename
            f.save(
                "/app/store/" + url,
            )

            file = open("/app/store/" + url, "rb")
            content = file.read()

        return "http://save.mock-interview.orby-tech.space/static/" + url

    @app.route("/static/<dir>/<name>")
    def send_js(dir, name):
        return send_from_directory("/app/store/", dir + "/" + name)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0")
