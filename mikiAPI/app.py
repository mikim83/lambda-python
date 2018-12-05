from chalice import Chalice, Response, BadRequestError, NotFoundError
import json
import boto3
import jsonschema 

app = Chalice(app_name='mikiAPI')
app.debug = True
OBJECTS = {
}

schema = {
    "type" : "object",
    "properties" : {
        "id" : {"type" : "string", "minItems": 1},
        "quantity" : {"type" : "integer", "minItems": 1}

    },
    "required": ["id","quantity"]
}

@app.route('/')
def index():
    message = json.dumps({'Message': 'Hello World'}, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(body=message,
                    status_code=200,
                    headers={'Content-Type': 'application/json'})
@app.route('/error400')
def error400():
    message = json.dumps({'Message': 'ERROR 400'}, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(body=message,
                    status_code=400,
                    headers={'Content-Type': 'application/json'})
@app.route('/error500')
def error500():
    message = json.dumps({'Message': 'ERROR 500'}, sort_keys=True, indent=4, separators=(',', ': '))
    return Response(body=message,
                    status_code=500,
                    headers={'Content-Type': 'application/json'})

@app.route('/counter/id/{id}', methods=['GET', 'POST'])
def counterid(id):
    request = app.current_request
    if request.method == 'POST':
        OBJECTS[id] = request.json_body
        try:
            jsonschema.validate(OBJECTS[id],schema)
        except jsonschema.exceptions.ValidationError as e:
            message = json.dumps({'Message':'ERROR - '+ e.message}, sort_keys=True, indent=4, separators=(',', ': '))
            return Response(body=message,
                    status_code=500,
                    headers={'Content-Type': 'application/json'})
        message = json.dumps(OBJECTS[id], sort_keys=True, indent=4, separators=(',', ': '))
        return Response(body=message,
            status_code=200,
            headers={'Content-Type': 'application/json'})
    elif request.method == 'GET':
        try:
            return {id: OBJECTS[id]}
        except KeyError:
            raise NotFoundError(id)




#    message = json.dumps({'city': id }, sort_keys=True, indent=4, separators=(',', ': '))
#    return Response(body=message,
#                    status_code=200,
#                    headers={'Content-Type': 'application/json'})




# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#


#from chalice import BadRequestError
#@app.route('/cities/{city}')
#def state_of_city(city):
#    try:
#        return {'state': CITIES_TO_STATE[city]}
#    except KeyError:
#        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
#            city, ', '.join(CITIES_TO_STATE.keys())))



# BadRequestError - return a status code of 400
# UnauthorizedError - return a status code of 401
# ForbiddenError - return a status code of 403
# NotFoundError - return a status code of 404
# ConflictError - return a status code of 409
# UnprocessableEntityError - return a status code of 422
# TooManyRequestsError - return a status code of 429
# ChaliceViewError - return a status code of 500






