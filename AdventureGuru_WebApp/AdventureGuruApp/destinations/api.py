from flask import request
from flask_restful import Resource
from AdventureGuruApp import db
from AdventureGuruApp.models import Destination

class destinationAPI(Resource):
    def get(self,title):
        destination = Destination.query.filter_by(title=title).first()

        if destination:
            return destination.json()
        else:
            return {'note':"Destination not found"},404

    def post(self,title):
        destination = Destination.query.filter_by(title=title).first()

        if destination:
            return {'note':"Destination Exists"}
        else:
            title = request.json['title']
            location =  request.json['location']
            type =  request.json['type']
            cost = request.json['cost']
            imageFilename = request.json['imageFilename']

            newDestination = Destination(title,location,type,cost,imageFilename)

            db.session.add(newDestination)
            db.session.commit()

            return newDestination.json()

    def put(self,title):
        destination = Destination.query.filter_by(title=title).first()

        if destination:
            destination.title = request.json['title']
            destination.location =  request.json['location']
            destination.type =  request.json['type']
            destination.cost = request.json['cost']
            destination.imageFilename = request.json['imageFilename']

            db.session.commit()

            return destination.json()
        else:
            return {'note':"Destination not found"},404

    def delete(self,title):
        destination = Destination.query.filter_by(title=title).first()

        if destination:
            db.session.delete(destination)
            db.session.commit()

            return {'note':'delete successful'}
        else:
            return {'note':"Destination not found"},404


class allDestinationAPI(Resource):
    def get(self,location):
        Location = Destination.query.filter_by(location=location)

        if Location:
            return [destination.json() for destination in Location]
        else:
            return {'note':"Location not found"},404
