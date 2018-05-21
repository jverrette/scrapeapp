from flask import Flask, render_template, request
import pythonScrape
app = Flask(__name__)
 
@app.route('/<name>')
def initial(name='index'):
    return render_template('index.html', name=name)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        website = request.form['website']
        information = pythonScrape.main(website)
        return render_template('response.html', website=website, information =information)
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run()

