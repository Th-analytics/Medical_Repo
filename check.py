from flask import Flask, request, jsonify, render_template
from sqlLite import GetData
import json

app = Flask(__name__)


def getValues(cur_obj):
    data_list = ['Select']
    for i in cur_obj.fetchall():
        data_list.append(i[0])
    return data_list


def getPrice(dataDict):
    dtn = dataDict.get('dtn')
    state = dataDict.get('state')
    district = dataDict.get('district')
    pincode = dataDict.get('pincode')
    region = dataDict.get('region')
    area = dataDict.get('area')
    lab = dataDict.get('lab')
    obj = GetData()
    obj.createConnection()
    if state == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' ")
        data = [row[0] for row in curObj.fetchall()]
    elif district == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'")
        data = [row[0] for row in curObj.fetchall()]
    elif pincode == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f" and District = '{district}'")
        data = [row[0] for row in curObj.fetchall()]
    elif region == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f" and District = '{district}' and Pincode = '{pincode}'")
        data = [row[0] for row in curObj.fetchall()]
    elif area == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f" and District = '{district}' and Pincode = '{pincode}' and Region = '{region}' ")
        data = [row[0] for row in curObj.fetchall()]
    elif lab == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f" and District = '{district}' and Pincode = '{pincode}' and Region = '{region}' "
                                 f"and Area = '{area}'")
        data = [row[0] for row in curObj.fetchall()]
    else:
        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f"and District = '{district}' and Pincode = '{pincode}' and Region = '{region}'"
                                 f"and Area = '{area}' and Lab_Name = '{lab}'")
        data = [row[0] for row in curObj.fetchall()]

    obj.con.close()
    return data

@app.route('/')
def index():

    return render_template('index.html', data='')


@app.route('/get_options', methods=['GET'])
def get_options():
    obj = GetData()
    obj.createConnection()
    dtn = obj.cur.execute("SELECT DISTINCT `Diagnostic Test Name` FROM dtest")
    data = getValues(dtn)
    obj.con.close()
    return jsonify(data)


@app.route('/get_data', methods=['POST'])
def get_data():
    option = request.json['dt']
    obj = GetData()
    obj.createConnection()
    data = obj.cur.execute(f"SELECT DISTINCT State FROM dtest where `Diagnostic Test Name`='{option}'")
    data = getValues(data)

    # Query your database using the selected option and retrieve the data
    # In this example, we just return a hardcoded list of data
    obj.con.close()
    return jsonify(data)


@app.route('/get_district', methods=['POST'])
def get_district():
    dtn = request.json['dtn']
    state = request.json['state']
    obj = GetData()
    obj.createConnection()
    curObj = obj.cur.execute(
        f"SELECT DISTINCT District FROM dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'")
    data = getValues(curObj)
    # Query your database using the selected option and retrieve the data
    obj.con.close()
    return jsonify(data)


@app.route('/get_pincode', methods=['POST'])
def get_pincode():
    dtn = request.json['dtn']
    state = request.json['state']
    district = request.json['district']
    obj = GetData()
    obj.createConnection()
    curObj = obj.cur.execute(f"SELECT DISTINCT Pincode FROM"
                             f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                             f"and District = '{district}'")
    data = getValues(curObj)
    # Query your database using the selected option and retrieve the data
    obj.con.close()
    return jsonify(data)


# Region
@app.route('/get_region', methods=['POST'])
def get_region():
    dtn = request.json['dtn']
    state = request.json['state']
    district = request.json['district']
    pincode = request.json['pincode']
    obj = GetData()
    obj.createConnection()
    curObj = obj.cur.execute(f"SELECT DISTINCT Region FROM"
                             f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                             f"and District = '{district}' and Pincode = '{pincode}'")
    data = getValues(curObj)
    # Query your database using the selected option and retrieve the data
    obj.con.close()
    return jsonify(data)


# get_area
@app.route('/get_area', methods=['POST'])
def get_area():
    dtn = request.json['dtn']
    state = request.json['state']
    district = request.json['district']
    pincode = request.json['pincode']
    region = request.json['region']

    obj = GetData()
    obj.createConnection()
    curObj = obj.cur.execute(f"SELECT DISTINCT Area FROM"
                             f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                             f"and District = '{district}' and Pincode = '{pincode}' and Region = '{region}'")
    data = getValues(curObj)
    # Query your database using the selected option and retrieve the data
    obj.con.close()
    return jsonify(data)


# lab
@app.route('/get_lab', methods=['POST'])
def get_lab():
    dtn = request.json['dtn']
    state = request.json['state']
    district = request.json['district']
    pincode = request.json['pincode']
    region = request.json['region']
    area = request.json['area']

    obj = GetData()
    obj.createConnection()
    print(dtn,state,district,pincode,region,area)
    curObj = obj.cur.execute(f"SELECT DISTINCT Lab_Name FROM"
                             f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                             f"and District = '{district}' and Pincode = '{pincode}' and Region = '{region}'"
                             f"and Area = '{area}'")
    data = getValues(curObj)
    # Query your database using the selected option and retrieve the data
    obj.con.close()
    return jsonify(data)


# Result
@app.route('/get_results', methods=['POST'])
def get_results():
    print("In get Results")
    print(request.get_json())
    data = getPrice(dataDict=request.get_json())
    return jsonify(data)


@app.route('/results')
def results():
    if json.loads(request.args.get('data')) is None:
        data = ''
    else:
        data = json.loads(request.args.get('data'))
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
