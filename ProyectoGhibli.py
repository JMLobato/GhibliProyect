from flask import Flask, url_for, render_template, request
from jinja2 import Template
import requests
app = Flask(__name__)
@app.route('/')
def inicio():
	r=requests.get('https://ghibliapi.herokuapp.com/films')
	doc = r.json()
	lista=[]
	for elem in doc:
		lista.append(elem["title"])
	return render_template("index.html",lista=lista)

@app.route('/peliculas')
def peliculas():
	r=requests.get('https://ghibliapi.herokuapp.com/films')
	doc = r.json()
	return render_template("films.html",doc=doc)

@app.route('/search',methods=['GET','POST'])
def search(q=None,cosa=None):
	q=request.form.get("q")
	if q:
		r=requests.get('https://ghibliapi.herokuapp.com/films')
		doc = r.json()
		lista=[]
		lista2=[]
		lista3=[]
		for peli in doc:
			if q.upper() == peli["title"].upper():
				lista.append(peli["title"])
				lista.append(peli["director"])
				lista.append(peli["producer"])
				lista.append(peli["release_date"])
				cosa="peli"
		r=requests.get('https://ghibliapi.herokuapp.com/people')
		doc = r.json()
		for person in doc:
			if q.upper() == person["name"].upper():
				lista.append(person["name"])
				lista.append(person["gender"])
				lista.append(person["age"])
				for elem in person["films"]:
					r=requests.get(elem)
					lista2.append(r.json())
				r=requests.get(person["species"])
				lista3.append(r.json())
				cosa="persona"
		r=requests.get('https://ghibliapi.herokuapp.com/locations')
		doc = r.json()
		for local in doc:
			if q.upper() == local["name"].upper():
				lista.append(local["name"])
				lista.append(local["climate"])
				lista.append(local["terrain"])
				for elem in local["films"]:
					r=requests.get(elem)
					lista2.append(r.json())
				for elem in local["residents"]:
					r=requests.get(elem)
					lista3.append(r.json())
				cosa="localizacion"
		r=requests.get('https://ghibliapi.herokuapp.com/species')
		doc = r.json()
		for specimen in doc:
			if q.upper() == specimen["name"].upper():
				lista.append(specimen["name"])
				lista.append(specimen["eye_colors"])
				lista.append(specimen["hair_colors"])
				for elem in specimen["films"]:
					r=requests.get(elem)
					lista2.append(r.json())
				for elem in specimen["people"]:
					r=requests.get(elem)
					lista3.append(r.json())
				cosa="specie"
		r=requests.get('https://ghibliapi.herokuapp.com/vehicles')
		doc = r.json()
		for car in doc:
			if q.upper() == car["name"].upper():
				lista.append(car["name"])
				lista.append(car["description"])
				lista.append(car["vehicle_class"])
				r=requests.get(car["films"])
				lista2.append(r.json())
				r=requests.get(car["pilot"])
				lista3.append(r.json())
				cosa="coche"
		if cosa:
			return render_template("busqueda.html",lista=lista,lista2=lista2,lista3=lista3,cosa=cosa)
		else:
			return render_template("search.html")
	else:
		return render_template("search.html")

@app.errorhandler(404)
def page_not_found(error):
	return render_template("fallo.html"), 404
@app.errorhandler(405)
def search_not_found(error):
	return render_template("search.html"), 405

if __name__ == '__main__':
    port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)