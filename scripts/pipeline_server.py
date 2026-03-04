from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/run-pipeline")
def run_pipeline():
    subprocess.run(["python", "scripts/run_pipeline.py"])
    return {"status": "pipeline executed"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)