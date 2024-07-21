from flask import Flask, render_template, request

app = Flask(__name__)
result_table = []
inputs = {}
preset_num = None
bonus_rates = {}
tabletype = '1'  # Initialize with a default value

@app.route("/", methods=["GET", "POST"])
def index():
    global result_table
    global inputs
    global preset_num
    global bonus_rates
    global tabletype

    if request.method == "POST":


        # Retrieve bonus rates from form
        oflu_bonus_orani = float(request.form.get('oflubonus', 0))
        sexbet_bonus_orani = float(request.form.get('sexbonus', 0))
        maskülenbet_bonus_orani = float(request.form.get('chadbonus', 0))

        inputs = {}
        # List of input names
        input_names = [
            'oflu0', 'oflu1', 'oflu2', 'sex0', 'sex1', 'sex2', 'chad0',
            'chad1', 'chad2'
        ]
        for name in input_names:
            input_value = request.form.get(name)
            if input_value:
                inputs[name] = float(input_value)

        # Retrieve table type from form
        tabletype = request.form.get('table_type', '1')  # Default to table 1 if no type is provided

        # Prepare the result table with the calculation
        result_table = [
            [round((100) / (inputs.get('oflu0', 1) * (100 + oflu_bonus_orani)), 4),
             round((100) / (inputs.get('sex0', 1) * (100 + sexbet_bonus_orani)), 4),
             round((100) / (inputs.get('chad0', 1) * (100 + maskülenbet_bonus_orani)), 4)],
            [round((100) / (inputs.get('oflu1', 1) * (100 + oflu_bonus_orani)), 4),
             round((100) / (inputs.get('sex1', 1) * (100 + sexbet_bonus_orani)), 4),
             round((100) / (inputs.get('chad1', 1) * (100 + maskülenbet_bonus_orani)), 4)],
            [round((100) / (inputs.get('oflu2', 1) * (100 + oflu_bonus_orani)), 4),
             round((100) / (inputs.get('sex2', 1) * (100 + sexbet_bonus_orani)), 4),
             round((100) / (inputs.get('chad2', 1) * (100 + maskülenbet_bonus_orani)), 4)]
        ]

    # Always render the template with default values if necessary
    return render_template('home.html', tabletype=tabletype, result_table=result_table,
                           preset_num=preset_num, bonus_rates=bonus_rates, inputs=inputs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
