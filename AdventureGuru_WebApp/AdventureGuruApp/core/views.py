from flask import render_template, request, Blueprint, flash
from AdventureGuruApp import mail
from AdventureGuruApp.core.forms import ContactForm
from flask_mail import Message

core = Blueprint('core',__name__)

@core.route('/')
def index():
    return render_template('home.html')

@core.route('/HowItWorks')
def info():
    return render_template('info.html')

@core.route('/about')
def about():
    return render_template('about.html')

@core.route('/contact',methods=['GET','POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html',form=form)
        else:
          msg = Message(subject=form.subject.data, sender='adventuregurutravels@gmail.com', recipients=['adventuregurutravels@gmail.com'])
          msg.body = """
            FROM:
            %s
            
            Email:
            %s

            MESSAGE:
            %s
          """ % (form.name.data, form.email.data, form.message.data)
          mail.send(msg)
          return render_template('contact.html',success=True)

    elif request.method == 'GET':
        return render_template('contact.html',form=form)
