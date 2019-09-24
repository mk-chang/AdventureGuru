from flask import session,render_template, request, Blueprint, redirect, url_for
from AdventureGuruApp import db
from AdventureGuruApp.models import Destination, Demo
from AdventureGuruApp.destinations.ML import Load_Data, Run_Model, Train_demoModel
import time

destinations = Blueprint('destinations',__name__)

@destinations.route('/Locations')
def Destination_Locations():
    Locations = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    Locations = [location[0] for location in Locations]

    return render_template('destination_locations.html',Locations=Locations)

@destinations.route('/Destinations/<string:location>')
def Destinations(location):
    Destinations = Destination.query.filter_by(location=location).order_by(Destination.title)
    Locations = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    Locations = [location[0] for location in Locations]

    return render_template('destinations.html',Destinations=Destinations,location=location,Locations=Locations)

@destinations.route('/Share_Locations', methods=['GET','POST'])
def Share_Locations():

    if request.method == 'POST':
        selectedLocations = []
        for location,selected in request.form.items():
            print(location)
            print(selected)
            if selected == 'on':
                selectedLocations.append(location)
        print('############################## Share Locations - POST ####################################')
        print(selectedLocations)
        return redirect(url_for('destinations.Share_Destinations',selectedLocations=selectedLocations))

    locationList = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    locationList = [location[0] for location in locationList]

    return render_template('locations.html',locationList=locationList)

@destinations.route('/Share_Destinations/<string:selectedLocations>', methods=['GET','POST'])
def Share_Destinations(selectedLocations):
    if request.method == "POST":
        print('############################## Share Destinations - POST ####################################')
        print(request.form.items())
        inputData = []
        for title,review in request.form.items():
            if review == '1':
                inputData.append((title,1))
            elif review == '-1':
                inputData.append((title,0))
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

@destinations.route('/Train_Model', methods=['GET'])
def Train_Model():
    if 'inputData' not in session:
        return redirect(url_for('destinations.Share_Locations'))
    else:
        return render_template('train.html')

@destinations.route('/Recommend_Location_Options')
def Recommend_Location_Options():
    #Data Input
    print('############################## Data Input ####################################')
    inputData = session['inputData']
    print("Input Data")
    print(inputData)
    trainData,trainLabel = Load_Data(inputData)
    print("trainData")
    print(trainData)
    print("trainData")
    print(trainLabel)

    #Train Model
    print('############################## Training Model ####################################')
    model_id = Train_demoModel(trainData,trainLabel)
    session['demo_model'] = model_id

    #Provide Locations
    Locations = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    Locations = [i[0] for i in Locations]

    return render_template('recommend.html',Locations=Locations)

@destinations.route('/Recommendations/<string:location>')
def Recommendations(location):
    time.sleep(2)

    print('############################## Running Model ####################################')
    #Initialize Recommendations Dict
    recommendations = {
        "Must-Go":[],
        "Recommend":[],
        "Avoid":[],
        }

    #Run Each Destination in Location
    if 'demo_model' in session:
        model_id = session['demo_model']
        destinations = Destination.query.filter_by(location=location)
        for destination in destinations:
            recommendation = Run_Model(model_id,destination.title)
            print(destination.title+": "+str(recommendation))
            if recommendation > 0.9:
                recommendations['Must-Go'].append(destination)
            elif recommendation > 0.5:
                recommendations['Recommend'].append(destination)
            elif recommendation < 0.2:
                recommendations['Avoid'].append(destination)

    Locations = db.session.query(Destination.location.distinct()).order_by(Destination.location).all()
    Locations = [i[0] for i in Locations]

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
