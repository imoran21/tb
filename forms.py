from django import forms
from captcha.fields import ReCaptchaField
from .models import Tutorial, User, PubLink
from django.contrib.auth import authenticate, login,logout
class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(attrs={'theme':'clean'})




class TutorialName(FormWithCaptcha):
    name = forms.CharField(label='Your Tutorial Name', max_length=100, \
    	widget=forms.TextInput(attrs ={'placeholder':'Tutorial Name', 'class':'form-control'}))
    password = forms.CharField(label='Your Tutorial password', max_length=40, \
    	widget=forms.TextInput(attrs ={'placeholder':'Password', 'class':'form-control', 'type':"password"}))
    password2 = forms.CharField(label='Your Tutorial password', max_length=40, \
    	widget=forms.TextInput(attrs ={'placeholder':'Password', 'class':'form-control', 'type':"password"}))
    def is_valid(self):
		name = self.data['name']
		password = self.data['password']
		password2 = self.data['password2']
		valid = super(TutorialName, self).is_valid()
		if not valid:
			return valid
		elif len(password) < 6:
			self._errors['Password Error: '] = "Password must be 6 characters or more"
			return False
		elif password2 != password:
			self._errors['Password Error: '] = "Passwords do not match"
			return False

		elif Tutorial.objects.filter(name=name).exists():
			self._errors['Tutorial Name Exists: '] = "This tutorial name already exists, please choose another"
			return False

		else:
			return True
    def save(self):
    	try:

    		u = User.objects.create_user(username= self.data['name'], email= "{}@tb.com".format(self.data['name']), password=self.data['password'])
    		u.save()

    		us = User.objects.get(username=self.data['name'])
    		t = Tutorial(name = self.data['name'], password = self.data['password'], user = us)
    		t.save()

    		tu = Tutorial.objects.get(name=self.data['name'])
    		link_name = "".join([x for x in self.data['name'] if x.lower() in 'abcdefghijklmnopqrstuvwxyz'])
    		p = PubLink(name=link_name, tutorial=tu)
    		p.save()
    		return True

    	except Exception as e:
    		print e
    		self._errors['Error saving the data: '] = "{}".format(e)
    		return False


class TutorialLogin(forms.Form):
	name = forms.CharField(label='Your Tutorial Name', max_length=100, \
    	widget=forms.TextInput(attrs ={'placeholder':'Tutorial Name', 'class':'form-control'}))
	password = forms.CharField(label='Your Tutorial password', max_length=40, \
    	widget=forms.TextInput(attrs ={'placeholder':'Password', 'class':'form-control', 'type':"password"}))
	def is_valid(self):
		name, password = self.data['name'], self.data['password']
		valid = super(TutorialLogin, self).is_valid()
		if not valid:
			return valid
		if not name or not password:
			self._errors['Password/TutorialName Error: '] = "Tutorial name and password fields must have values"
			return False
		user = authenticate(username = name, password = password)
		if user is not None:
			return True
		else:
			self._errors['Username Does not exist'] = "Click Create tutorial to make a new one"
			return False

		return False

class AddTitle(forms.Form):
	title = forms.CharField(label='Your Tutorial Title', max_length=150, \
    	widget=forms.TextInput(attrs ={'placeholder':'Tutorial Title', 'class':'form-control'}))

	def is_valid(self):
		valid = super(AddTitle, self).is_valid()
		if not valid:
			self._errors['Title Error: '] = "Value can not be blank"
			return valid
		if self.data['title']:
			return True
		else:
			return False


class AddHeader(forms.Form):
	header = forms.CharField(label='Your Tutorial Header', max_length=150, \
    	widget=forms.Textarea(attrs ={"cols":33,"rows":3, "placeholder":'Tutorial Header', 'class':'form-control'}))

	def is_valid(self):
		valid = super(AddHeader, self).is_valid()
		if not valid:
			self._errors['Header Error: '] = "Value can not be blank"
			return valid
		if self.data['header']:
			return True
		else:
			self._errors['Header Error: '] = "Value can not be blank"
			return False


class AddRequirement(forms.Form):
	def __init__(self,*args,**kwargs):
		self.number = kwargs.pop('number')
		super(AddRequirement,self).__init__(*args,**kwargs)
		self.fields['index'] = forms.ChoiceField(choices=[(x, x) for x in range(1, self.number+1)], widget=forms.Select(attrs={"class":"form-control"}))
	requirement = forms.CharField(label='Tutorial Requirement', max_length=50, \
    	widget=forms.TextInput(attrs ={"placeholder":'Add Requirement', 'class':'form-control'}))


	link = forms.CharField(required=False, label='Your Tutorial Header', max_length=100, \
    	widget=forms.TextInput(attrs ={"blank":True, "placeholder":'Reference Link <Optional>', 'class':'form-control'}))

	index =  None

	def is_valid(self):

		valid = super(AddRequirement, self).is_valid()
		if not valid:
	
			return valid
		elif self.data['requirement']:
			return True
		else:

			return False


class DeleteRequirement(forms.Form):
	def __init__(self,*args,**kwargs):
		self.choices = kwargs.pop('choices')
		super(DeleteRequirement,self).__init__(*args,**kwargs)
		if self.choices:
			self.fields['choices'] = forms.ChoiceField(choices=[(x, x) for x in self.choices], widget=forms.Select(attrs={"class":"form-control"}))
	choices =  False
	def is_valid(self):
		if self.data['choices']:
			return True
		else:

			return False



class AddStep(forms.Form):
	def __init__(self,*args,**kwargs):
		self.step_count = kwargs.pop('step_count')
		super(AddStep,self).__init__(*args,**kwargs)
		self.fields['index'] = forms.ChoiceField(choices=[(x, x) for x in range(1, self.step_count+1)], widget=forms.Select(attrs={"class":"form-control"}))
	title = forms.CharField(label='Step Title', max_length=100, \
    	widget=forms.Textarea(attrs ={"cols":33,"rows":2, "placeholder":'Add a step title', 'class':'form-control'}))
	description_before = forms.CharField(label='Beginning Text', max_length=500, \
    	widget=forms.Textarea(attrs ={'blank':True, "cols":45,"rows":4, "placeholder":'<Optional> Describe the summary of this step', 'class':'form-control'}))
	description_after = forms.CharField(label='End Text', max_length=500, \
    	widget=forms.Textarea(attrs ={'blank':True, "cols":45,"rows":4, "placeholder":'<Optional> Describe the conclusion of this step', 'class':'form-control'}))
	index = None
	def is_valid(self):
		if not self.data['title']:
			return False
		else:
			return True

class DeleteStep(forms.Form):
	def __init__(self,*args,**kwargs):
		self.choices = kwargs.pop('choices')
		super(DeleteStep,self).__init__(*args,**kwargs)
		if self.choices:
			self.fields['choices'] = forms.ChoiceField(choices=[(x, x) for x in self.choices], widget=forms.Select(attrs={"class":"form-control"}))
	choices =  False

	def is_valid(self):
		if self.data['choices']:
			return True
		else:
			return False


class AddSubStep(forms.Form):
	def __init__(self,*args,**kwargs):
		self.steps = kwargs.pop('steps')
		if len(self.steps) == 0:
			self.valid = False
		else:
			self.valid = True
		super(AddSubStep,self).__init__(*args,**kwargs)
		self.fields['valid'] = self.valid

		self.fields['steps'] = forms.ChoiceField(choices=[(x, x) for x in self.steps], widget=forms.Select(attrs={"class":"form-control"}))
		
	description= forms.CharField(label='Substep Description', max_length=200, \
    	widget=forms.Textarea(attrs ={'blank':False, "cols":45,"rows":4, "placeholder": "Add a substep", 'class':'form-control'}))
	
	steps = None
	def is_valid(self):
		if not self.data['description'] or not self.data['steps']:
			return False
		else:
			return True



class DeleteSubStep(forms.Form):
	def __init__(self,*args,**kwargs):
		self.steps = kwargs.pop('steps')
		if len(self.steps) == 0:
			self.valid = False
		else:
			self.valid = True
		super(DeleteSubStep,self).__init__(*args,**kwargs)
		self.fields['valid'] = self.valid
		self.fields['steps'] = forms.ChoiceField(choices=[(x, x) for x in self.steps], widget=forms.Select(attrs={"class":"form-control"}))

	steps = None
	def is_valid(self):
		if not self.data['steps']:
			return False
		else:
			return True


class AddCode(forms.Form):
	def __init__(self,*args,**kwargs):
		self.steps = kwargs.pop('steps')
		if len(self.steps) == 0:
			self.valid = False
		else:
			self.valid = True
		super(AddCode,self).__init__(*args,**kwargs)
		self.fields['valid'] = self.valid

		self.fields['steps'] = forms.ChoiceField(choices=[(x, x) for x in self.steps], widget=forms.Select(attrs={"class":"form-control"}))
	code_choices = ["bsh", "c", "cc", "cpp", "cs", "csh", "cyc", "cv", "htm", "html", "java", "js", "m", "mxml", "perl", "pl", "pm", "py", "rb", "sh", "xhtml", "xml", "xsl"]
	code_description= forms.CharField(label='Substep Description', max_length=100, \
    	widget=forms.Textarea(attrs ={'blank':False, "cols":45,"rows":2, "placeholder": "Code Description", 'class':'form-control'}))
	code_lines =  forms.CharField(label='Substep Description', max_length=1000, \
    	widget=forms.Textarea(attrs ={'blank':False, "cols":45,"rows":8, "placeholder": "Enter code here", 'class':'form-control'}))
	code_type = forms.ChoiceField(choices=[(x, x) for x in code_choices], widget=forms.Select(attrs={"class":"form-control"}))
	
	steps = None
	def is_valid(self):
		if not self.data['code_description'] or not self.data['steps'] or not self.data['code_lines']:
			return False
		else:
			return True



class DeleteCode(forms.Form):
	def __init__(self,*args,**kwargs):
		self.steps = kwargs.pop('steps')
		if len(self.steps) == 0:
			self.valid = False
		else:
			self.valid = True
		super(DeleteCode,self).__init__(*args,**kwargs)
		self.fields['valid'] = self.valid
		self.fields['steps'] = forms.ChoiceField(choices=[(x, x) for x in self.steps], widget=forms.Select(attrs={"class":"form-control"}))

	steps = None
	def is_valid(self):
		if not self.data['steps']:
			return False
		else:
			return True

class AddImage(forms.Form):
	def __init__(self,*args,**kwargs):
		self.steps = kwargs.pop('steps')
		if len(self.steps) == 0:
			self.valid = False
		else:
			self.valid = True
		super(AddImage,self).__init__(*args,**kwargs)
		self.fields['valid'] = self.valid
		self.fields['steps'] = forms.ChoiceField(choices=[(x, x) for x in self.steps], widget=forms.Select(attrs={"class":"form-control"}))


	

	image_description= forms.CharField(label='Image Description', max_length=300, \
    	widget=forms.Textarea(attrs ={'blank':False, "cols":45,"rows":3, "placeholder": "Image Description", 'class':'form-control'}))
	image_link =  forms.CharField(label='Image Link', max_length=200, \
    	widget=forms.TextInput(attrs ={'blank':False, "placeholder": "Enter link to image", 'class':'form-control'}))
	
	
	steps = None
	def is_valid(self):
		if not self.data['image_link'] or not self.data['image_description']:
			return False
		else:
			return True


class DeleteImage(forms.Form):
	def __init__(self,*args,**kwargs):
		self.steps = kwargs.pop('steps')
		if len(self.steps) == 0:
			print 'false coun'
			self.valid = False
		else:
			self.valid = True
		super(DeleteImage,self).__init__(*args,**kwargs)
		self.fields['valid'] = self.valid
		self.fields['steps'] = forms.ChoiceField(choices=[(x, x) for x in self.steps], widget=forms.Select(attrs={"class":"form-control"}))

	steps = None
	def is_valid(self):
		if not self.data['steps']:
			return False
		else:
			return True



