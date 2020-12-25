from shutil import copyfile, move, copytree
from collections import OrderedDict
import fileinput, sys
import os, re, json
import itertools


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
# Current TODO List: 1/1/2021
# - Inherit from base - make it work
# - add to header the generic body and footer is exsits
# - check if src/ href is not a url or '#'
# - Improve the "how to use" guide
# - class that have the functions bellow and also have a class-integers (the pathes)
# - Lorem Ipsum instead of p tags
# - - - - - - - - - - - - - - - - -


# - Some Point:
# + The app has been coded to listen on port 5000
# + the generator will build the app.py as templates for you to edit and for saving time,
# + it excpects you to take a look and review the solution.

# + The code ignore generate header.html in app.py, 
# + so that if your template has a file called header.html you need to change here and in json the configuration (local change obviously)

# + App.py accepting POST and GET requests, consider that.
def menue_prints():
	print('$ Yaron-Shamul @ github.com')
	print(u"""
 ___            __          ___  ___        __            ___  ___  __  
|__  |     /\  /__` |__/ __  |  |__   |\/| |__) |     /\   |  |__  |__) 
|    |___ /~~\ .__/ |  \     |  |___  |  | |    |___ /~~\  |  |___ |  \ """)



"""
its a TODO function
here we want recursively rebuild tags if includes text, without touch
urls and important data / functions.
"""
def clean_text_from_tag(tag, line):
	pass 



"""
here it takes the html file and move the head tag to header.html
"""
def header_compress(templates_path):
	head_pattern, title_pattern, diff_head_content = '<head>(.*?)</head>', '<title>(.*?)</title>', ''

	try:
		with open('code_templates.json') as f:
			data = json.load(f)
		decorate_header = list(data.values())[5]
		head_tag = list(data.values())[6]
		 
	except Exception as e:
		print(e)		
		print('Could not open code_templates.json, please try again.')		


	for file_name in os.listdir(templates_path):
		filepath = os.path.join(templates_path, file_name)
		with open(filepath, "r+") as file:
			html_content = file.read()
			file.seek(0)
			header_content = ''.join(re.findall(head_pattern, html_content , flags=re.DOTALL))
			diff_head_content += header_content
			html_content = html_content.replace(header_content, '')
			
			file.write(f'{decorate_header[0]}\n {html_content[48:]}\n {decorate_header[1]}')
			file.truncate()
			file.flush()

	# The lines bellow will magically will take the diff 
	# between all the header tags of the files in the templates folder
	# and puts it inside new file calls header.html
	diff_head_content = diff_head_content.split('\n')
	for head_content in diff_head_content:
		if head_content.lstrip().startswith('<title>') and head_content.endswith('</title>'):
			diff_head_content.remove(head_content)
		
	diff_head_content.append('  <title>FLASK-TEMPLATED-TITLE</title>')

	# The line bellow will remove duplicates by convert the list to dict,
	# than it will convert the list to string and seprete every line with \n
	diff_head_content = '\n'.join(list(dict.fromkeys(diff_head_content)))
	
	try:
		with open(f'{templates_path}/header.html','a+') as header_file:
			header_file.seek(0)
			header_file.write(f'{head_tag[0]} {diff_head_content}\n\n {head_tag[1]}')
			
	except Exception as e:
		print('Could not create header file, please try again.')		
		print(e)



"""
The function will generate app.py file so you can run and check your 
flask-templated project app!
"""
def flask_app_creator(templates_folder):
	with open('code_templates.json') as f:
		data = json.load(f)
	
	html_files = os.listdir(fr'{templates_folder}\templates')
	routing_template = ''

	# each file get a route template
	# data.values())[2] one of the json template elements
	for html_file in html_files: 
		routing_template += list(data.values())[2].format(file_name=html_file[:-5].replace('-', '_'), html_file=html_file)
	
	data_file = list(data.values())
	data_file[2] = routing_template

	# - in case json have nested list we want it to parse
	#   it as well using the line bellow:
	# ''.join(list(itertools.chain.from_iterable(data_file)))
	data_file = ''.join(data_file[:5])
	with open(fr'{templates_folder}\app.py', 'a') as app_py:
		app_py.write(data_file)
	

"""
This function will take care the html to be editable and save you time 
"""	
def html_organize(templates_path):
	for html_file in os.listdir(templates_path):
		for line in fileinput.input([f'{templates_path}\\{html_file}'], inplace=True):

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
	start_param_index = line.find(f'{param}="')					
	if start_param_index >= 0: # param appears in the line
	
		end_param_content = re.findall(f'{param}="(.*?)"', line)[0] 
		end_param_index = len(end_param_content)
		quotation_marks = line[start_param_index + end_param_index + 6:]
		if not quotation_marks.startswith('"'):
			quotation_marks = f'"{quotation_marks}'

		start_tag = line[:start_param_index]
		return f"{start_tag}{param}=\"{{{{ url_for('static', filename='{end_param_content}') }}}}{quotation_marks}"
		

"""
Build the tree structure that familiar with flask project
"""
def restructure(bootstrap_folder):

	flask_templated = f'{bootstrap_folder}FLASK-TEMPLATED'
	try:
		os.mkdir(flask_templated)
		os.mkdir(fr'{flask_templated}\templates')

	except Exception as e:
		print(e)
		
	else:    
		copytree(bootstrap_folder, fr'{flask_templated}\static')
		
		for file_name in os.listdir(fr'{flask_templated}\static'):
			if file_name.endswith('.html') and file_name != 'header.html': # it assumes there is no unusals
				move(f'{flask_templated}\\static\\{file_name}', f'{flask_templated}\\templates\\{file_name}')


"""
Menu and validations for the base-folder
"""
def menue():
	menue_prints()
	try:
		base_folder = input("please enter full path for the base-folder:")
		
		# the base_folder need to be created and the path length need to be at least 5
		validations = [len(base_folder) < 5 ,not os.path.isdir(base_folder), os.path.isdir(fr'{base_folder}FLASK-TEMPLATED\templates')]
		while any(validations):
			validations = [len(base_folder) < 5, not os.path.isdir(base_folder), os.path.isdir(fr'{base_folder}FLASK-TEMPLATED\templates')]
		
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
	# base_folder = menue()
	templates_path = fr'{base_folder}FLASK-TEMPLATED\templates'
	restructure(base_folder)

	html_organize(templates_path)
	header_compress(templates_path)
	flask_app_creator(r'{}FLASK-TEMPLATED'.format(base_folder))
	

if __name__ == '__main__':
	main()


