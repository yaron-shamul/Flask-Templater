from flask import Flask, render_template
import logging, os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY



@app.route('/demo', methods=['GET', 'POST'])
def demo():
	# if requests post
	# db rendering
	return render_template('demo.html')


@app.route('/TEMPLATE_ROUTER_FOR_map_at_specified_location', methods=['GET', 'POST'])
def TEMPLATE_ROUTER_FOR_map_at_specified_location():
	return render_template('TEMPLATE-ROUTER-FOR-map-at-specified-location.html')


@app.errorhandler(404)
def not_found_error(error):
	return '<h1>404 error</h1>'


@app.errorhandler(500)
def internal_error(error):
	return '<h1>500 error</h1>'



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
	#logging.basicConfig(filename='logfile.log', level=logging.DEBUG)