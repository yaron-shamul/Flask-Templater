from shutil import copyfile, move, copytree
import os


def restructure():

	bootstrap_folder = r'C:\Users\Yaron Shamul\Desktop\iPortfolio'
	flask_templated = '{}FLASK-TEMPLATED'.format(bootstrap_folder)
	
	try:
	    os.mkdir(flask_templated)
	    os.mkdir(r'{}\templates'.format(flask_templated))

	except Exception as e:
	    print(e)
	    
	else:    

		copytree(bootstrap_folder, r'{}\static'.format(flask_templated))

		for file_name in os.listdir(r'{}\static'.format(flask_templated)):
			if file_name.endswith('.html'):
				move(r'{}\static\{}'.format(flask_templated, file_name), r'{}\templates\{}'.format(flask_templated, file_name))
				
