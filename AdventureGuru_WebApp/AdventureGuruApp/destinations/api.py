from flask import request
from flask_restful import Resource
from AdventureGuruApp import db
from AdventureGuruApp.models import Destination, Type, Time, Age, association_table, Demo

##############################################################

                        #Functions

##############################################################

def String_to_List(string):
    # Converts a string to a 1D python string list
    # Example 1. "aa,bb,cc,dd" --> ["aa","bb","cc","dd"]
    if type(string) is not str:
        return None
    List = []
    word = ""
    stringLength = len(string)
    for i in range(stringLength):
        char = string[i]
        if i==stringLength-1:
            word+=char
            List.append(word)
        elif char =="," and word:
            List.append(word)
            word = ""
        else:
            if not (len(word)==0 and char==" "):
                word+=char
    print("List")
    print(List)
    return List

##############################################################

                        #REST API

##############################################################

class destinationAPI(Resource):
    def get(self,title):
        destination = Destination.query.filter_by(title=title).first()

        if destination:
            return destination.json()
        else:
            return {'note':"Destination not found"},404

    def post(self,title):
        title = request.json['title']
        destination = Destination.query.filter_by(title=title).first()
        error = []

        if destination:
            return {'note':"Destination Exists"}
        else:
            #Basic Attributes
            location = request.json['location']
            country = request.json['country']
            imagefilename = request.json['imagefilename']
            category = request.json['category']

            newDestination = Destination(title,location,country,category,imagefilename)

            db.session.add(newDestination)
            db.session.commit()

            #Characteristcs
            newDestination.cost = request.json['cost']
            newDestination.accessibility = request.json['accessibility']

            for destinationType in String_to_List(request.json['types']):
                type = Type.query.filter_by(title=destinationType).first()
                if type:
                    type.destinations.append(newDestination)
                else:
                    error.append(destinationType)
                db.session.commit()

            for destinationTime in String_to_List(request.json['times']):
                time = Time.query.filter_by(title=destinationTime).first()
                if time:
                    time.destinations.append(newDestination)
                else:
                    error.append(destinationTime)
                db.session.commit()

            for destinationAge in String_to_List(request.json['ages']):
                age = Age.query.filter_by(title=destinationAge).first()
                if age:
                    age.destinations.append(newDestination)
                else:
                    error.append(destinationAge)
                db.session.commit()

            if error:
                error_message = "These features do not exist:"+str(error)
                return {'Error':error_message}
            else:
                return newDestination.json()

    def put(self,title):
        destination = Destination.query.filter_by(title=title).first()
        error=[]

        if destination:
            #Basic Attributes
            destination.title = request.json['title']
            destination.location =  request.json['location']
            destination.cost = request.json['cost']
            destination.imagefilename = request.json['imagefilename']
            destination.category = request.json['category']

            #Characteristcs
            destination.cost = request.json['cost']
            destination.accessibility = request.json['accessibility']

            db.session.commit()

            destination.types.clear()
            destination.times.clear()
            destination.ages.clear()
            db.session.commit()

            for destinationType in String_to_List(request.json['types']):
                type = Type.query.filter_by(title=destinationType).first()
                if type:
                    type.destinations.append(destination)
                else:
                    error.append(destinationType)
                db.session.commit()

            for destinationTime in String_to_List(request.json['times']):
                time = Time.query.filter_by(title=destinationTime).first()
                if time:
                    time.destinations.append(destination)
                else:
                    error.append(destinationTime)
                db.session.commit()

            for destinationAge in String_to_List(request.json['ages']):
                age = Age.query.filter_by(title=destinationAge).first()
                if age:
                    age.destinations.append(destination)
                else:
                    error.append(destinationAge)
                db.session.commit()

            if error:
                error_message = "These features do not exist:"+str(error)
                return {'Error':error_message}
            else:
                return newDestination.json()

        else:
            return {'note':"Destination not found"},404

    def delete(self,title):
        destination = Destination.query.filter_by(title=title).first()

        if destination:
            destination.types.clear()
            destination.times.clear()
            destination.ages.clear()
            db.session.delete(destination)
            db.session.commit()

            return {'note':'delete successful'}
        else:
            return {'note':"Destination not found"},404

class allDestinationAPI(Resource):
    def get(self):
        destinationList = Destination.query.all()

        if destinationList:
            return [destination.json() for destination in destinationList]
        else:
            return {'note':"Location not found"},404

class featureAPI(Resource):
    featureMap = {"type":Type, "time":Time, "age":Age}
    def get(self,category,featureTitle):
        feature = self.featureMap[category].query.filter_by(title=featureTitle).first()
        if feature:
            return feature.json()
        else:
            return {'note':"Feature not found"},404

    def post(self,category,featureTitle):
        feature = self.featureMap[category].query.filter_by(title=featureTitle).first()
        if feature:
            return {'note':"Destination Exists"}
        else:
            newFeature = self.featureMap[category](featureTitle)
            db.session.add(newFeature)
            db.session.commit()
            featureList = self.featureMap[category].query.all()
            return [feature.json() for feature in featureList]

    def put(self,category,featureTitle):
        feature = self.featureMap[category].query.filter_by(title=featureTitle).first()
        if feature:
            feature.title = request.json['title']
            db.session.commit()
            featureList = self.featureMap[category].query.all()
            return [feature.json() for feature in featureList]
        else:
            return {'note':"Feature not found"},404

    def delete(self,category,featureTitle):
        feature = self.featureMap[category].query.filter_by(title=featureTitle).first()
        if feature:
            db.session.delete(feature)
            db.session.commit()
            featureList = self.featureMap[category].query.all()
            return [feature.json() for feature in featureList]
        else:
            return {'note':"Feature not found"},404

class allFeatureAPI(Resource):
    featureMap = {"type":Type, "time":Time, "age":Age}
    def get(self,category):
        featureList = self.featureMap[category].query.all()
        if featureList:
            return [feature.json() for feature in featureList]
        else:
            return {'note':"Feature not found"},404

    def post(self,category):
        #Input Json Example - {"titles": "feature1,feature2,feature3"}
        for featureTitle in String_to_List(request.json['titles']):
            feature = self.featureMap[category].query.filter_by(title=featureTitle).first()
            if feature:
                print("Feature Already Exist")
            else:
                newFeature = self.featureMap[category](featureTitle)
                db.session.add(newFeature)
                db.session.commit()

        featureList = self.featureMap[category].query.all()
        return [feature.json() for feature in featureList]

class demoAPI(Resource):
    def get(self,demoID):
        demo = Demo.query.filter_by(id=demoID).first()
        if demo:
            return demo.json()
        else:
            return {'note':"Destination not found"},404

    def delete(self,title):
        demo = Demo.query.filter_by(id=demoID).first()
        if demo:
            db.session.delete(demo)
            db.session.commit()
            return {'note':'delete successful'}
        else:
            return {'note':"Destination not found"},404

class allDemoAPI(Resource):
    def get(self,demoID):
        demoList = Demo.query.all()
        if demo:
            return [demo.json() for demo in demoList]
        else:
            return {'note':"Destination not found"},404
