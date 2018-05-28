from flask import Flask,render_template,redirect,request,session,abort
from jinja2 import Template
import requests
from requests_oauthlib import OAuth2Session
from urllib.parse import parse_qs
import os,json
app = Flask(__name__)   
app.secret_key= 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
			abort(405)
	else:
		abort(405)

redirect_uri_sp = 'https://proyecto-ghibli.herokuapp.com/spotify_callback'
scope_sp = 'user-read-private user-read-email'
token_url_sp = "https://accounts.spotify.com/api/token"

def token_valido_spotify():
    try:
        token=json.loads(session["token_sp"])
    except:
        token = False
    if token:
        token_ok = True
        try:
            oauth2 = OAuth2Session(os.environ["client_id_spotify"], token=token)
            r = oauth2.get('https://api.spotify.com/v1/me')
        except TokenExpiredError as e:
            token_ok = False
    else:
        token_ok = False
    return token_ok

@app.route('/perfil_spotify')
def info_perfil_spotify():
  if token_valido_spotify():
    return redirect("/perfil_usuario_spotify")
  else:
    oauth2 = OAuth2Session(os.environ["client_id_spotify"], redirect_uri=redirect_uri_sp,scope=scope_sp)
    authorization_url, state = oauth2.authorization_url('https://accounts.spotify.com/authorize')
    session.pop("token_sp",None)
    session["oauth_state_sp"]=state
    return redirect(authorization_url)  

@app.route('/spotify_callback')
def get_token_spotify():
    oauth2 = OAuth2Session(os.environ["client_id_spotify"], state=session["oauth_state_sp"],redirect_uri=redirect_uri_sp)
    print (request.url)
    token = oauth2.fetch_token(token_url_sp, client_secret=os.environ["client_secret_spotify"],authorization_response=request.url[:4]+"s"+request.url[4:])
    session["token_sp"]=json.dumps(token)
    return redirect("/perfil_usuario_spotify")

@app.route('/perfil_usuario_spotify')
def info_perfil_usuario_spotify():
    if token_valido_spotify():
        token=json.loads(session["token_sp"])
        oauth2 = OAuth2Session(os.environ["client_id_spotify"], token=token)
        r = oauth2.get('https://api.spotify.com/v1/me')
        doc=json.loads(r.content.decode("utf-8"))
        return render_template("canciones.html", datos=doc)
    else:
        return redirect('/perfil')

@app.route('/logout_spotify')
def salir_spotify():
    session.pop("token_sp",None)
    return redirect("/")

@app.errorhandler(404)
def page_not_found(error):
	return render_template("fallo.html"), 404

@app.errorhandler(405)
def search_not_found(error):
	return render_template("search.html"), 405

if __name__ == '__main__':
	port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)