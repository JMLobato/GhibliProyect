from flask import Flask, url_for, render_template
import requests
app = Flask(__name__)

@app.route('/')
def inicio(): 
	return render_template("index.html")

#r=requests.get('https://ghibliapi.herokuapp.com/films')
#if r.status_code == 200:
#	doc = r.json()
#	for peli in doc:
#		print(peli["title"])
#		print(peli["director"])
#		print(peli["producer"])
#		print(peli["release_date"])
#		print()


@app.errorhandler(404)
def page_not_found(error):
	return 'Parece que algo esta fallando...', 404

if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)