from flask import Flask, request, render_template_string
from dork import perform_dorking

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Dorking Tool</title>
    <style>
        body { background: #111; color: #eee; font-family: monospace; padding: 20px; }
        input, button { padding: 10px; background: #222; color: #0f0; border: 1px solid #555; margin-bottom: 10px; }
        textarea { width: 100%; height: 400px; background: #000; color: #0f0; padding: 10px; border: none; white-space: pre; }
    </style>
</head>
<body>
    <h2>🕵️‍♂️ Google Dorking Tool by TheXM0G</h2>
    <form method="POST">
        <input name="site" placeholder="Enter domain (e.g., tryhackme.com)" required>
        <button type="submit">Start Dorking</button>
    </form>
    {% if logs %}
    <h3>🔍 Scan Log:</h3>
    <textarea readonly>{{ logs }}</textarea>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    logs = ""
    if request.method == "POST":
        site = request.form.get("site")
        if site:
            log_lines = perform_dorking(site)
            logs = "\n".join(log_lines)
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=10000)
