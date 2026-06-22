from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target = request.form["target"]

    cmd = [
        "nuclei",
        "-u",
        target,
        "-json-export",
        "results/output.json"
    ]

    subprocess.run(cmd)

    return "Scan completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
