from flask import Flask, request, render_template, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# PACS server credentials
PACS_URL = 'https://pacs.protosonline.in/dicom-web/studies'
PACS_USERNAME = 'admin'
PACS_PASSWORD = 'password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')

        # Build the query parameters
        params = {
            'includefield': [
                '00100010',  # Patient Name
                '00101010',  # Patient Age
                '00100040',  # Patient Sex
                '00200010',  # Study ID
                '00080020',  # Study Date
                '0020000E',  # Series Instance UID
                '0008103E',  # Series Description
                '00201206',  # Number of Series
                '00201208',  # Number of SOP Instances
            ],
            'orderby': '00080020',
            'limit': '11',
            '00100010': f'*{patient_name}*'  # Filter by patient name
        }

        # Send a request to the PACS server
        response = requests.get(PACS_URL, params=params, auth=HTTPBasicAuth(PACS_USERNAME, PACS_PASSWORD))

        if response.status_code == 200:
            # Parse the response data
            data = response.json()  # Assuming the PACS returns JSON data
            return jsonify(data)
        else:
            return jsonify({'error': f"Error: {response.status_code} - {response.text}"}), response.status_code

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
