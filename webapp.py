from flask import Flask, request, render_template_string
from dork import perform_dorking

app = Flask(__name__)

HTML_TEMPLATE = '
<!doctype html>
<html>
<head>
    <title>Dorking Tool</title>
    <style>
        body { background: #111; color: #eee; font-family: monospace; padding: 20px; }
        input, button { padding: 10px; background: #222; color: #0f0; border: 1px solid #555; margin-bottom: 10px; }
        textarea { width: 100%; height: 400px; background: #000; color: #0f0; padding: 10px; border: none; }
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
'
