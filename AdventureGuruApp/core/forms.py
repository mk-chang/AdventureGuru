from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
  name = StringField("Name",validators=[DataRequired("Please enter your name.")])
  email = StringField("Email",validators=[DataRequired("Please enter your email address."),Email("Please enter a valid email address.")])
  subject = StringField("Subject",validators=[DataRequired("Please enter a subject.")])
  message = TextAreaField("Message",validators=[DataRequired("Please enter a message.")])
  submit = SubmitField("Send")
