import os

from flask import render_template, request, send_from_directory

from atmospheres import app
from atmospheres.db.datastore import DataStore



app.db = DataStore()

@app.route('/')
def home():
    #import pdb; pdb.set_trace()
    #result = render_template('geo.html') 
    return render_template('geo.html')
    #return result

@app.route('/static/sf_zips.topo.json')
def get_topo_json():
   return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'sf_zips.topo.json',
    )

@app.route('/data/sentiments')
def get_live_sentiments_json():
   return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'demo_sentiments.json',
    )

@app.route('/postdata/', methods=['POST'])
def store_post():
    # This method is expecting json object. When client sends the
    # json data, it should also sets the request header Content-Type 
    # to application/json.
    data = { "mypostdata": request.json }  # { 'mypostdata': { 'fname': 'kumari', 'lname': 'sweta'}}
    print data
    app.db.write(data)
    return 'Thank you for the data'


def main():
    app.run(debug=True)



if __name__=="__main__":
    main()