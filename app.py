from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)


# 👉 Serve your frontend
@app.route("/")
def home():
    return render_template("index.html")


# 👉 Run robocopy
@app.route("/run", methods=["POST"])
def run_robocopy():
    data = request.json

    source = data.get("source")
    destination = data.get("destination")
    filename = data.get("filename", "")
    options = data.get("options", "")

    if not source or not destination:
        return jsonify({"error": "Source and Destination are required"}), 400

    try:
        cmd = f'robocopy "{source}" "{destination}"'

        if filename:
            cmd += f' "{filename}"'

        if options:
            cmd += f' {options}'

        print(f"Running Command: {cmd}")

        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = []
        for line in process.stdout:
            output.append(line)

        process.wait()

        return jsonify({
            "status": "success",
            "output": "".join(output)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# 👉 Preview command
@app.route("/preview", methods=["POST"])
def preview_command():
    data = request.json

    source = data.get("source")
    destination = data.get("destination")
    filename = data.get("filename", "")
    options = data.get("options", "")

    if not source or not destination:
        return jsonify({"error": "Source and Destination are required"}), 400

    cmd = f'robocopy "{source}" "{destination}"'

    if filename:
        cmd += f' "{filename}"'

    if options:
        cmd += f' {options}'

    return jsonify({
        "command": cmd
    })


if __name__ == "__main__":
    app.run(debug=True)