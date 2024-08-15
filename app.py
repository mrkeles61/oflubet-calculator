from flask import Flask, render_template, request
from otuzbirmanyagi import entries

app = Flask(__name__)

inputs = {}
preset_num = None
bonus_rates = {}
match_name='AYIBOĞAN'
winning_outcome= None
oflubet_values = []
sexbet_values = []
maskulenbet_values = []

# Define inputs_2d globally
inputs_2d = []
  # Initialize entries globally


def update_entries_with_inputs(entries, inputs_2d, bonus_rates):
    site_names = ["oflu", "sex", "chad"]

    for row in entries:
        for entry in row:
            site_index = entry['bet_site']

            # Get the correct input value from the 2D array based on site_index and betted_outcome
            input_value = inputs_2d[site_index][entry["betted_outcome"]]
            entry['bet_Rate'] = input_value

            # Get the bonus rate using the site name
            site_name = site_names[site_index]
            entry['bonus_orani'] = bonus_rates.get(site_name, 0)


def calculate_second_day(entries, winning_outcome):
    for row in entries:
        for entry in row:
            if entry['betted_outcome'] == (winning_outcome):
                yatirilacak_tutar = entry['yatirilacak_tutar']
                bet_rate = entry['bet_Rate']
                cap_num = entry['cap_number']
                bonus_orani = entry['bonus_orani']

                entry['second_day_YT'] = round((((yatirilacak_tutar * bonus_orani) / 10) - (cap_num / bet_rate) + 15),2)
                                         


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


    oflu_bonus = float(request.form.get('oflubonus', 0))
    sex_bonus = float(request.form.get('sexbonus', 0))
    chad_bonus = float(request.form.get('chadbonus', 0))

    for row in range(3):
        for col in range(3):
            bet_site = int(entries[row][col]['bet_site'])
            betted_outcome = int(entries[row][col]['betted_outcome'])
            bet_rate = float(entries[row][col]['bet_Rate'])
            bonus_orani = 0
            cap_num = entries[row][col]['cap_number']

            # Assign bonus rate based on bet_site
            if bet_site == 0:
                bonus_orani = oflu_bonus
            elif bet_site == 1:
                bonus_orani = sex_bonus
            elif bet_site == 2:
                bonus_orani = chad_bonus

            yatirilacak_tutar = (cap_num * 100) / (bet_rate * (100 + bonus_orani))
            entries[row][col]['yatirilacak_tutar']=round(yatirilacak_tutar,2)


@app.route("/", methods=["GET", "POST"])
def index():
    global inputs
    global preset_num
    global bonus_rates
    global winning_outcome
    global inputs_2d
    global entries
    global match_name

    inputs = {
        'oflu1': request.form.get('oflu1', ''),
        'oflu0': request.form.get('oflu0', ''),
        'oflu2': request.form.get('oflu2', ''),
        'sex1': request.form.get('sex1', ''),
        'sex0': request.form.get('sex0', ''),
        'sex2': request.form.get('sex2', ''),
        'chad1': request.form.get('chad1', ''),
        'chad0': request.form.get('chad0', ''),
        'chad2': request.form.get('chad2', ''),
    }
    bonus_rates = {
        'oflu': request.form.get('oflubonus', ''),
        'sex': request.form.get('sexbonus', ''),
        'chad': request.form.get('chadbonus', '')
    }

    if request.method == "POST":
        # Debug print to see received form data
        print("Form Data:", request.form)

        # Retrieve preset_num from form
        preset_num = int(request.form.get('table_type', 0))

        # Retrieve bonus rates from form
        bonus_rates = {
            'oflu': float(request.form.get('oflubonus', 0)),
            'sex': float(request.form.get('sexbonus', 0)),
            'chad': float(request.form.get('chadbonus', 0))
        }

        # Initialize inputs_2d
        inputs_2d = [
            [
                float(request.form.get('oflu0', 0)),
                float(request.form.get('oflu1', 0)),
                float(request.form.get('oflu2', 0))
            ],
            [
                float(request.form.get('sex0', 0)),
                float(request.form.get('sex1', 0)),
                float(request.form.get('sex2', 0))
            ],
            [
                float(request.form.get('chad0', 0)),
                float(request.form.get('chad1', 0)),
                float(request.form.get('chad2', 0))
            ]
        ]

        # Update entries with bet rates and bonus rates
        update_entries_with_inputs(entries, inputs_2d, bonus_rates)

        # Retrieve winning outcome from form and debug print
        winning_outcome_str = request.form.get('winning_outcome', '0')
        print("Winning Outcome String:", winning_outcome_str)

        try:
            winning_outcome = int(winning_outcome_str)
        except ValueError:
            winning_outcome = 0  # Default value if conversion fails


        # Update entries based on the preset number
        update_entries(preset_num, entries)
        calculate_second_day(entries, winning_outcome)
        match_name=request.form.get('match_name', 'default')

        print("Match Name:", match_name)  # Debug print to check value

    # Render the template with current values (no default fallback)
    return render_template('home.html',
                           preset_num=preset_num,
                           bonus_rates=bonus_rates,
                           inputs=inputs,
                           entries=entries,
                           winning_outcome=winning_outcome,
                           match_name=match_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
