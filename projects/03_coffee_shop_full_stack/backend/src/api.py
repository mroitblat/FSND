import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
Uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def drinks():
    try:
        return jsonify({
            'success': True,
            'drinks': [drink.short() for drink in Drink.query.all()]
        }), 200
    except:
        abort(500)


'''
POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(f):
    body = request.get_json()
    if not body:
        abort(400)

    title = body.get('title', None)
    if type(body.get('recipe')) == str:
        recipe = body.get('recipe', None)
    else:
        recipe = json.dumps(body.get('recipe'))

    if not title or not recipe:
        abort(400)

    try:
        drink = Drink(title, recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200
    except:
        abort(500)

'''
PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(f, drink_id):
    body = request.get_json()
    if not body:
        abort(400)

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink:
            drink.title = body.get('title') if body.get('title') else drink.title
            recipe = body.get('recipe') if body.get('recipe') else drink.recipe
            drink.recipe = recipe if type(recipe) == str else json.dumps(recipe)

            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            }), 200
        else:
            abort(404)
    except:
        abort(500)

'''
DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(f, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': drink.id
            }), 200
        else:
            abort(404)
    except:
        abort(500)


'''
GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(f):
    try:
        return jsonify({
            'success': True,
            'drinks': [drink.long() for drink in Drink.query.all()]
        }), 200
    except:
        abort(500)

## Error Handling
'''
Example error handling for unprocessable entity
'''
'''
Implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Unauthorized"
        }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False, 
        "error": 403,
        "message": "Forbidden"
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource not found"
        }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500

'''
Implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error['code']
        }), 401
