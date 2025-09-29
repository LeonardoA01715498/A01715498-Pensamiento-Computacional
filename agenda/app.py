from flask import Flask, request, render_template, redirect
import sqlite3
import calendar

app = Flask(__name__)

#.\.venv\Scripts\activate

def init_db():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS agenda (id INTEGER PRIMARY KEY, persona TEXT, hora TEXT, dia TEXT, mes TEXT, year TEXT, evento TEXT)')
        con.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, price REAL, evento TEXT)')
        con.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS pagos (id INTEGER PRIMARY KEY, persona REAL, pay TEXT)')
        con.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS empleados (id INTEGER PRIMARY KEY, persona UNIQUE)')
        con.commit()

init_db()

def index():
        if request.method == 'POST':
            names = request.form.get('hora')
            persona = request.form.get('person')
            evento = request.form.get('evento')
            sale = prices(evento)
            pay = payment(evento)
            month = request.form.get('month')
            day = request.form.get('day')
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                dates = cur.execute('SELECT * FROM agenda WHERE dia LIKE ?', ('%' + day + '%',))
                date = dates.fetchall()
            if names and persona and evento:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO agenda (hora, persona, evento, mes, dia) VALUES (?, ?, ?, ?, ?)', (names, persona, evento, month, day))
                    cur.execute('INSERT INTO sales (price, evento) VALUES (?, ?)', (sale, evento))
                    cur.execute('INSERT INTO pagos (persona, pay) VALUES (?, ?)', (persona, pay))
                    con.commit()
                return render_template('index.html', hour=date, month=month, day=day)
        return render_template('index.html', hour=date)

@app.route('/', methods=['GET', 'POST'])
@app.route('/month', methods=['GET', 'POST'])

def month():
    if request.method == 'POST':
        month_num = int(request.form.get('month'))
        day = request.form.get('day')
        year = request.form.get('year')
        month = calendar.month_name[month_num + 1]
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            dates = cur.execute('SELECT * FROM agenda WHERE dia LIKE ?', ('%' + day + '%',))
            date = dates.fetchall()
            print(date)
        return render_template('index.html', month=month, day=day, year=year, hour=date,)
    return render_template('month.html')


@app.route('/crear', methods=['GET', 'POST'])

def crear():
    if request.method == 'POST':
        name = request.form.get('name')
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO empleados (persona) VALUES (?)', (name,))
            con.commit()
    return render_template('crear.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    return render_template('menu.html')

def payment(evento):
    #Need to add amount of people to the function
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        people = cur.execute('SELECT COUNT(persona) FROM empleados').fetchall()
    price = prices(evento)
    sale = price
    pay = (sale/2) - (sale * 0.15)
    while sale > 0:
        for i in range (people[0][0]):
            pay = pay / people[0][0]
    #Assign to each employee
    print(f"Precio: {sale}")
    print(f"Pago: {pay}")
    return pay

def prices(evento):
    prices = {
        "Reunion": 50.0,
        "Cita Medica": 75.0,
        "Cumpleanos": 100.0,
        "Otro": 30.0
    }
    return prices.get(evento, 0.0)

