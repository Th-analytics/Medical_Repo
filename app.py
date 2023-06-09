from flask import Flask, request, jsonify, render_template, render_template_string, send_file, make_response
from sqlLite import GetData
import pandas as pd
import shutil
import os

app = Flask(__name__)


def getValues(cur_obj):
    data_list = []

    for i in cur_obj.fetchall():
        data_list.append(i[0])
    return data_list


def delete_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(os.path.join(root, file))


def getPrice(dataDict):
    col = ['Disease', 'Drug_name', 'Generic_name', 'Brand_names', 'Drug_class', 'Rx_OTC', 'Pregnancy', 'CSA', 'Alcohol']
    diseaseName_ = dataDict.get('diseaseName')
    drugName_ = dataDict.get('drugName')
    print("Name of Disease and Drug: ", diseaseName_, drugName_)
    obj = GetData()
    obj.createConnection()
    df = pd.DataFrame([])
    if diseaseName_ == 'Select':
        query = f"SELECT DISTINCT Disease, Drug_name, Generic_name, Brand_names, Drug_class," \
                f"Rx_OTC, Pregnancy, CSA, Alcohol FROM drugData where Drug_name = '{drugName_}'"
        df = pd.read_sql(query, con=obj.con)
    elif drugName_ == 'Select':

        query = f"SELECT DISTINCT  Drug_name, Disease, Generic_name, Brand_names, Drug_class," \
                f"Rx_OTC, Pregnancy, CSA, Alcohol FROM drugData where Disease = '{diseaseName_}'"
        df = pd.read_sql(query, con=obj.con)

    else:
        pass

    obj.con.close()
    return df


@app.route('/')
def index():
    delete_files_in_directory("dataFile")
    return render_template('index.html', data='')


@app.route('/get_options', methods=['GET'])
def get_options():
    obj = GetData()
    obj.createConnection()
    disease_ = obj.cur.execute("SELECT DISTINCT Disease FROM drugData order by Disease")
    disease = getValues(disease_)
    obj.con.close()

    obj = GetData()
    obj.createConnection()
    drug_ = obj.cur.execute("SELECT DISTINCT Drug_name FROM drugData order by Drug_name")
    drug = getValues(drug_)

    data = {'disease': disease, 'drug': drug}
    obj.con.close()
    return jsonify(data)


# Result
@app.route('/get_results', methods=['POST'])
def get_results():
    print("In get Results")
    print(request.get_json())
    df_ = getPrice(dataDict=request.get_json())
    dataDict = request.get_json()
    diseaseName_ = dataDict.get('diseaseName')
    drugName_ = dataDict.get('drugName')
    if diseaseName_ != "Select":
        fileName = diseaseName_
    elif drugName_ != "Select":
        fileName = drugName_

    df_.to_csv(f"dataFile/{fileName}.csv", index=False)

    html_table = df_.to_html(classes='table table-striped',
                             header=True, index=False,
                             justify='center',
                             table_id='myTable')
    # Add CSS styles to columns
    html_table = html_table.replace('<thead>', '<thead style="background-color:#007bff;color:white">')
    html_table = html_table.replace('<th>', '<th style="text-align:center">')
    html_table = html_table.replace('<tbody>', '<tbody style="background-color:#f5f5f5;">')
    html_table = html_table.replace('<td>', '<td style="text-align:center">')
    return jsonify(html_table=html_table)



@app.route('/data')
def download_data():
    fileName = request.args.get('fileName')
    diseaseName = request.args.get('diseaseName')
    drugName = request.args.get('drugName')
    filePath = os.path.join('dataFile', fileName)
    if os.path.exists(filePath):
        response = make_response(send_file(filePath, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename={fileName}'
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Cache-Control'] = 'no-cache'
        if diseaseName:
            response.set_cookie('diseaseName', diseaseName)
        if drugName:
            response.set_cookie('drugName', drugName)
        return response
    else:
        return jsonify({'status': 'error', 'message': f'{fileName} not found'})
@app.route('/results', methods=['POST'])
def results():
    print("In results:")
    if not request.args.get('data'):
        data = ''
    else:
        data = {'html_table': request.args.get('data')}
    return render_template_string('<div>{{ html_table|safe }}</div>', data=data)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
