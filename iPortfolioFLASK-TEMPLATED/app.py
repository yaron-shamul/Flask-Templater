from flask import Flask, render_template
import logging, os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY



@app.route('/header', methods=['GET', 'POST'])
def header():
	return render_template('header.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/inner_page', methods=['GET', 'POST'])
def inner_page():
	return render_template('inner-page.html')


@app.route('/portfolio_details', methods=['GET', 'POST'])
def portfolio_details():
	return render_template('portfolio-details.html')


@app.errorhandler(404)
def not_found_error(error):
	return '<h1>404 error</h1>'


@app.errorhandler(500)
def internal_error(error):
	return '<h1>500 error</h1>'



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
	#logging.basicConfig(filename='logfile.log', level=logging.DEBUG)