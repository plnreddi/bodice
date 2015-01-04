from flask import Flask, request, jsonify
from Bodice1.BasicBodice import data2Server

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static/')

data = data2Server()
print data

@app.route('/')
def root():
    return app.send_static_file('app/index.html')


@app.route('/static/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)


@app.route('/api/basicbodice')
def basicbodice_output():
	return jsonify(data=data)

if __name__ == "__main__":
    app.run(debug=True)
