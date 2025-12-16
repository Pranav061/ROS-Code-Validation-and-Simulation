from flask import Flask, render_template, request
from code_checker import run_all
from simulation_runner import run_simulation


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
report = None
sim = None
if request.method == 'POST':
f = request.files['zipfile']
path = 'uploads/code.zip'
f.save(path)
report = run_all(path)
if not report['syntax'] and not report['structure']:
sim = run_simulation()
return render_template('index.html', report=report, sim=sim)


app.run(debug=True)
