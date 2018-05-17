from flask import Flask, render_template, request
import pythonFile

app = Flask(__name__)
 
@app.route('/<name>')
def hello2(name='index'):
    return render_template('index.html', name=name, title=pythonFile.count('Aruba'))

@app.route('/send', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        outputter = request.form['website']
        lister = pythonFile.db(outputter)
        return render_template('response.html', website=outputter, title=pythonFile.count('Aruba'), phone=pythonFile.phone(lister), email=pythonFile.emails(lister))
    return render_template('index.html', title=pythonFile.count('Aruba'))
 
if __name__ == "__main__":
    app.run()
