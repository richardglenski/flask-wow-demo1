import json

from flask import Flask, render_template, make_response
from app import app
import pdfkit
import pandas as pd

def get_data():
      # Graph data #
    df = pd.read_csv('data.csv').drop('Open', axis=1)
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return data

@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', title='Home', data=get_data())

@app.route('/generate_pdf')
def generate_pdf():
    css='app/static/main.css'
    rendered = render_template('index.html', data=get_data())
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=output.pdf'

    return response