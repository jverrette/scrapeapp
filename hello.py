from flask import Flask, render_template
import pythonFile

app = Flask(__name__)
 
@app.route('/<name>')
def hello(name='index'):
    return render_template('index.html', name=name, title=pythonFile.sqrt(1))
 
if __name__ == "__main__":
    app.run()
