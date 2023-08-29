from flask import Flask, jsonify
from collections import OrderedDict
import json

app = Flask(__name__)
y = [] #history

def evaluate(expression):
    try:
        result = eval(expression)
        en = OrderedDict([('question', expression), ('answer', result)])

        if en not in y:
            y.append(en)

        if len(y) > 20:
            y.pop(0)

        return result, expression
    except Exception as e:
        return None, None


@app.route('/')
def home():
    return "Kalvium Task"


@app.route('/history')
def get_history():
    return jsonify(y)


@app.route('/<path:expression>')
def calculate(expression):

    expression = expression.replace('/', ' ').replace('plus', '+').replace('minus', '-').replace('into', '*').replace(
        'by', '/')

    op = {
        '+': ' + ',
        '-': ' - ',
        '*': ' * ',
        '/': ' / ',
    }
    for o, r in op.items():
        expression = expression.replace(o, r)

    result, question = evaluate(expression)
    if result is not None:
        x = OrderedDict([('question', question), ('answer', result)])
        return json.dumps(x)
    else:
        return jsonify({'ERROR': 'Invalid Expression'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=3000)