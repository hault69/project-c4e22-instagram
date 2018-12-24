from flask import *
import requests
from bs4 import BeautifulSoup
import urllib

app= Flask(__name__)

data = {
    'url': '',
    'raw': '',
    'soup': '',
}


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'GET':
	    return render_template('index.html')
    elif request.method=='POST': 
        url=request.form['iurl']
        raw=requests.get(url) 
        soup=BeautifulSoup(raw.text,'html.parser')
        #filter data
        links= soup.find(property="og:image")		
        # links_video = soup.find(property="og:video")
        image=links.get('content')
        data['url'] = url
        data['raw'] = raw
        data['soup'] = soup
        # video=link.get('content')
        while image!='':
            print(data['url'])
            return redirect(url_for('download'))

@app.route("/download",methods=['GET','POST'])
def download():
    if request.method=='GET':
        return render_template('download.html', url = data['url'])
    if request.method=='POST':
        url = data['url']
        raw = data['raw']
        soup = data['soup']
        name = request.form['name']
        filename = request.form['file']
        if filename == 'jpg':
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
            return redirect("/")
            # return '<img src="'+image+'"'+ 'align="center">' # view item

if __name__=='__main__':
	app.run()