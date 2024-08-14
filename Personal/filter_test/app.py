from flask import Flask, request, render_template, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

from requests.auth import HTTPBasicAuth
# PACS server credentials
PACS_URL = 'https://pacs.protosonline.in/dicom-web/studies'
# PACS_URL = 'http://localhost:8042/dicom-web/studies'
PACS_USERNAME = 'admin'
PACS_PASSWORD = 'password'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        search_value = request.form.get('searchValue')

        if search_type == 'name':
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
                'limit': '11',
                '00100010': f'*{search_value}*'  # Filter by patient name
            }
        elif search_type == 'id':
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
                'limit': '11',
                '00100020': f'*{search_value}*'  # Filter by patient ID
            }

        try:
            # Send a request to the PACS server
            response = requests.get(PACS_URL, params=params, auth=HTTPBasicAuth(PACS_USERNAME, PACS_PASSWORD))
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        except requests.RequestException as e:
            return jsonify({'error': f"Error: {e}"}), 500

        # Parse the response data
        data = response.json()
        return jsonify(data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
