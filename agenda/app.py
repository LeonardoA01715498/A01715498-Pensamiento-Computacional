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
        cur.execute('CREATE TABLE IF NOT EXISTS empleados (id INTEGER PRIMARY KEY, persona REAL, pay TEXT)')
        con.commit()
        res = cur.execute('SELECT * FROM sales')
        #print(res.fetchall())
        res = cur.execute('SELECT * FROM empleados')
        #print(res.fetchall())

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        dates = cur.execute('SELECT * FROM agenda')
        date = dates.fetchall()
        if request.method == 'POST':
            names = request.form.get('hora')
            persona = request.form.get('person')
            evento = request.form.get('evento')
            sale = sales(evento)
            pay = payment(evento)
            month = request.form.get('month')
            day = request.form.get('day')
            if names and persona and evento:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute('INSERT INTO agenda (hora, persona, evento, mes, dia) VALUES (?, ?, ?, ?, ?)', (names, persona, evento, month, day))
                    cur.execute('INSERT INTO sales (price, evento) VALUES (?, ?)', (sale, evento))
                    cur.execute('INSERT INTO empleados (persona, pay) VALUES (?, ?)', (persona, pay))
                    con.commit()
                return render_template('index.html', hour=date, month=month, day=day)
    return render_template('index.html', hour=date)

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
        return render_template('index.html', month=month, day=day, year=year, hour=date)
    return render_template('month.html')

def payment(evento):
    price = sales(evento)
    sale = price
    pay = (sale/2) - (sale * 0.15)
    print(f"Precio: {sale}")
    print(f"Pago: {pay}")
    return pay

def sales(evento):
    prices = {
        "Reunion": 50.0,
        "Cita Medica": 75.0,
        "Cumpleanos": 100.0,
        "Otro": 30.0
    }
    return prices.get(evento, 0.0)