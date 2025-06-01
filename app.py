from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, expression TEXT, result TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    operand1 = data.get('operand1')
    operand2 = data.get('operand2')
    operator = data.get('operator')
    expression = f"{operand1} {operator} {operand2}"
    try:
        # Secure calculation
        if operator not in ['+', '-', '*', '/']:
            raise Exception('Invalid operator')
        op1 = float(operand1)
        op2 = float(operand2)
        if operator == '+':
            result = op1 + op2
        elif operator == '-':
            result = op1 - op2
        elif operator == '*':
            result = op1 * op2
        elif operator == '/':
            if op2 == 0:
                raise Exception('Division by zero')
            result = op1 / op2
        result_str = str(result)
        store_history(expression, result_str)
        return jsonify({'result': result_str})
    except Exception as e:
        return jsonify({'result': 'Error'})

def store_history(expression, result):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (expression, result) VALUES (?, ?)', (expression, result))
    conn.commit()
    conn.close()

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('SELECT expression, result FROM history ORDER BY id DESC LIMIT 10')
    rows = c.fetchall()
    conn.close()
    return jsonify({'history': rows})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)