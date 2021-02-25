import os, sys, logging

from flask import Flask, request

from service.input_csv_service import InputCsvService

app = Flask(__name__)

@app.route('/input', methods=["POST"])
def parse_input_csv():

    status_code = 200
    status_message = 'success'
    
    input_file = request

    if not input_file:
        status_code = flask.Response(status=503)
        status_message = 'Failure: No input file found'
        return f'status: {status_message}', status_code

    input_csv_service = InputCsvService()
    status_code = 200 if input_csv_service.parse_input_csv(input_file) else 503

    return f'status: {status_message}', status_code

if __name__ == '__main__':

    logging.basicConfig(filename='/tmp/api_debug.log', level=logging.DEBUG)

    app.run(host='0.0.0.0', port=os.getenv('PORT'))
