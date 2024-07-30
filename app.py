from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)

# Configure session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'supersecretkey'
Session(app)

result_table = {}
inputs = {}
preset_num = None
bonus_rates = {}
tabletype = '1'  # Initialize with a default value
winning_values = {}
winning_outcome = '1'
oflubet_values = []
sexbet_values = []
maskulenbet_values = []

# Default entries
default_entries = [
    [{'bet_site': 0, 'betted_by': 'Mert', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 1, 'betted_by': 'Mert', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 2, 'betted_by': 'Mert', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''}],
    [{'bet_site': 0, 'betted_by': 'Keleş', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 1, 'betted_by': 'Keleş', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 2, 'betted_by': 'Keleş', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''}],
    [{'bet_site': 0, 'betted_by': 'Semih', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 1, 'betted_by': 'Semih', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''},
     {'bet_site': 2, 'betted_by': 'Semih', 'yatirilacak_tutar': 0.0, 'betted_outcome': ''}]
]

def update_entries(preset_num, entries):

    if preset_num == 1:
        entries[0][0]['betted_outcome'] = 1
        entries[0][1]['betted_outcome'] = 0
        entries[0][2]['betted_outcome'] = 2
        entries[1][0]['betted_outcome'] = 2
        entries[1][1]['betted_outcome'] = 1
        entries[1][2]['betted_outcome'] = 0
        entries[2][0]['betted_outcome'] = 0
        entries[2][1]['betted_outcome'] = 2
        entries[2][2]['betted_outcome'] = 1
    elif preset_num == 2:
        entries[0][0]['betted_outcome'] = 2
        entries[0][1]['betted_outcome'] = 0
        entries[0][2]['betted_outcome'] = 1
        entries[1][0]['betted_outcome'] = 1
        entries[1][1]['betted_outcome'] = 2
        entries[1][2]['betted_outcome'] = 0
        entries[2][0]['betted_outcome'] = 0
        entries[2][1]['betted_outcome'] = 1
        entries[2][2]['betted_outcome'] = 2
    elif preset_num == 3:
        entries[0][0]['betted_outcome'] = 0
        entries[0][1]['betted_outcome'] = 1
        entries[0][2]['betted_outcome'] = 2
        entries[1][0]['betted_outcome'] = 1
        entries[1][1]['betted_outcome'] = 2
        entries[1][2]['betted_outcome'] = 0
        entries[2][0]['betted_outcome'] = 2
        entries[2][1]['betted_outcome'] = 0
        entries[2][2]['betted_outcome'] = 1

    for row in range(3):
        for col in range(3):
            if entries[row][col]['bet_site'] == col:
                if entries[row][col]['betted_by'] == 'Mert':
                    entries[row][col]['yatirilacak_tutar'] = entries[row][col]['yatirilacak_tutar'] * 4000
                elif entries[row][col]['betted_by'] == 'Keleş':
                    entries[row][col]['yatirilacak_tutar'] = entries[row][col]['yatirilacak_tutar'] * 3950
                elif entries[row][col]['betted_by'] == 'Semih':
                    entries[row][col]['yatirilacak_tutar'] = entries[row][col]['yatirilacak_tutar'] * 3900

@app.route("/", methods=["GET", "POST"])
def index():
    global result_table
    global inputs
    global preset_num
    global bonus_rates
    global tabletype
    global winning_values
    global winning_outcome
    global oflubet_values
    global sexbet_values
    global maskulenbet_values

    # Retrieve entries from session or use default if not present
    entries = session.get('entries', default_entries)

    if request.method == "POST":
        # Retrieve preset_num from form
        preset_num = int(request.form.get('preset_num', 0))

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

        # Retrieve winning outcome from form
        winning_outcome = request.form.get('winning_outcome', '')

        # Prepare the result table with the calculation 100 / input value
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

        # Update entries based on the preset number
        update_entries(preset_num, entries)

        # Store updated entries in the session
        session['entries'] = entries
        session.modified = True  # Force session to be updated

    # Render the template with current values (no default fallback)
    return render_template('home.html', tabletype=tabletype, result_table=result_table,
           preset_num=preset_num, bonus_rates=bonus_rates, inputs=inputs, 
           winning_values=winning_values, entries=entries)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
