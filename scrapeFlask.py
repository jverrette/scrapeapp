from flask import Flask, render_template, request
import pythonScrape
app = Flask(__name__)
 
@app.route('/<name>')
def initial(name='index'):
    return render_template('scrapeAdaptation.php', name=name)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        website = request.form['website']
        information = pythonScrape.main(website)
        return render_template('scrapeAdaptation.php', website=website, information =information)
    return render_template('scrapeAdaptation.php', website='', information ={})
 
if __name__ == "__main__":
    app.run()

