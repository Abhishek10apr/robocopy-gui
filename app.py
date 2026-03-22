from flask import Flask, request, jsonify, render_template
import subprocess
import os
import sys
import webbrowser
from threading import Timer

# 🚨 VVI — Fix paths for PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 🚨 VVI — Correct Flask paths
app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)


# 🌐 Home route
@app.route("/")
def home():
    return render_template("index.html")


# ⚙️ Run RoboCopy
@app.route("/run", methods=["POST"])
def run_robocopy():
    data = request.json

    source = data.get("source")
    destination = data.get("destination")
    options = data.get("options", "/E /Z /ETA")

    # Debug print (VERY useful)
    print("Incoming Data:", data)

    if not source or not destination:
        return jsonify({"error": "Source and Destination are required"}), 400

    try:
        # 🚨 VVI — DO NOT use shlex, pass full string
        cmd = f'robocopy "{source}" "{destination}" {options}'
        print("Running Command:", cmd)

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        output, error = process.communicate()

        return jsonify({
            "output": output,
            "error": error,
            "returncode": process.returncode
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🧪 TEST ROUTE (use this to verify RoboCopy works)
@app.route("/test")
def test():
    cmd = 'robocopy "C:\\Windows" "D:\\testcopy" /E /Z /ETA'

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    output, error = process.communicate()

    return f"<pre>{output}</pre>"


# 🌐 Auto-open browser
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# 🚀 Start app
if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=True)