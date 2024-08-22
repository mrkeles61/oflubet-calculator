from flask import Flask, render_template, request
from erentemplates import entries_template,ilk_yatirma_template,kalan_cevrim_template,entries_template_second
import copy

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
            bet_site = str(entries[row][col]['bet_site'])
            betted_outcome = str(entries[row][col]['betted_outcome'])
            bonus_orani=bonus_rates[bet_site]   
            
            bet_rate=rate_inputs[bet_site][betted_outcome]
            
            cap_num = entries[row][col]['cap_number']

            yatirilacak_tutar = (cap_num * 100) / (bet_rate * (100 + bonus_orani))
            entries[row][col]['bonus_orani']=bonus_orani
            entries[row][col]['bet_Rate']=bet_rate
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
    inputs_first={}
    inputs_second={}
    preset_num = None
    preset_num_second=None
    bonus_rates_first = {}
    bonus_rates_second={}
    match_name='AYIBOĞAN'
    match_name_second='Karlsruhe-Stuttgart'
    winning_outcome= None
    winning_outcome_second=None
    entries_first=entries_template
    entries_second=entries_template_second
    ilk_yatirma=ilk_yatirma_template
    kalan_cevrim=ilk_yatirma_template

    

    
    

    if request.method == "POST":
        
        bonus_rates_first = {
            '0': int(request.form.get('oflubonus', '3')),
            '1': int(request.form.get('sexbonus', '3')),
            '2': int(request.form.get('chadbonus', '3')),
        }

        bonus_rates_second = {
            '0': int(request.form.get('paribonus', '3')),
            '1': int(request.form.get('trbonus', '3')),
            '2': int(request.form.get('kanyonbonus', '3')),
        }

        inputs_first = {
            '0': {
                '0': float(request.form.get('oflu0', '3')),
                '1': float(request.form.get('oflu1', '3')),
                '2': float(request.form.get('oflu2', '3'))
            },
            '1': {
                '0': float(request.form.get('sex0', '3')),
                '1': float(request.form.get('sex1', '3')),
                '2': float(request.form.get('sex2', '3'))
            },
            '2': {
                '0': float(request.form.get('chad0', '3')),
                '1': float(request.form.get('chad1', '3')),
                '2': float(request.form.get('chad2', '3'))
            }
        }

        inputs_second = {
            '0': {
                '0': float(request.form.get('pari0', '3')),
                '1': float(request.form.get('pari1', '3')),
                '2': float(request.form.get('pari2', '3'))
            },
            '1': {
                '0': float(request.form.get('tr0', '3')),
                '1': float(request.form.get('tr1', '3')),
                '2': float(request.form.get('tr2', '3'))
            },
            '2': {
                '0': float(request.form.get('kanyon0', '3')),
                '1': float(request.form.get('kanyon1', '3')),
                '2': float(request.form.get('kanyon2', '3'))
            }
        }



    



        
        

        # get both table types from user input
        preset_num = int(request.form.get('table_type', 0))       
        preset_num_second=int(request.form.get('table_type_second',0))

        # assign winning outcomes
        winning_outcome = int(request.form.get('winning_outcome', '0'))
        winning_outcome_second= int(request.form.get('winning_outcome_second', '0'))

        


        update_entries(preset_num, entries_first,inputs_first,bonus_rates_first)


        update_entries(preset_num_second,entries_second,inputs_second,bonus_rates_second)
        
        
        calculate_second_day(entries_first, winning_outcome)
        calculate_second_day(entries_second,winning_outcome_second)

        

        

        print(inputs_first,bonus_rates_first,winning_outcome,preset_num)

        print("\n\n")

        print(inputs_second,bonus_rates_second,winning_outcome_second,preset_num_second)

        print("\n\n")

        for row in range(3):
            for col in range(3):
                print(entries_first[row][col]['bet_Rate'])
                print(entries_first[row][col]['bonus_orani'])
                print(entries_first[row][col]['yatirilacak_tutar'])
                print(entries_first[row][col]['second_day_YT'])
                print(winning_outcome)
                     

        print("\n\n")

        for row in range(3):
            for col in range(3):
                print(entries_second[row][col]['bet_Rate'])
                print(entries_second[row][col]['bonus_orani'])
                print(entries_second[row][col]['yatirilacak_tutar'])
                print(entries_second[row][col]['betted_outcome'])
                print(winning_outcome_second)
        

        

    else:
    # Page refresh or initial GET request: Reset to default values
        entries_first = copy.deepcopy(entries_template)
        entries_second = copy.deepcopy(entries_template_second)
        ilk_yatirma = copy.deepcopy(ilk_yatirma_template)
        kalan_cevrim = copy.deepcopy(kalan_cevrim_template)
        bonus_rates_first = {}
        bonus_rates_second = {}
        inputs_first = {}
        inputs_second = {}
        winning_outcome = None
        winning_outcome_second = None

        
    # Render the template with current values (no default fallback)
    return render_template('home.html',
                           ilk_yatirma=ilk_yatirma,
                           kalan_cevrim=kalan_cevrim,
                           preset_num=preset_num,
                           preset_num_second=preset_num_second,
                           bonus_rates_first=bonus_rates_first,
                           bonus_rates_second=bonus_rates_second,
                           inputs_first=inputs_first,
                           inputs_second=inputs_second,
                           entries_first=entries_first,
                           entries_second=entries_second,
                           winning_outcome=winning_outcome,
                           winning_outcome_second=winning_outcome_second,
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
