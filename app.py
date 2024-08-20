from flask import Flask, render_template, request
from erentemplates import entries_template,ilk_yatirma_template,kalan_cevrim_template

app = Flask(__name__)


  

def calculate_second_day(entries, winning_outcome):
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
                


def update_entries(preset_num, entries, rate_inputs,bonus_rates):
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
            bet_site = int(entries[row][col]['bet_site'])
            betted_outcome = int(entries[row][col]['betted_outcome'])
            bet_rate=float(rate_inputs[bet_site][betted_outcome])
            bonus_orani=bonus_rates[bet_site]       
            
            cap_num = entries[row][col]['cap_number']

            yatirilacak_tutar = (cap_num * 100) / (bet_rate * (100 + bonus_orani))
            entries[row][col]['yatirilacak_tutar']=round(yatirilacak_tutar,2)

def calculate_total_deposits(entries, ilk_yatirma ,kalan_cevrim):
    for row in range(3):
        for col in range(3):
            bet_site=entries[row][col]['bet_site']
            yatiran=entries[row][col]['betted_by']
            yatirilacak_tutar=entries[row][col]['yatirilacak_tutar']
            cevrim=entries[row][col]['second_day_YT']
            ilk_yatirma[yatiran][bet_site]+=yatirilacak_tutar
            kalan_cevrim[yatiran][bet_site]+=cevrim

    


@app.route("/", methods=["GET", "POST"])
def index():
    inputs={}
    inputs_second={}
    preset_num = None
    preset_num_second=None
    bonus_rates = {}
    bonus_rates_second={}
    match_name='AYIBOĞAN'
    match_name_second='Karlsruhe-Stuttgart'
    winning_outcome= None
    winning_outcome_second=None
    entries=entries_template
    entries_second=entries_template
    ilk_yatirma=ilk_yatirma_template
    kalan_cevrim=ilk_yatirma_template

    

    
    

    if request.method == "POST":
        #collect first table's inputs in dictionaries so it could be used as placeholder values
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


        #second table, same process
        inputs_second = {
            'pari1': request.form.get('pari1', ''),
            'pari0': request.form.get('pari0', ''),
            'pari2': request.form.get('pari2', ''),
            'tr1': request.form.get('tr1', ''),
            'tr0': request.form.get('tr0', ''),
            'tr2': request.form.get('tr2', ''),
            'kanyon1': request.form.get('kanyon1', ''),
            'kanyon0': request.form.get('kanyon0', ''),
            'kanyon2': request.form.get('kanyon2', ''),
        }
        
        bonus_rates_second = {
            'pari': request.form.get('paribonus', ''),
            'tr': request.form.get('trbonus', ''),
            'kanyon': request.form.get('kanyonbonus', '')
        }

        inputs_first = [
            [request.form.get('oflu0', ''), request.form.get('oflu1', ''), request.form.get('oflu2', '')],
            [request.form.get('sex0', ''), request.form.get('sex1', ''), request.form.get('sex2', '')],
            [request.form.get('chad0', ''), request.form.get('chad1', ''), request.form.get('chad2', '')]
        ]

        inputs_second = [
            [request.form.get('pari0', ''), request.form.get('pari1', ''), request.form.get('pari2', '')],
            [request.form.get('tr0', ''), request.form.get('tr1', ''), request.form.get('tr2', '')],
            [request.form.get('kanyon0', ''), request.form.get('kanyon1', ''), request.form.get('kanyon2', '')]
        ]

        bonus_rates_first = [
            request.form.get('oflubonus', ''),
            request.form.get('sexbonus', ''),
            request.form.get('chadbonus', '')
        ]

        bonus_rates_second = [
            request.form.get('paribonus', ''),
            request.form.get('trbonus', ''),
            request.form.get('kanyonbonus', '')
        ]



        
        

        # get both table types from user input
        preset_num = int(request.form.get('table_type', 0))       
        preset_num_second=int(request.form.get('table_type_second',0))

        # assign winning outcomes
        winning_outcome = int(request.form.get('winning_outcome', '0'))
        winning_outcome_second= int(request.form.get('winning_outcome_second', '0'))

        #assign both of the match names accordingly
        match_name=request.form.get('match_name', 'default')
        match_name_second=request.form.get('match_name_second', 'default')
    
        
        update_entries(preset_num, entries,inputs_first,bonus_rates_first)
        calculate_second_day(entries, winning_outcome)

        update_entries(preset_num_second, entries_second,inputs_second,bonus_rates_second)
        calculate_second_day(entries_second, winning_outcome_second)

        calculate_total_deposits(entries,ilk_yatirma,kalan_cevrim)
        calculate_total_deposits(entries_second,ilk_yatirma,kalan_cevrim)
        

        

    else:  # If request is GET, reset all variables to their default state
        inputs={}
        inputs_second={}
        preset_num = None
        preset_num_second=None
        bonus_rates = {}
        bonus_rates_second={}
        match_name='AYIBOĞAN'
        match_name_second='Karlsruhe-Stuttgart'
        winning_outcome= None
        winning_outcome_second=None
        entries=entries_template
        entries_second=entries_template
        ilk_yatirma=ilk_yatirma_template
        kalan_cevrim=ilk_yatirma_template

        
    # Render the template with current values (no default fallback)
    return render_template('home.html',
                           ilk_yatirma=ilk_yatirma,
                           kalan_cevrim=kalan_cevrim,
                           preset_num=preset_num,
                           preset_num_second=preset_num_second,
                           bonus_rates=bonus_rates,
                           bonus_rates_second=bonus_rates_second,
                           inputs=inputs,
                           inputs_second=inputs_second,
                           entries=entries,
                           entries_second=entries_second,
                           winning_outcome=winning_outcome,
                           winning_outcome_second=winning_outcome_second,
                           match_name_second=match_name_second,
                           match_name=match_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
