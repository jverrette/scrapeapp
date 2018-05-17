from flask import Flask, render_template, request
import pythonFile

app = Flask(__name__)
 
@app.route('/<name>')
def hello2(name='index'):
    return render_template('index.html', name=name)

@app.route('/send', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        outputter = request.form['website']
        lister = pythonFile.db(outputter)
        return render_template('response.html', website=outputter, phone=pythonFile.phone(lister), email=pythonFile.emails(lister))
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run()
