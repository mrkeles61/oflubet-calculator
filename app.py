from flask import Flask, render_template, request
from otuzbirmanyagi import entries

app = Flask(__name__)

inputs={}
preset_num = None
bonus_rates = {}
match_name='AYIBOĞAN'
winning_outcome= None
second_winning_outcome=0

  

def calculate_second_day(entries, winning_outcome,second_winning_outcome):
    for row in range(3):
        for col in range(3):
            entry = entries[row][col]
            if entry['betted_outcome'] == winning_outcome:
                yatirilacak_tutar = entry['yatirilacak_tutar']
                bet_rate = entry['bet_Rate']
                cap_num = entry['cap_number']
                bonus_orani = entry['bonus_orani']
                

                entry['second_day_YT'] = round((((yatirilacak_tutar * bonus_orani) / 10) - (cap_num / bet_rate) + 15), 2)
                entries[row][col]['second_day_YT']=entry['second_day_YT']
                entries[row][col]['total_winning']+=yatirilacak_tutar*bet_rate
                


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

            if bet_site == 0:  # oflu
                if betted_outcome == 0:
                    bet_rate = float(request.form.get('oflu0', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                elif betted_outcome == 1:
                    bet_rate = float(request.form.get('oflu1', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                elif betted_outcome == 2:
                    bet_rate = float(request.form.get('oflu2', 0))
                    entries[row][col]['bet_Rate']=bet_rate
            elif bet_site == 1:  # sex
                if betted_outcome == 0:
                    bet_rate = float(request.form.get('sex0', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                elif betted_outcome == 1:
                    bet_rate = float(request.form.get('sex1', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                elif betted_outcome == 2:
                    bet_rate = float(request.form.get('sex2', 0))
                    entries[row][col]['bet_Rate']=bet_rate
            elif bet_site == 2:  # chad
                if betted_outcome == 0:
                    bet_rate = float(request.form.get('chad0', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                elif betted_outcome == 1:
                    bet_rate = float(request.form.get('chad1', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                elif betted_outcome == 2:
                    bet_rate = float(request.form.get('chad2', 0))
                    entries[row][col]['bet_Rate']=bet_rate
                    
            bonus_orani = 0
            cap_num = entries[row][col]['cap_number']

            # Assign bonus rate based on bet_site
            if bet_site == 0:
                bonus_orani = oflu_bonus
                entries[row][col]['bonus_orani']=bonus_orani

                
            elif bet_site == 1:
                bonus_orani = sex_bonus
                entries[row][col]['bonus_orani']=bonus_orani
            elif bet_site == 2:
                bonus_orani = chad_bonus
                entries[row][col]['bonus_orani']=bonus_orani

            yatirilacak_tutar = (cap_num * 100) / (bet_rate * (100 + bonus_orani))
            entries[row][col]['yatirilacak_tutar']=round(yatirilacak_tutar,2)
            entries[row][col]['total_winning']-=yatirilacak_tutar


@app.route("/", methods=["GET", "POST"])
def index():
    global inputs
    global preset_num
    global bonus_rates
    global winning_outcome
    global entries
    global match_name
    global second_winning_outcome
    

    
    

    if request.method == "POST":
        
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


        # Retrieve preset_num from form
        preset_num = int(request.form.get('table_type', 0))        

        # Retrieve winning outcome from form and debug print
        winning_outcome = int(request.form.get('winning_outcome', '0'))
    
        # Update entries based on the preset number
        update_entries(preset_num, entries)
        calculate_second_day(entries, winning_outcome,second_winning_outcome)
        match_name=request.form.get('match_name', 'default')

        print(entries)

        
    # Render the template with current values (no default fallback)
    return render_template('home.html',
                           preset_num=preset_num,
                           bonus_rates=bonus_rates,
                           inputs=inputs,
                           entries=entries,
                           second_winning_outcome=second_winning_outcome,
                           winning_outcome=winning_outcome,
                           match_name=match_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
