from flask import Flask, request, jsonify
from Bodice1.BasicBodice import data2Server

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static/')

'''
data = data2Server()
print data
'''

@app.route('/')
def root():
    return app.send_static_file('app/index.html')


@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

'''
@app.route('/api/basicbodice')
def basicbodice_output():
	return jsonify(data=data)
'''

@app.route('/api/basicbodice', methods=['GET', 'POST'])
def basicbodice_output():

    if request.method == "POST":
        user_data = request.json['usr_data']
        data2 = data2Server(user_data)
        print data2
        return jsonify(data=data2)
    '''
	data2 = data2Server()
	return jsonify(data=data2)
    '''

if __name__ == "__main__":
    app.run(debug=True)


    '''
    usr_data = 'ok'
    print usr_data
    
	if request.method=='POST':
    	usr_data = request.get_json()
    	print usr_data

        usr_data = json.loads(request.data)
    '''