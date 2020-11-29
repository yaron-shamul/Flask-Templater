from shutil import copyfile, move, copytree
import os


# Hello Every one who watch this tool, I want to build something that will
# make it easier to build and use html-templates with Flask. 
# And so then I attched the template here to the project.
# I need everything to be automated and clean.. Lets do it :)

# Current TODO List: 29/11/2020
# add html links edit (inside html files)
# generate a file that routes the pages
# create some "how to use" guide


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
				
