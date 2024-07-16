from flask import Flask, render_template, request

app = Flask(__name__)
result_table=None
@app.route("/", methods=["GET", "POST"])
def index():
    global result_table
    if request.method == "POST":
        inputs = {}
        # List of input names
        input_names = ['oflu0', 'oflu1', 'oflu2', 'sex0', 'sex1', 'sex2', 'chad0', 'chad1', 'chad2']
        for name in input_names:
            input_value = request.form.get(name)
            if input_value:
                inputs[name] = float(input_value)

        # Prepare the result table with the calculation 4000 / input value
        result_table = [
            [4000 / inputs.get('oflu0', 1), 4000 / inputs.get('sex0', 1), 4000 / inputs.get('chad0', 1)],
            [4000 / inputs.get('oflu1', 1), 4000 / inputs.get('sex1', 1), 4000 / inputs.get('chad1', 1)],
            [4000 / inputs.get('oflu2', 1), 4000 / inputs.get('sex2', 1), 4000 / inputs.get('chad2', 1)],
        ]
        for row in range(len(result_table)):
            for col in range(len(result_table[row])):
                result_table[row][col] = "{:.2f}".format(result_table[row][col])
    # Always render the template with the result_table, even if it's None
    return render_template('home.html', result_table=result_table)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
