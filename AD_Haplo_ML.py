from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, SubmitField, FloatField, IntegerField
from Helper_Functions import get_intervals
import os

app = Flask(__name__)
app.secret_key='a-secret'

class UploadForm(FlaskForm):
    p_value = FloatField('P Value')
    exponent = IntegerField()
    window = IntegerField()
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Search')

@app.route('/')
def index():
    form = UploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file_path = os.path.join(app.instance_path, 'files', f.filename)
            f.save(file_path)
            get_intervals(file_path, './outfiles/output', './outfiles/gnomadout', form.p_value.data*(10**form.exponent.data), form.window.data, '/filestore/gnomad/gnomad.genomes.r2.1.1.sites.vcf.bgz')
            return render_template('result.html', img='./outfiles/output')

    return render_template('index.html', form=form)

@app.route('/result')
def result():
    return render_template('result.html', img=img)
