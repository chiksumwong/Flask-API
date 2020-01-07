import flask
from flask import jsonify, request
import numpy as np
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

excel_file = "./Cases.xlsx"
cases = pd.read_excel(excel_file)
cases.columns = ['Id', 'Case', 'Category', 'Condition']
# print(cases.head())

# Get the case list
case_list = []
nrows = cases.shape[0]
for i in range(nrows):
    ser = cases.loc[i, :]
    row_dict = {}
    for idx, val in zip(ser.index, ser.values):
        if type(val) is str:
            row_dict[idx] = val
        elif type(val) is np.int64:
            row_dict[idx] = int(val)
        elif type(val) is np.float64:
            row_dict[idx] = float(val)
    case_list.append(row_dict)

rootUrl = '/qa/api/v1.0'

# Home
@app.route('/', methods=['GET'])
def home():
    return "<h1>QA</h1>"

# Get all
@app.route(rootUrl + '/cases', methods=['GET'])
def get_cases():
    return jsonify({'cases': case_list})

# Get by id
@app.route(rootUrl + '/cases/<string:case_id>', methods=['GET'])
def get_case(case_id):
    case = [case for case in case_list if case['Id'] == case_id]
    if len(case) == 0:
        abort(404)
    return jsonify({'cases': case[0]})

# Get by category
@app.route(rootUrl + '/cases/category/<string:case_category>', methods=['GET'])
def get_case_category(case_category):
    case = [case for case in case_list if case['Category'] == case_category]
    if len(case) == 0:
        abort(404)
    return jsonify({'cases': case})

# Get by condition
@app.route(rootUrl + '/cases/condition/<string:case_condition>', methods=['GET'])
def get_case_condition(case_condition):
    case = [case for case in case_list if case['Condition'] == case_condition]
    if len(case) == 0:
        abort(404)
    return jsonify({'cases': case})

# Create
@app.route(rootUrl + '/cases', methods=['POST'])
def create_case():
    if not request.json or not 'Case' or not 'Category' or not 'Condition' or not 'Id' in request.json:
        abort(400)
    case = {
        'Id': request.json['Id'],
        'Case': request.json['Case'],
        'Category': request.json['Category'],
        'Condition': request.json['Condition'],
    }
    # Action to add to xlsx....
    # May be......
    return jsonify({'cases': case}), 201

app.run()