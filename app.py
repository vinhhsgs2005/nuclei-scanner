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
        "-u", target,
        "-json-export", "results/output.json",
        
        # 1. SCOPE REDUCTION (Crucial for Memory)
        # Only load specific tags (e.g., cve, misconfiguration, exposures) 
        # instead of loading the entire 8000+ template database
        "-tags", "cve,exposures", 
        
        # 2. EXTREME THROTTLING
        "-c", "2",                # Only 2 concurrent templates
        "-bs", "2",               # Bulk size of 2
        "-rl", "15",              # Hard rate limit: Max 15 requests per second
        
        # 3. OVERHEAD REDUCTION
        "-disable-update-check",  # Stop background memory usage
        "-nc",                    # No color (saves a tiny bit of buffer overhead)
        "-ni"                     # Non-interactive
    ]

    subprocess.run(cmd)

    return "Scan completed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
