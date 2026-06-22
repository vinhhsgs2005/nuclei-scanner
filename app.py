from flask import Flask, request, render_template
import subprocess
import os
import time
app = Flask(name)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/scan", methods=["POST"])
def scan():
    target = request.form["target"]
    os.makedirs("results", exist_ok=True)
    output_file = f"results/output_{int(time.time())}.jsonl"
    cmd = [
        "nuclei",
        "-u", target,
        "-j",
        "-o", output_file,
        "-c", "5",
        "-rl", "5",
        "-bs", "10",
        "-s", "critical",
        "-silent",
        "-duc"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return f"Scan failed:<br><pre>{result.stderr}</pre>"
    except subprocess.TimeoutExpired:
        return "Scan timed out"
    return "Scan completed"
if name == "main":
    app.run(host="0.0.0.0", port=10000)
