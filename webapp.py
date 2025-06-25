# webapp.py
from flask import Flask, request, render_template
from dork.py import perform_dorking  # Move functions to another file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        site = request.form['site']
        results = perform_dorking(site)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
