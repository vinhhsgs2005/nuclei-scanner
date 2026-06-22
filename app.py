from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    target = request.form["target"]

    # Đã thêm các cờ tối ưu RAM vào mảng cmd
    cmd = [
        "nuclei",
        "-u", target,
        "-json-export", "results/output.json",
        "-c", "10",              
        "-bs", "5",               
        "-disable-update-check",  
        "-ni"                     
    ]

    subprocess.run(cmd)

    return "Scan completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
