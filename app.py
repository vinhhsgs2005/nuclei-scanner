from flask import Flask, request, render_template
import subprocess
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target = request.form["target"]
    output_file = "results/output.jsonl"
    #localhost does not need: "-tags", "cve,exposures",  -c:10, -bs:5
    cmd = [
        "nuclei",
        "-u", target,
        "-j", "-o", output_file,
        "-c", "50",              
        "-bs", "25",
        "-disable-update-check",  
        "-ni"
    ]
    
    subprocess.run(cmd)

    scan_results = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    scan_results.append(data)
                except:
                    continue
        
        os.remove(output_file)
        
    return render_template("results.html", target=target, results=scan_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
