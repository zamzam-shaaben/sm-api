from logging import log
from flask import Flask, request, redirect, url_for,make_response, jsonify
from flask_restful import Resource, Api
from flask_expects_json import expects_json
from jsonschema import ValidationError
import smpp_client 
# this particular app calls the server 
app = Flask(__name__)
api = Api(app)

# run the server but before we must check
if __name__ == '__main__':
    # my application will start the web service using this server we can test our methods
    app.run(debug=True)

schema ={
    "type":"array",
    "items":
    {
        "type":"object",
        "properties":{
            "dst_number":{
                "type":"string"
            },
            "content":{
                "type":"string"
            },
            "source_number":{
                "type":"string"
            }
        },
        "required":[
            "dst_number",
            "content",
            "source_number"
        ]
    }
}

@app.route('/messages', methods=['POST'])
@expects_json(schema, ignore_for=['GET'])
def messages():

        args = request.json
        for arg in  args:
            # source
            # dest 
            # content 
            smpp_client.SendSms(arg['source_number'],arg['dst_number'],arg['content'])
            
        return args

@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': original_error.message}), 400)
    # handle other 'Bad Request'-errors
    return error 


