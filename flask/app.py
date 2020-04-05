from flask import Flask

app = Flask(__name__)

@app.route('/hello')
@app.route('/hello/<string:name>')
def hello(name=None):
    if name is None:
        name = 'Avon'
        
    return 'hello {}\n'.format(name)

app.run(debug=True, host='0.0.0.0', port=9000)