from  nlpProcessing import NlpProcessing
from flask import Flask
from flask import request
import json
from flask_cors import CORS

nlpProcessing = NlpProcessing('example.feature')
app = Flask(__name__)
CORS(app)
    
    
    
@app.route('/')
def hello_world():
    return str(nlpProcessing.find_steps_in_doc_from_keywords(['found', 'world']))


@app.route('/find_keywords', methods=['GET'])
def find_keywords():
    keywords = request.args.get('keywords', '').split('$')
    print(keywords)
    results =  nlpProcessing.find_steps_in_doc_from_keywords(keywords)
    return json.dumps(results)