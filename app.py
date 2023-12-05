from flask import Flask, request, render_template, jsonify
import BASIC_Functionality_no_gui as b
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show-plot')
def show_plot():
    return render_template('plot.html')

@app.route("/GetData")
def GetData():
    df = pd.read_json("test_output.json")
    temp = df.to_dict('records')
    columnNames = df.columns.values

    df = pd.read_json("simulation_results.json")
    temp2 = df.to_dict('records')
    columnNames2 = df.columns.values

    df = pd.read_json("network_analysis.json")
    temp3 = df.to_dict('records')
    columnNames3 = df.columns.values
    
    return render_template('record.html', records=temp, colnames=columnNames,
                           records2=temp2,colnames2=columnNames2,
                           records3=temp3,colnames3=columnNames3)


@app.route('/run-script', methods=['POST'])
def run_script():
    # Retrieve argument from the request
    data = request.json
    argument = data['argument']
    length = data['argument2']
    num_loc = data['argument3']
    min_immunity = data['argument4']
    max_immunity = data['argument5']
    mortality = data['argument6']

    b.main(argument, length, num_loc,
           min_immunity, max_immunity, mortality)
    
    return jsonify({"message": f"Script executed with argument: {argument}"})

if __name__ == '__main__':
    app.run(debug=True)
