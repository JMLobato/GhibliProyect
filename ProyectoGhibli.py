from flask import Flask, url_for, render_template, request
from jinja2 import Template
import requests
app = Flask(__name__)
r=requests.get('https://ghibliapi.herokuapp.com/films')
doc = r.json()
@app.route('/')
def inicio():
	lista=[]
	for elem in doc:
		lista.append(elem["title"])
	return render_template("index.html",lista=lista)

@app.route('/peliculas')
def peliculas():
	return render_template("films.html",doc=doc)

@app.route('/search')
def search():
	r=requests.get('https://ghibliapi.herokuapp.com/people')
	doc2 = r.json()
	r=requests.get('https://ghibliapi.herokuapp.com/locations')
	doc3 = r.json()
	r=requests.get('https://ghibliapi.herokuapp.com/species')
	doc3 = r.json()
	r=requests.get('https://ghibliapi.herokuapp.com/vehicles')
	doc4 = r.json()
	q=request.form.get("q")
	return render_template("busqueda.html",doc=doc,doc2=doc2,doc3=doc3,doc4=doc4,q=q)

@app.errorhandler(404)
def page_not_found(error):
	return render_template("fallo.html"), 404

if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)