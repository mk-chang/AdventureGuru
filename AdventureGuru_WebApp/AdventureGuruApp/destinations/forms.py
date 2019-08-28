from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField, SubmitField,FieldList,FormField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    locations = SelectMultipleField(u'Locations',[DataRequired()])
    submit = SubmitField('Next')

class DestinationForm(FlaskForm):
    id = IntegerField('id')
    title = HiddenField('Destination Title')
    review = RadioField('Review',choices=[(-1,'Bad'),(1,'Good')])

class ExperienceForm(FlaskForm):
    destinations = FieldList(FormField(DestinationForm))
    submit = SubmitField('Next')
