from flask import Flask, render_template, request
import pythonFile

app = Flask(__name__)
 
@app.route('/<name>')
def hello2(name='index'):
    return render_template('index.html', name=name)

@app.route('/send', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        website = request.form['website']
        information = pythonFile.main(website)
        return render_template('response.html', website=website, information =information)
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run()

