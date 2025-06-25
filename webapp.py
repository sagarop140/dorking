from flask import Flask, request, render_template_string
from dork import perform_dorking
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dorking Tool</title>
</head>
<body style='background-color:#1e1e1e; color:#00ffff; font-family:monospace;'>
    <h1>Dorking Tool 🔍</h1>
    <form method='POST'>
        <input type='text' name='site' placeholder='Enter domain like example.com' required>
        <input type='submit' value='Start Dorking'>
    </form>
    {% if site %}
        <h3>Dorking on: <span style='color:orange;'>{{ site }}</span></h3>
        {% if results %}
            <h4>Results Found:</h4>
            <ul>
                {% for r in results %}
                    <li><a href='{{ r }}' target='_blank' style='color:lightgreen;'>{{ r }}</a></li>
                {% endfor %}
            </ul>
        {% else %}
            <p style='color:red;'>No results found for this domain.</p>
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    site = None
    if request.method == 'POST':
        site = request.form['site']
        results = perform_dorking(site)
    return render_template_string(HTML_TEMPLATE, results=results, site=site)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
