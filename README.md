# A01715498-Pensamiento-Computacional

El proyecto es una pagina para agendar servicios para un comercio. La idea del proyecto es como usuario poder personalizar tus servicios y empleados para poder agendar y llevar todo el contenido relacionado con las ventas. Este programa llevara una agenda por dia donde se mostraran los empleados disponibles y las horas en las que pueden trabajar. Al agendar un evento se le asignara un precio a este y al momento de completar el pago se mandara toda la informacion a la base de datos para en un modulo aparte poder administrar toda el area de finanzas.

Dependencias:
Flask:  pip install Flask     https://flask.palletsprojects.com/en/stable/installation/#python-version

Run:
Crear enviroment:
  > cd agenda
  > python3 -m venv .venv
  > pip install Flask

Correr programa:
flask run

Esto mostrara un link en la terminal con el puerto 500 en local host

Al abrir el link te llevara a una pagina donde podras seleccionar una hora y un evento el cual tendra un precio asignado. Las operaciones se hacen en el documento app.py en la funcion payment donde al agendar un evento los precios se mostraran en la terminal

#ignore all the mess 😬#

