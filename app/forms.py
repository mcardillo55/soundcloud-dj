from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class SubmissionForm(Form):
	subURL = TextField('subURL', validators = [Required()])