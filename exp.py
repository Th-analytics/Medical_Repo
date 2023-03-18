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
                                 f"District = '{district}'")
        data = [row[0] for row in curObj.fetchall()]
    elif region == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f"District = '{district}' and Pincode = '{pincode}'")
        data = [row[0] for row in curObj.fetchall()]
    elif area == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f"District = '{district}' and Pincode = '{pincode}' and Region = '{region}' ")
        data = [row[0] for row in curObj.fetchall()]
    elif lab == 'Select':

        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f"District = '{district}' and Pincode = '{pincode}' and Region = '{region}' "
                                 f"and Area = '{area}'")
        data = [row[0] for row in curObj.fetchall()]
    else:
        curObj = obj.cur.execute(f"SELECT avg(`View Price`) FROM"
                                 f" dtest where `Diagnostic Test Name`='{dtn}' and State='{state}'"
                                 f"and District = '{district}' and Pincode = '{pincode}' and Region = '{region}'"
                                 f"and Area = '{area}' and Lab_Name = '{lab}'")
        data = [row[0] for row in curObj.fetchall()]


    return data