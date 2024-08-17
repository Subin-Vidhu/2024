# app.py
from flask import Flask, request, render_template, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# PACS server credentials
PACS_URL = 'https://pacs.protosonline.in/dicom-web/studies'
# PACS_URL = 'http://localhost:8042/dicom-web/studies'
PACS_USERNAME = 'admin'
PACS_PASSWORD = 'password'

# Mapping of search options to DICOM tags
SEARCH_OPTIONS = {
    'name': '00100010',  # Patient Name
    'id': '00100020',  # Patient ID
    'birthdate': '00100030',  # Patient Birth Date
    'sex': '00100040',  # Patient Sex
    'study_date': '00080020',  # Study Date
    'study_time': '00080030',  # Study Time
    'study_id': '00200010',  # Study ID
    'study_description': '00081030',  # Study Description
    'accession_number': '00080050',  # Accession Number
    'referring_physician': '00080090',  # Referring Physician's Name
    'performing_physician': '00081050',  # Performing Physician's Name
    'institution_name': '00080080',  # Institution Name
    'department_name': '00081040',  # Department Name
    'modality': '00080060',  # Modality
    'series_description': '0008103E',  # Series Description
    'series_instance_uid': '0020000E',  # Series Instance UID
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        search_value = request.form.get('searchValue')

        if search_type in SEARCH_OPTIONS:
            params = {
                'includefield': [
                    '00100010',  # Patient Name
                    '00101010',  # Patient Age
                    '00100040',  # Patient Sex
                    '00200010',  # Study ID
                    '00080020',  # Study Date
                    '00080030',  # Study Time
                    '0020000E',  # Series Instance UID
                    '0008103E',  # Series Description
                    '00201206',  # Number of Series
                    '00201208',  # Number of SOP Instances
                    '00100030',  # Patient Birth Date
                    '00080060',  # Modality
                    '00080050',  # Accession Number
                    '00080090',  # Referring Physician's Name
                    '00081050',  # Performing Physician's Name
                    '00080080',  # Institution Name
                    '00081040',  # Department Name
                ],
                'limit': '50',
            }

            if search_type == 'birthdate':
                params[SEARCH_OPTIONS[search_type]] = search_value
            elif search_type == 'study_date':
                params[SEARCH_OPTIONS[search_type]] = search_value
            elif search_type == 'study_time':
                params[SEARCH_OPTIONS[search_type]] = search_value
            elif search_type == 'series_instance_uid':
                params[SEARCH_OPTIONS[search_type]] = search_value
            else:
                params[SEARCH_OPTIONS[search_type]] = f'*{search_value}*'

        else:
            return jsonify({'error': 'Invalid search type'}), 400

        try:
            # Send a request to the PACS server
            response = requests.get(PACS_URL, params=params, auth=HTTPBasicAuth(PACS_USERNAME, PACS_PASSWORD))
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        except requests.RequestException as e:
            return jsonify({'error': f"Error: {e}"}), 500

        # Parse the response data
        data = response.json()
        output = []
        for study in data:
            patient_info = {
                'patient_name': study.get('00100010', {}).get('Value', [])[0] if study.get('00100010', {}).get('Value', []) else 'N/A',
                'patient_id': study.get('00100020', {}).get('Value', [])[0] if study.get('00100020', {}).get('Value', []) else 'N/A',
                'patient_birth_date': study.get('00100030', {}).get('Value', [])[0] if study.get('00100030', {}).get('Value', []) else 'N/A',
                'patient_sex': study.get('00100040', {}).get('Value', [])[0] if study.get('00100040', {}).get('Value', []) else 'N/A',
                'study_id': study.get('00200010', {}).get('Value', [])[0] if study.get('00200010', {}).get('Value', []) else 'N/A',
                'study_date': study.get('00080020', {}).get('Value', [])[0] if study.get('00080020', {}).get('Value', []) else 'N/A',
                'study_time': study.get('00080030', {}).get('Value', [])[0] if study.get('00080030', {}).get('Value', []) else 'N/A',
                'study_description': study.get('00081030', {}).get('Value', [])[0] if study.get('00081030', {}).get('Value', []) else 'N/A',
                'accession_number': study.get('00080050', {}).get('Value', [])[0] if study.get('00080050', {}).get('Value', []) else 'N/A',
                'referring_physician': study.get('00080090', {}).get('Value', [])[0] if study.get('00080090', {}).get('Value', []) else 'N/A',
                'performing_physician': study.get('00081050', {}).get('Value', [])[0] if study.get('00081050', {}).get('Value', []) else 'N/A',
                'institution_name': study.get('00080080', {}).get('Value', [])[0] if study.get('00080080', {}).get('Value', []) else 'N/A',
                'department_name': study.get('00081040', {}).get('Value', [])[0] if study.get('00081040', {}).get('Value', []) else 'N/A',
                'modality': study.get('00080060', {}).get('Value', [])[0] if study.get('00080060', {}).get('Value', []) else 'N/A',
                'series_instance_uid': study.get('0020000E', {}).get('Value', [])[0] if study.get('0020000E', {}).get('Value', []) else 'N/A',
                'series_description': study.get('0008103E', {}).get('Value', [])[0] if study.get('0008103E', {}).get('Value', []) else 'N/A',
                'number_of_series': study.get('00201206', {}).get('Value', [])[0] if study.get('00201206', {}).get('Value', []) else 'N/A',
                'number_of_sop_instances': study.get('00201208', {}).get('Value', [])[0] if study.get('00201208', {}).get('Value', []) else 'N/A',
            }
            output.append(patient_info)
        return jsonify(output)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)