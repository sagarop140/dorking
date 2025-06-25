from flask import Flask, request, render_template_string
from dork import perform_dorking  # Make sure perform_dorking returns the results list

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DuckDuckGo Dorking Tool</title>
</head>
<body style="background-color:#1e1e1e; color:#00ffff; font-family:monospace;">
    <h1>DuckDuckGo Dorking Tool</h1>
    <form method="POST">
        <input type="text" name="site" placeholder="Enter site (e.g. example.com)" required>
        <input type="submit" value="Start Dorking">
    </form>
    {% if results %}
    <h2>Results:</h2>
    <ul>
        {% for r in results %}
        <li><a href="{{ r }}" style="color:lightgreen;" target="_blank">{{ r }}</a></li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        site = request.form['site']
        results = perform_dorking(site)
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(debug=True)
