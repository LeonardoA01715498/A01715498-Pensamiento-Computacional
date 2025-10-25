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
        cur.execute('CREATE TABLE IF NOT EXISTS pagos (id INTEGER PRIMARY KEY, persona REAL, pay TEXT, id_empleado INTEGER, FOREIGN KEY (id_empleado) REFERENCES empleados(id))')
        con.commit()
        cur.execute('CREATE TABLE IF NOT EXISTS empleados (id INTEGER PRIMARY KEY, persona UNIQUE)')
        con.commit()
        #cur.execute('DELETE FROM pagos WHERE id > 0')
        # pagos = cur.execute('SELECT COUNT(id) FROM pagos').fetchall()
        # print(pagos)
        # for x in range (pagos[0][0]):
        #     pago = cur.execute('SELECT * FROM pagos WHERE id = ?', (x, )).fetchall()
        #     print(pago)

init_db()
@app.route('/index', methods=['GET', 'POST'])
# app.py

# ... (resto del código)

@app.route('/index', methods=['GET', 'POST'])
# app.py

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("\n--- DATOS RECIBIDOS DEL FORMULARIO ---")
        print(f"Formulario completo: {request.form}")
        # ----------------------------------------
        
        names = request.form.get('hora')
        persona = request.form.get('person')
        evento = request.form.get('evento')
        month = request.form.get('month')
        day = request.form.get('day')

        # Comprueba si alguna variable es None (valor faltante)
        if not (names and persona and evento and month and day):
            print("❌ ERROR 400: Uno o más campos faltan o son None.")
            return {'error': 'Faltan datos requeridos.'}, 400


        try:
            # 1. Ejecutar las funciones que modifican la DB
            sale = prices(evento)
            pay = payment(evento) 
            
            # 2. Guardar en la base de datos (agenda y sales)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO agenda (hora, persona, evento, mes, dia) VALUES (?, ?, ?, ?, ?)', (names, persona, evento, month, day))
                cur.execute('INSERT INTO sales (price, evento) VALUES (?, ?)', (sale, evento))
                con.commit()
            
            # 3. Respuesta de éxito para el AJAX de JavaScript
            # El código 204 (No Content) es ideal para indicar éxito sin enviar datos de vuelta.
            return '', 204 

        except Exception as e:
            # Capturar errores del servidor (DB, lógica)
            print(f"Error al procesar la petición POST: {e}")
            return {'error': f'Error interno del servidor: {e}'}, 500

    # Lógica para la petición GET (Carga inicial de la página)
    # ... (Tu código GET original)
    month_name = request.args.get('month')
    day = request.args.get('day')
    date = []
    
    if day:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            dates = cur.execute('SELECT * FROM agenda WHERE dia = ?', (day.strip(),)) 
            date = dates.fetchall()

    return render_template('index.html', hour=date, month=month_name, day=day)


@app.route('/', methods=['GET', 'POST'])
@app.route('/month', methods=['GET', 'POST'])

def month():
    if request.method == 'POST':
        month_num = int(request.form.get('month'))
        month = calendar.month_name[month_num]
        day = request.form.get('day')
        year = request.form.get('year')
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
        id_pago = cur.execute('SELECT id FROM empleados').fetchall()
        pay_ids = cur.execute('SELECT * FROM pagos').fetchall()
        #print(id_pago)
        #print(people)
        #print(pay_ids)
        #print(id_pago[0][0])
    price = prices(evento)
    sale = price
    pay = (sale/2) - (sale * 0.15)
    pay_id = pay / people[0][0]
    num_people = int(people[0][0])
    print(f"Precio: {sale}")
    print(f"Pago: {pay_id}")
    i = 0
    while (i < num_people):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO pagos (pay, id_empleado) VALUES (?, ?)', (pay_id, id_pago[i][0]))
            con.commit()
        pay -= pay_id
        i+=1
    print("Lista de pagos por id:")
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        pagos = cur.execute('SELECT COUNT(id) FROM pagos').fetchall()
        for x in range (pagos[0][0]):
            pago = cur.execute('SELECT * FROM pagos WHERE id = ?', (x, )).fetchall()
            print(pago)
    return pay

def prices(evento):
    prices = {
        "Reunion": 50.0,
        "Cita Medica": 75.0,
        "Cumpleanos": 100.0,
        "Otro": 30.0
    }
    return prices.get(evento, 0.0)

