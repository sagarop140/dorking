from flask import Flask, request, render_template_string
from dork import perform_dorking
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Dorking Tool</title>
    <style>
        body { font-family: Arial, sans-serif; background: #121212; color: #e0e0e0; padding: 2rem; }
        input[type=text] { width: 300px; padding: 0.5rem; font-size: 1rem; }
        button { padding: 0.5rem 1rem; font-size: 1rem; margin-left: 10px; cursor: pointer; }
        pre { background: #222; padding: 1rem; border-radius: 5px; overflow-x: auto; max-height: 500px; }
        h1 { color: #00bcd4; }
    </style>
</head>
<body>
    <h1>Advanced Bing Dorking Tool</h1>
    <form method="post">
        <input name="site" type="text" placeholder="Enter domain (e.g. nasa.gov)" required />
        <button type="submit">Start Dorking</button>
    </form>
    {% if logs %}
    <h2>Results:</h2>
    <pre>{{ logs }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    logs = None
    if request.method == 'POST':
        site = request.form.get('site', '').strip()
        if site:
            logs_list = perform_dorking(site)
            logs = '\n'.join(logs_list)
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
