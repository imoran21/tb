from django.shortcuts import render,redirect
from .forms import TutorialName, TutorialLogin, AddTitle, AddHeader, AddRequirement ,DeleteRequirement, AddStep, DeleteStep, AddSubStep, DeleteSubStep, AddCode, DeleteCode, AddImage, DeleteImage
from .models import Tutorial, PubLink
from django.contrib.auth import authenticate, login,logout
from tutorialgen import TutorialConstructor
import pprint
import json

def home(request):
	if request.user.is_authenticated():
		return home_auth(request)
	if request.method == "POST":
		# create a form instance and populate it with data from the request:
		form = TutorialName(request.POST)
		# check whether it's valid:
		if form.is_valid():
			r = form.save()
			if not r:

				return render(request, 'tb/home.html', {'form':form})
			try:
				u = authenticate(username = form.data['name'], password = form.data['password'])
				login(request, u)

				return home_auth(request)
			except: 
				print 'ERROR'
				return redirect(home)
		else:
			return render(request, 'tb/home.html', {'form':form})

			

	else:
		form = TutorialName()
		loginform = TutorialLogin()



		return render(request, 'tb/home.html', {'form':form, 'loginform':loginform})
    

def home_auth(request):


	if not request.user.is_authenticated():
		return redirect(home)
	payload = {}
	if 'message' in request.session:
		message= request.session['message']
		request.session['message'] = False
		payload.update({'message':message})


	tutorial = Tutorial.objects.get(user=request.user)
	publink = PubLink.objects.get(tutorial=tutorial)

	json_raw = tutorial.json_data
	t = TutorialConstructor(content=json_raw)
	json_data = t.printall()
	html_data = t.construct_html()

	number = len(json_raw['requirements']) +1 
	step_count = len(json_raw['steps']) + 1

	initial_title, initial_header = json_raw['title'], json_raw['header']
	steps = ["{}. {}".format(i+1, x['title']) for i, x in enumerate(json_raw['steps'])]


	imagesteps = []
	substeps = []
	codesteps = []
	for i, step in enumerate(json_raw['steps']):
		for v, sub in enumerate(step['sub_steps']):
			substeps.append("{}. {} | {}. {}".format(i+1, step['title'], v+1, sub))
	for i, step in enumerate(json_raw['steps']):
		for v, sub in enumerate(step['code_assets']):
			codesteps.append("{}. {} | {}. {}".format(i+1, step['title'], v+1, sub['code_description']))
	for i, step in enumerate(json_raw['steps']):
		for v, sub in enumerate(step['images']):
			imagesteps.append("{}. {} | {}. {}".format(i+1, step['title'], v+1, sub['image_description']))

	addsubstepForm = AddSubStep(steps = steps)
	deletesubstepForm = DeleteSubStep(steps = substeps)
	deletecodeForm = DeleteCode(steps = codesteps)
	deleteimageForm = DeleteImage(steps = imagesteps)


	addtitleForm = AddTitle(initial = {'title':initial_title} )
	addheaderForm = AddHeader(initial = {'header':initial_header})
	addrequirementForm = AddRequirement(number = number, initial = {'index':number})
	addstepForm = AddStep(step_count = step_count, initial = {'index':step_count})
	addcodeexampleForm = AddCode(steps = steps)
	addimageForm = AddImage(steps = steps)



	deleterequirementForm= DeleteRequirement(choices = map(lambda x: x['requirement'], json_raw['requirements']))
	deletestepForm = DeleteStep(choices =  map(lambda x: x['title'], json_raw['steps']))


	#divide


	

	payload.update({'html_data':html_data, 'json_data':json_data, 'tutorial_name':tutorial.name,'addtitleForm':addtitleForm, 'addheaderForm': addheaderForm})
	payload.update({'addrequirementForm':addrequirementForm})
	payload.update({'deleterequirementForm':deleterequirementForm})
	payload.update({'addstepForm':addstepForm})
	payload.update({'deletestepForm':deletestepForm})
	payload.update({'addsubstepForm':addsubstepForm})
	payload.update({'deletesubstepForm':deletesubstepForm})
	payload.update({'addcodeexampleForm':addcodeexampleForm})
	payload.update({'deletecodeForm':deletecodeForm})
	payload.update({'addimageForm':addimageForm})
	payload.update({'deleteimageForm':deleteimageForm})
	payload.update({'publinkName':publink.name})



	return render(request, 'tb/home_auth.html',payload )


def logout_request(request):
	logout(request)
	return redirect(home)

def login_request(request):
	if request.user.is_authenticated():
		return redirect(home)
	else:
		if request.method == "POST":
			loginform = TutorialLogin(request.POST)
			if loginform.is_valid():
				name, password = loginform.cleaned_data['name'], loginform.cleaned_data['password']
				user = authenticate(username = name, password = password)
				login(request, user)
				return redirect(home)
			
			else:
				form = TutorialName()
				return render(request, 'tb/home.html', {'form':form,'loginform':loginform})
		else:
			return redirect(home)


def change_title(request):
	if request.method == "POST":
		form = AddTitle(request.POST)
		if form.is_valid():
			title= form.data['title']

			tutorial = Tutorial.objects.get(user = request.user)
			tutorial.json_data['title'] = title
			tutorial.save()
			return redirect(home)
		else:	
			request.session['message'] = 'No empty vaues for {}'.format('title field')
			return redirect(home)

def change_header(request):
	if request.method == "POST":
		form = AddHeader(request.POST)
		if form.is_valid():
			header= form.data['header']
			tutorial = Tutorial.objects.get(user = request.user)
			tutorial.json_data['header'] = header
			tutorial.save()
			return redirect(home)
			
		else:	
			print 'failed validation'
			request.session['message'] = 'No empty vaues for {}'.format('header field')
			return redirect(home)
def change_requirement(request):
	if request.method == "POST":
		form = AddRequirement(request.POST, number = int(request.POST.get('index')))
		if form.is_valid():
			requirement= form.data['requirement']
			link = form.data['link']
			index = int(form.data['index'])
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			if index-1 == len(t.content['requirements']):

				t.add_requirement(requirement,link)
			else:
				t.add_requirement(requirement,link, index)
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
			
		else:	
			request.session['message'] = 'No empty vaues for {}'.format('requirement')
			return redirect(home)
def delete_requirement(request):
	if request.method == "POST":
		form = DeleteRequirement(request.POST, choices = (request.POST.get('choices')))
		if form.is_valid():
			choice= form.data['choices']
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			try:
				tutorial.json_data['requirements'] = [x for x in tutorial.json_data['requirements'] if not x['requirement'] == choice]
			except Exception as e:
				print e
				raise ValueError('error in exception block under delete requirement function: \n\t {}'.format(e))
			
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
			
		else:	
			request.session['message'] = 'There was an error deleting your {}'.format('Requirement')
			return redirect(home)
	else:
		return redirect(home)

def add_step(request):
	if request.method == "POST":
		form = AddStep(request.POST, step_count = int(request.POST.get('index')))
		if form.is_valid():
			title= form.data['title']
			description_before= form.data['description_before']
			description_after= form.data['description_after']

			index = int(form.data['index'])
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			if index-1 == len(t.content['steps']):

				t.add_step(\
					title = title,\
					description_before = description_before,\
					description_after = description_after,\

					)
			else:

				t.add_step(\
					title = title,\
					description_before = description_before,\
					description_after = description_after,\
					step_number= index,\
					)
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
			
		else:	
			request.session['message'] = 'No empty vaues for {}'.format('Title')
			return redirect(home)



def delete_step(request):
	if request.method == "POST":
		form = DeleteRequirement(request.POST, choices = (request.POST.get('choices')))
		if form.is_valid():
			choice= form.data['choices']
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			try:
				tutorial.json_data['steps'] = [x for x in tutorial.json_data['steps'] if not x['title'] == choice]
			except Exception as e:
				print e
				raise ValueError('error in exception block under delete step function: \n\t {}'.format(e))
			
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
			
		else:	
			request.session['message'] = 'There was an error deleting your {}'.format('step')
			return redirect(home)
	else:
		return redirect(home)



def add_substep(request):
	if request.method == "POST":
		form = AddSubStep(request.POST, steps = request.POST.get('steps'))
		if form.is_valid():
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			t.add_step_sub_step(int(str(form.data['steps'])[0]), form.data['description'])
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)

		else:
			request.session['message'] = 'There was an adding your {}, please try again'.format('substep')
			return redirect(home)

	else:
		return redirect(home)



def delete_substep(request):
	if request.method == "POST":
		form = DeleteSubStep(request.POST, steps = request.POST.get('steps'))
		if form.is_valid():
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			step_index = int(form.data['steps'][0])
			substep_index = int(form.data['steps'].split(" | ")[1][0])
			del t.content['steps'][step_index-1]['sub_steps'][substep_index-1]
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
		else:
			request.session['message'] = 'There was an deleting your {}, please try again'.format('substep')
			return redirect(home)
	return redirect(home)

def add_code(request):
	if request.method == "POST":
		form = AddCode(request.POST, steps = request.POST.get('steps'))
		if form.is_valid():
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			code_type = form.data['code_type']
			code_lines = form.data['code_lines']
			code_description = form.data['code_description']
			step_number = int(form.data['steps'][0])
			t.add_code_example(step_number, code_description, code_type, code_lines)

			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)

		else:
			request.session['message'] = 'There was an adding your {}, please try again'.format('substep')
			return redirect(home)

	else:
		return redirect(home)

def delete_code(request):
	if request.method == "POST":
		form = DeleteCode(request.POST, steps = request.POST.get('steps'))
		if form.is_valid():
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			step_index = int(form.data['steps'][0])
			substep_index = int(form.data['steps'].split(" | ")[1][0])
			del t.content['steps'][step_index-1]['code_assets'][substep_index-1]
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
		else:
			request.session['message'] = 'There was an deleting your {}, please try again'.format('code')
			return redirect(home)
	return redirect(home)

def add_image(request):
	if request.method == "POST":
		form = AddImage(request.POST, steps = request.POST.get('steps'))
		if form.is_valid():
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			t.add_image(int(form.data['steps'][0]), form.data['image_description'], form.data['image_link'])
			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
		else:
			request.session['message'] = 'There was an adding your {}, please try again'.format('image')
			return redirect(home)
	return redirect(home)



def delete_image(request):
	if request.method == "POST":
		form = DeleteImage(request.POST, steps = request.POST.get('steps'))
		if form.is_valid():
			
			step_index = int(form.data['steps'][0])
			substep_index = int(form.data['steps'].split(" | ")[1][0])
			tutorial = Tutorial.objects.get(user = request.user)
			t = TutorialConstructor(tutorial.json_data)
			del t.content['steps'][step_index-1]['images'][substep_index-1]
			

			tutorial.json_data = t.content
			tutorial.save()
			return redirect(home)
		else:
			request.session['message'] = 'There was an deleting your {}, please try again'.format('code')
			return redirect(home)
	return redirect(home)


def live(request):
	if request.user.is_authenticated():
		payload = {}	
		tutorial = Tutorial.objects.get(user=request.user)
		json_raw = tutorial.json_data
		t = TutorialConstructor(content=json_raw)
		json_data = t.printall()
		html_data = t.construct_html()
		payload.update({'html_data':html_data})
		return render(request, 'tb/live.html',payload)
	else:
		request.session['message'] = 'Please Login to view your tutorial'
		return render(request, 'tb/live.html',payload )




def pub_view(request, name=None):
	print name

	if PubLink.objects.filter(name=name).exists():

		p = PubLink.objects.get(name=name)
		t= TutorialConstructor(p.tutorial.json_data)
		html_data = t.construct_html()
		return render(request, 'tb/live.html', {'html_data':html_data})
	else:
		pass






