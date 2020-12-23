from shutil import copyfile, move, copytree
import fileinput, sys
import os, re, json


# Yaron-Shamul @ github.com

# - - - - - The idea - - - - - - - 
# Hello Every one who watch this tool, I want to build something that will
# make it easier to build and use html-templates with Flask. 
# And so then I attched the template here to the project.
# I need everything to be automated and clean.. Lets do it :)
# - - - - - - - - - - - - - - - - -


# - - - - - An amzing websites that offers bootstrap / web templates - - - - - -
# https://startbootstrap.com/themes
# https://colorlib.com/wp/template/philosophy/
# https://themewagon.com/thank-you-for-downloading/?item_id=86980&dl=VDQ3OU4rUldFbDZ6ajBzOVBJVnVobzM2STJsaVZPNUpIcGVING5FQ3N0L05hN0xIQnoyWFhkOFpDb3BVNmEwTw==
# - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - -
# Current TODO List: 2/12/2020
#(not a url or '#')
# - Improve the "how to use" guide
# - class that have the functions bellow and also have a class-integers (the pathes)
# - Lorem Ipsum instead of p tags
# - - - - - - - - - - - - - - - - -



"""
its a TODO function
here we want recursively rebuild tags if includes text, without touch
urls and important data / functions.
"""
def clean_text_from_tag(tag, line):
	pass 


def header_compress(templates_path):
	from collections import OrderedDict
	start_decorate = """{% extends 'main/header.html' %}

{% block content %}\n\n"""
	end_decorate = """{% endblock %}"""
	pattern = r"<head>(.*?)</head>"

	diff_head_content = ""
	for file_name in os.listdir(templates_path):
		filepath = os.path.join(templates_path, file_name)
		with open(filepath, "r+") as file:
			html_content = file.read()
			file.seek(0)
	

			header_content = ''.join(re.findall(pattern, html_content , flags=re.DOTALL))
			diff_head_content += header_content
			html_content = html_content.replace(header_content, '')
			
			file.write(start_decorate + html_content[48:] + end_decorate)
			file.truncate()
			file.flush()

	# The line bellow will magically will take the diff 
	# between all the header tags of the files in the templates folder
	# and puts it inside new file calls header.html
	header_content = """<head>\n
	{% load static %}\n""", """</head>\n\n"""
	diff_head_content = '\n'.join(list(OrderedDict.fromkeys(diff_head_content.split('\n')).keys()))
	try:
		with open(f'{templates_path}/header.html','a+') as header_file:
			header_file.seek(0)
			header_file.write(f'{header_content[0]} {diff_head_content}\n\n {header_content[1]}')
			
	except Exception as e:
		print('Could not create header file, please try again.')		
		print(e)




def menue_prints():
	print('$ Yaron-Shamul @ github.com')
	print(u"""
 ___            __          ___  ___        __            ___  ___  __  
|__  |     /\  /__` |__/ __  |  |__   |\/| |__) |     /\   |  |__  |__) 
|    |___ /~~\ .__/ |  \     |  |___  |  | |    |___ /~~\  |  |___ |  \ """)



"""
The function will generate app.py file so you can run and check your 
flask-templated project app!
"""
def flask_app_creator(templates_folder):
	with open('code_templates.json') as f:
		data = json.load(f)
	
	html_files = os.listdir(r'{}\templates'.format(templates_folder))
	routing_template = ''

	#each file get a route template
	for html_file in html_files: 
		routing_template += list(data.values())[2].format(file_name=html_file[:-5].replace('-', '_'), html_file=html_file)
	
	data_file = list(data.values())
	data_file[2] = routing_template
	data_file = ''.join(data_file)
	with open(r'{}\app.py'.format(templates_folder), 'a') as app_py:
		app_py.write(data_file)
	

"""
This function will take care the html to be editable and save you time 
"""	
def html_organize(templates_path):
	for html_file in os.listdir(templates_path):
		for line in fileinput.input([r'{}\{}'.format(templates_path, html_file)], inplace=True):

			sspi = (line.find('src="'), line.find('href="'))
			if new_line := edit_line(line, "src"):
				line = line.replace(line, new_line)
			elif new_line := edit_line(line, "href"): # we assume there is no place where two params used
				line = line.replace(line, new_line)
					
			sys.stdout.write(line)			


"""
This one will generically handle the rendering and templating html line by it's param.
"""
def edit_line(line, param):
	start_param_index = line.find('{}="'.format(param))					
	if start_param_index >= 0: # param appears in the line
	
		end_param_content = re.findall('{}="(.*?)"'.format(param), line)[0] 
		end_param_index = len(end_param_content)
		quotation_marks = line[start_param_index + end_param_index + 6:]
		if not quotation_marks.startswith('"'):
			quotation_marks = '"{}'.format(quotation_marks)

		start_tag = line[:start_param_index]
		return f"{start_tag}{param}=\"{{{{ url_for('static', filename='{end_param_content}') }}}}{quotation_marks}"
		

"""
Build the tree structure that familiar with flask project
"""
def restructure(bootstrap_folder):

	flask_templated = '{}FLASK-TEMPLATED'.format(bootstrap_folder)	
	try:
		os.mkdir(flask_templated)
		os.mkdir(r'{}\templates'.format(flask_templated))

	except Exception as e:
		print(e)
		
	else:    
		copytree(bootstrap_folder, r'{}\static'.format(flask_templated))
		
		for file_name in os.listdir(r'{}\static'.format(flask_templated)):
			if file_name.endswith('.html'): # we can assume there is no unusals
				move(r'{}\static\{}'.format(flask_templated, file_name), r'{}\templates\{}'.format(flask_templated, file_name))


"""
Menu and validations for the base-folder
"""
def menue():
	menue_prints()
	try:
		base_folder = input("please enter full path for the base-folder:")
		
		# the base_folder need to be created and the path length need to be at least 5
		validations = [len(base_folder) < 5 ,not os.path.isdir(base_folder), os.path.isdir(r'{}FLASK-TEMPLATED\templates'.format(base_folder))]
		while any(validations):
			validations = [len(base_folder) < 5, not os.path.isdir(base_folder), os.path.isdir(r'{}FLASK-TEMPLATED\templates'.format(base_folder))]
		
			if validations[0]:
				print("Something is wrong with the length!")
			elif validations[1]:
				print("There is alredy a base-folder!")
			elif validations[2]:
				print("There is alredy a flask_templated-folder!")
			if any(validations):
				base_folder = input("Please enter again full path for the base-folder:")

		return base_folder
	except Exception as e:
		print(e)


"""
- The fllow will defined here
"""
def main():

	base_folder = r'C:\Users\Yaron Shamul\Documents\GitHub\Flask-Templater\iPortfolio'  
	#base_folder = menue()
	templates_path = r'{}FLASK-TEMPLATED\templates'.format(base_folder)
	restructure(base_folder)

	html_organize(templates_path)
	header_compress(templates_path)
	#flask_app_creator(r'{}FLASK-TEMPLATED'.format(base_folder))
	

if __name__ == '__main__':
	main()


