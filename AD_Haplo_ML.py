from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SelectField, SubmitField, FloatField, IntegerField
import Helper_Functions
import os

app = Flask(__name__)
# Required for forms.
app.secret_key='9dfm3id8v732mfdmd3poak3krp40cj93d'

class UploadForm(FlaskForm):
    p_value = FloatField('P Value')
    exponent = IntegerField()
    window = IntegerField()
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    # If form is submitted (and valid)
    if request.method == 'POST':
        if form.validate_on_submit():
            # The default values that show up weren't actually being passed.
            p_value = form.p_value.data or 5
            exponent = form.exponent.data or -12
            window = form.window.data or 10000
            f = form.file.data
            # Just save file to current directory.
            file_path = os.path.join('.', f.filename)
            f.save(file_path)
            Helper_Functions.get_intervals(file_path, './output', './gnomadout', float(p_value)*(10**int(exponent)), window, '/filestore/gnomad/gnomad.genomes.r2.1.1.sites.vcf.bgz')
            return render_template('result.html', img='./outfiles/output')

    return render_template('index.html', form=form)

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', img=img)
