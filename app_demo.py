from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
import urllib


app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
	if request.method=='POST': # basic Flask structure 
		url=request.form['iurl'] 
		raw=requests.get(url) # make a request to the URL

		soup=BeautifulSoup(raw.text,'html.parser') # get the HTML

		
		name = request.form['name']
		filename = request.form['file']

		if filename == "jpg":
			name = name + ".jpg"
			links= soup.find(property="og:image") 
			image=links.get('content') # get link
			urllib.request.urlretrieve(image, name)  # save

		if filename == "mp4":
			name = name + ".mp4"
			links2= soup.find(property="og:image") 
			links= soup.find(property="og:video")
			image=links2.get('content') # show imgae
			image_save = links.get('content')
			urllib.request.urlretrieve(image_save, name)  
		# return in the browser
		while image!='':
			return '<img src="'+image+'"'+ 'align="center">' # view item

	return render_template('index.html')

if __name__=='__main__':
	app.run()
