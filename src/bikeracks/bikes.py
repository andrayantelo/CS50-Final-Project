# A view
# Blueprints are a way to organize your project
# Example blueprints:
#    users blueprint (responsible for logging in/out, password
#        resets, email confirmations)
#    bikes (todo change name?) (responsible for adding/deleting
#        bike racks

# Rather than registering views and other code directly with an app
# they are registered with a blueprint. Then the bp is registered with
# the app when it is available in the factory function.

from flask import (
    Blueprint, render_template, request, session, jsonify, Response
)

from . import helpers as helper

from bikeracks.db import get_db
# __name__ is passed as 2nd arg so that bp knows where it is defined
# __name__ evaluates to to the name of the current module
bikes = Blueprint('bikes', __name__)

# View functions can be can be mapped to one or more routes
# might want to add the '/' route here TODO
@bikes.route('/dynamic/<path:path>')
def render_file(path):
    # the view function for the route to scripts inside of dynamic directory
    response = render_template(path), 200, {'Content-Type': 'text/javascript'}
    
    return response


@bikes.route('/coordinates', methods=('POST',))
def coordinates():
    # get the coordinates from the request
    lat = request.form.get('lat', 0, type=float)
    lng = request.form.get('lng', 0, type=float)
    address = request.form.get('address', '')
    
    if not helper.validate_coordinates((lat, lng)):
        return "Invalid Coordinates", 500

    # if valid, save in database

    # connect to database to be able to store new coordinates for temporary bikerack
    db = get_db()
    db.execute('INSERT INTO bikeracks (latitude, longitude, address) VALUES (?, ?, ?);', (lat, lng, address))
    db.commit()
    # return data for the added temporary marker
    bike_rack = helper.get_rack_state(db, lat, lng)

    return bike_rack
  

# get racks based on status ('not_approved', 'approved')
@bikes.route('/get_racks/', methods=['GET'])
def get_racks():

    status = request.args.get('status', "", type=str)
    user_id = request.args.get('userId', "", type=str)

    # make a connection to the database
    db = get_db()

    racks = helper.get_racks(db, status, user_id)

    return racks

 
@bikes.route('/store_rack/', methods=['POST'])
def store_rack():
    # manually insert racks into db   

    args = request.json
    db = get_db()
    
    helper.insert_rack(db, args)
    return Response(status=200)

 
@bikes.route('/get_single_rack', methods=['GET'])
def get_single_rack():
    # get rack based on rack_id 
   
    rack_id = request.args.get('rack_id', None, type=int)
    
    # database connection
    db = get_db()
    
    rack = helper.get_single_rack(db, rack_id)
    
    return rack

# this is a test
@bikes.route('/update_rack_status', methods=['GET'])
def update_rack_status():
    # update a rack's status (approved, not_approved) based on the upvote_count
    # and downvote_count percentages
   
    rack_id = request.args.get('rack_id', None, type=int)
    
    db = get_db()
    percentages = helper.get_count_percentage(rack_id, db)
    upvote_ratio = percentages['upvote_percentage']
    downvote_ratio = percentages['downvote_percentage']
    
    current_rack_status = db.execute("SELECT status FROM bikeracks WHERE rack_id=?", (rack_id,)).fetchone()
    current_rack_status = helper.dict_from_row(current_rack_status)
    current_rack_status = current_rack_status['status']

    
    # if the rack has more than 50 % downvotes, and the rack's status is approved,
    # we change the status to not approved
    if downvote_ratio > 50 and current_rack_status == 'approved':
        # change status to not approved
        
        db.execute("UPDATE bikeracks SET status = 'not_approved' WHERE rack_id=?", (rack_id,))
        db.commit()
    # if the rack has more than or equal to 50 % upvotes, and the rack status is currently not approved
    # we change the status to approved
    elif upvote_ratio >= 50 and current_rack_status == 'not_approved':
        
        # change status to approved
        db.execute("UPDATE bikeracks SET status = 'approved' WHERE rack_id=?", (rack_id,))
        db.commit()
    after_rack_status = db.execute("SELECT status FROM bikeracks WHERE rack_id=?", (rack_id,)).fetchone()
    after_rack_status = helper.dict_from_row(after_rack_status)
    after_rack_status = after_rack_status['status']
    
    result = {'before': current_rack_status, 'after': after_rack_status}
    return jsonify(result)
    
