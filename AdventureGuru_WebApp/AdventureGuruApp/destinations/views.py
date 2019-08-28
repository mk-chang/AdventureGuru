from flask import session,render_template, request, Blueprint, redirect, url_for
from AdventureGuruApp import db
from AdventureGuruApp.models import Destination
from AdventureGuruApp.ML import recomendationModel
from AdventureGuruApp.destinations.forms import LocationForm, ExperienceForm
import time


destinations = Blueprint('destinations',__name__)

@destinations.route('/Share_Locations', methods=['GET','POST'])
def Share_Locations():

    if request.method == 'POST':
        selectedLocations = []
        for location,selected in request.form.items():
            if selected == 'on':
                selectedLocations.append(location)
        print(selectedLocations)
        return redirect(url_for('destinations.Share_Destinations',selectedLocations=selectedLocations))

    locationList= db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    locationForm = [(i[0],"/static/location_pics/location_pic.jpeg") for i in locationList]
    #locationPics.append("/static/location_pics/"+location+".jpeg")
    return render_template('locations.html',locationForm=locationForm)

@destinations.route('/Share_Destinations/<string:selectedLocations>', methods=['GET','POST'])
def Share_Destinations(selectedLocations):
    if request.method == "POST":
        print('############################## Share Destinations - POST ####################################')
        print(request.form)
        inputData = []
        for title,review in request.form.items():
            if review == '1':
                inputData.append((title,1))
            elif review == '-1':
                inputData.append((title,-1))
        print('Input Data')
        print(inputData)
        session['inputData']=inputData

        return redirect(url_for('destinations.Train_Model'))
        #return redirct(url_for('destinations.train_Model'))

    print('############################## Share Destinations - GET ####################################')
    print('Selected Locations')
    print(selectedLocations)

    if selectedLocations == "none":
        Locations= db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
        Locations = [i[0] for i in locationList]
    else:
        #Parse the input
        Locations = []
        notLetter = ["[","]","'",","," "]
        word = ""
        for string in selectedLocations:
            if string in notLetter:
                if word and string == "'":
                    Locations.append(word)
                    word = ""
            else:
                word+=string
        print('Locations')
        print(Locations)

    #Pre-populate Form
    experienceForm = []
    for location in Locations:
        destinationForms = Destination.query.filter_by(location=location).order_by(Destination.title)
        experienceForm.append((location,destinationForms))
    print('Form Data')
    print(experienceForm)

    return render_template('share.html',experienceForm=experienceForm)

@destinations.route('/Recommend_Destinations', methods=['GET'])
def Train_Model():
    if 'inputData' not in session:
        return redirect(url_for('destinations.Share_Locations'))
    else:
        inputData = session['inputData']
        print("Input Data")
        print(inputData)
        return render_template('train.html')

@destinations.route('/Recommend_Location')
def Recommend_Location():
    time.sleep(2)
    #Data Input

    #Train Model

    session['model'] = True

    #Provide Locations
    Locations = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    Locations = [i[0] for i in Locations]

    return render_template('recommend.html',Locations=Locations)

@destinations.route('/Recommendations/<string:location>')
def Recommendations(location):
    time.sleep(2)

    Locations = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    Locations = [i[0] for i in Locations]

    recommendations = {
        "Must-Go":[],
        "Recommend":[],
        "Avoid":[],
        }
    if 'model' in session:
        for category in recommendations.keys():
            destinations = Destination.query.filter_by(location=location)
            recommendations[category] = destinations

    return render_template('recommendations.html',recommendations=recommendations,Locations=Locations)


'''
#######################################################################################

                                        #Archive

#######################################################################################
@destinations.route('/share_Experience', methods=['GET','POST'])
def share_Experience():
    locationList= db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    locationList = [location.location for location in locationList]

    currentLocation = request.args.get('location', locationList[0].location, type=string)

    destinations = Destination.query.filter_by(location=currentLocation)order_by(Destination.title)

    if ExperienceForm.validate_on_submit() :
        return redirct(url_for('train_Model'))

    return render_template('input.html',locationList=locationList,destinations=destinations)

@destinations.route('/good_Experience', methods=['POST'])
def good_Experience():
    destination = request.form['destination']
    Session[inputData].append((destination,1))
    return


@destinations.route('/bad_Experience', methods=['POST'])
def bad_Experience():
    destination = request.form['destination']
    Session[inputData].append((destination,-1))
    return

@destinations.route('/Share_Experience_Locations', methods=['GET','POST'])
def Share_Experience_Locations():

    form = LocationForm()
    locationList= db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    locationList = [i[0] for i in locationList]
    form.locations.choices = zip(locationList,locationList)

    if form.validate_on_submit() :
        selectedLocations = form.locations.data
        return redirect(url_for('destinations.Share_Experience_Destinations',selectedLocations=selectedLocations))

    return render_template('locations.html',form=form)

@destinations.route('/Share_Experience_Destinations/<string:selectedLocations>', methods=['GET','POST'])
def Share_Experience_Destinations(selectedLocations):

    print('############################## DEBUG ####################################')
    print('Selected Locations')
    print(selectedLocations)

    #Parse the input
    Locations = []
    notLetter = ["[","]","'",","," "]
    word = ""
    for string in selectedLocations:
        if string in notLetter:
            if word and string == "'":
                Locations.append(word)
                word = ""
        else:
            word+=string
    print('Locations')
    print(Locations)

    #Pre-populate Form
    destinations = []
    id = 0

    experienceForm = ExperienceForm()

    for location in Locations:
        destinationList = Destination.query.filter_by(location=location).order_by(Destination.title)
        destinationFormData = []
        for destination in destinationList:
            #Add destinations
            destinationData = dict(zip(["title","id"], [destination.title,destination.id]))
            destinations.append(destination)
            id+=1
            destinationFormData.append(destinationData)
        locationFormData = dict(zip(["title","destinations"],[location,destinationFormData]))
        print(locationFormData)
        print('Form Data')
        experienceForm.locations.append_entry(locationFormData)

    if experienceForm.validate_on_submit():
        return redirct(url_for('destinations.train_Model'))

    return render_template('share.html',experienceForm=experienceForm,destinations=destinations)

@destinations.route('/Share_Experience_Locations', methods=['GET','POST'])
def Share_Experience_Locations():

    form = LocationForm()

    locationList= db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    locationList = [i[0] for i in locationList]

    locationPics = []
    for location in locationList:
        #locationPics.append(location+".jpeg")
        locationPics.append("/static/location_pics/location_pic.jpeg")

    form.locations.choices = zip(locationList,locationList)

    if form.validate_on_submit() :
        selectedLocations = form.locations.data
        return redirect(url_for('destinations.Share_Experience_Destinations',selectedLocations=selectedLocations))

    return render_template('locations.html',form=form,locationPics=locationPics)

@destinations.route('/Share_Experience_Destinations/<string:selectedLocations>', methods=['GET','POST'])
def Share_Experience_Destinations(selectedLocations):

    print('############################## DEBUG ####################################')
    print('Selected Locations')
    print(selectedLocations)

    #Parse the input
    Locations = []
    notLetter = ["[","]","'",","," "]
    word = ""
    for string in selectedLocations:
        if string in notLetter:
            if word and string == "'":
                Locations.append(word)
                word = ""
        else:
            word+=string
    print('Locations')
    print(Locations)

    #Pre-populate Form
    destinations = []
    locationIndex = []
    id = 0
    experienceForm = ExperienceForm()

    for location in Locations:
        destinationList = Destination.query.filter_by(location=location).order_by(Destination.title)
        for destination in destinationList:
            #Add destination form entry
            destinationFormData = dict(zip(["title","id"], [destination.title,id]))
            experienceForm.destinations.append_entry(destinationFormData)
            id+=1
            print('Form Data')
            print(destinationFormData)

            #Add destination object to list
            destinations.append(destination)

        locationIndex.append(id)

    if experienceForm.validate_on_submit():
        inputData = []
        for form in experienceForm.destinations:
            inputData.append(form.title.data,form.review.data)
        print(inputData)
        Session['inputData']=inputData
        return redirct(url_for('destinations.Train_Model'),inputData=inputData)

    return render_template('share.html',experienceForm=experienceForm,destinations=destinations, locationIndex=locationIndex)
'''
