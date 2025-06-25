from flask import Flask, request
from dork import perform_dorking
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dorking Tool</title>
    <style>
        body {{ background-color: #0f1117; color: #f8f8f2; font-family: monospace; padding: 20px; }}
        input[type="text"] {{ width: 300px; padding: 8px; }}
        input[type="submit"] {{ padding: 8px 16px; background-color: #50fa7b; border: none; color: black; cursor: pointer; }}
        pre {{ background-color: #282a36; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Google Dorking (via Bing) Tool</h1>
    <form method="POST">
        <label>Enter domain (e.g., nasa.gov):</label><br><br>
        <input type="text" name="site" required>
        <input type="submit" value="Start Dorking">
    </form>
    <hr>
    {results}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    results_output = ""
    if request.method == 'POST':
        site = request.form['site'].strip()
        dork_results = perform_dorking(site)
        if dork_results:
            results_output += "<pre>"
            for res in dork_results:
                results_output += res + "\n"
            results_output += "</pre>"
        else:
            results_output = "<p>No results found.</p>"

    return HTML_TEMPLATE.format(results=results_output)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # For Render deployment
    app.run(host='0.0.0.0', port=port, debug=True)
