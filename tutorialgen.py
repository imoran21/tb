

import pprint

MANUAL_TEMPLATE =  {
	"title": "",
	"header": "",
	"warning": "Please make sure you have the following setup before starting",
	"requirements":[],
	"setup":
		{ 
			"javascript_links": '''
				    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha512-K1qjQ+NcF2TYO/eI3M6v8EiNYZfA95pQumfvcVrTHtwQVDG+aHRqLi/ETn2uB+1JqwYqVG3LIvdm9lj6imS/pQ==" crossorigin="anonymous"></script>
				    <script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js" async></script>"''',
			"bootstrap_cdn":
				'''
					<!-- Latest compiled and minified CSS -->
					<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">
					
					<!-- Optional theme -->
					<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-aUGj/X2zp5rLCbBxumKTCw2Z50WgIr1vs/PFN4praOTvYXWlVyh2UtNUU0KAUhAX" crossorigin="anonymous">
				'''
		 },
	"end_result_image": {},
	"steps":[],
}	



class TutorialConstructor(object):


	def __init__(self, content = MANUAL_TEMPLATE):
		self.content = content

	def template_skeleton(self):
		self.content['title'] = "Your Title"
		self.content['header'] = "This will be your Tutorial mission statement"
		self.content['requirements'] = []
		self.content["steps"] = []
		self.content['end_result_image'] = {}

		return self.content

	def add_string_attribute(self, attribute, content):
		if not attribute in ['title', 'header', 'warning']:
			raise ValueError('Can only accept unicode or string types into title, header, warning elements of page')
		self.string_validator([content])
		self.content[attribute] = content

	def add_end_result(self, description, link):
		self.string_validator([description])
		
		self.content['end_result_image']['end_result_image_description'] = description
		self.content['end_result_image']['end_result_image_link'] = link
					
	def add_step(self, title, description_before="", description_after="", step_number= False):
		self.string_validator([title, description_before, description_after])


		if not step_number:
			self.content['steps'].append(\
				{
					"title": title,
					"description_before": description_before,
					'sub_steps': [],
					"description_after": description_after,
					"code_assets":[],
					"images": [],
					'tables': [],
				})
		if step_number:
			step_number = step_number -1 
			self.step_number_validator(step_number)
			self.content['steps'].insert(step_number,
				{
					"title": title,
					"description_before": description_before,
					'sub_steps': [],
					"description_after": description_after,
					"code_assets":[],
					"images": [],
					'tables': [],
				})
			
	def add_step_sub_step(self, step_number, description, index= False):

		step_number = step_number -1
		self.step_number_validator(step_number)
		self.string_validator([description])
		if not index:
			self.content['steps'][step_number]['sub_steps'].append(description)
		else:
			if index > len(self.content['steps'][step_number]['sub_steps']):
				raise ValueError('substep index does not exist')
			else:
				self.content['steps'][step_number]['sub_steps'].insert(index-1,description)


	def printall(self):
		pp = pprint.PrettyPrinter(depth=8)
		return pprint.pformat(self.content)

	def add_code_example(self, step_number, code_description, code_type, code_lines, index= False):
		step_number = step_number-1
		self.string_validator([code_description, code_type, code_lines])

		if index and index> len(self.content['steps'][step_number]['code_assets']):
			raise ValueError('code index does not exist')

		if not index:
			self.content['steps'][step_number]['code_assets'].append(
				{
					'code_description': code_description,
					'code_type':code_type,
					'code_lines': code_lines

				})
		else:
			self.content['steps'][step_number]['code_assets'].insert(index-1, 
				{
					'code_description': code_description,
					'code_type':code_type,
					'code_lines': code_lines

				})

	def add_image(self, step_number, image_description, image_link, index=False):
	
		self.step_number_validator(step_number)
		step_number= step_number-1
		self.string_validator([image_description, image_link])
		if index and index> len(self.content['steps'][step_number]['images']):
			raise ValueError('image index does not exist')
		if not index:
			self.content['steps'][step_number]['images'].append(
				{'image_description':image_description, 'image_link': image_link})
		elif index:
			index = index-1
			self.content['steps'][step_number]['images'].insert(index, 
				{'image_description':image_description, 'image_link': image_link})

	def add_table(self, step_number, table_title, table_headers, table_rows, index = False):
		self.list_validator([table_headers, table_rows])
		self.step_number_validator(step_number)
		step_number = step_number -1		
		self.string_validator(table_title)

		if index and index > len(self.content['steps'][step_number]['tables']):
			raise ValueError('table index does not exist')

		if not index:
			self.content['steps'][step_number]['tables'].append(
				{
					'table_title': table_title,
					'table_headers': table_headers,
					'table_rows': table_rows
				})
		elif index:
			index = index -1
			self.content['steps'][step_number]['tables'].insert(index,
				{
					'table_title': table_title,
					'table_headers': table_headers,
					'table_rows': table_rows

				})

	def add_requirement(self, requirement, link = "#", index= False):
		self.string_validator([requirement, link])
		if index:
			if index > len(self.content['requirements']):
				raise ValueError('The requirement index you want to insert at does not exist')
			else:
				index = index-1
				self.content['requirements'].insert(index, {'requirement':requirement, 'link':link})
		else:
			self.content['requirements'].append( {'requirement':requirement, 'link':link})

	def step_number_validator(self, step_number):
		if step_number > len(self.content['steps']):
			raise ValueError('The step you are trying to edit does not exist at the index specified')

	def string_validator(self, strings):
		if not all(map (lambda x: isinstance(x,(str,unicode)), strings)):
			raise ValueError('Can only accept unicode or string types into the element')

	def list_validator(self, lists):
		if not all(map (lambda x: isinstance(x, (list)), lists)):
			raise ValueError('can only enter list into the element')

	def construct_overview_html(self):
		payload = ''' 
				<div class="container" id="headdingsection">
				  <div class ="row">
				    <div class="col-md-7 col-lg-6 col-sm-7">	        
				     
				      <h3>  Overview of steps: </h3>
				
				      <ul class="list-group" >
			'''
		steps = [x['title'] for x in self.content['steps']]
		for i, step in enumerate(steps):
			payload+='''
						  <li class="list-group-item">
    						<span class="label label-default label-pill pull-right">{}</span>
						    {}
						  </li>
					'''.format(i+1,step)


		payload += '''
					</ul>
     

				    </div>


			'''
		return payload

	def construct_step_html(self, step, number):
		payload = '''
		<div class ="container"><div class="row">
		  <br /><br />
		  <div class="panel panel-default">
		    <div class="panel-heading">{}.  {}</div>
		      <div class="panel-body">



		      <div class ="col-md-8 col-lg-8 col-sm-10">
		        <p class = "description_before"> {}</p>
		        <ol class = "sub_steps">
		        
		'''.format(number, step['title'], str(step['description_before']))
		for x in step['sub_steps']:
			payload+='''
			        <li> {}</li>
			        '''.format(x)
		payload += '''

		         </ol>  
		            <p class= "description_after"> {}  <br><br></p>
		      </div>'''.format(step['description_after'])
		for asset in step['code_assets']:
			payload += '''
			
			  <div class="col-md-8 col-lg-6 col-sm-12">
			  <hr>
			      <h5 class= "code_description"> {}</h5>
			      <pre style = "font-size:10px;" class="prettyprint linenums lang-{}">
			      <script style = "display:block;" type="text/plain">
{}

				</script>
					</pre>
			  </div>'''.format(asset['code_description'], asset['code_type'],asset['code_lines'])


		for image in step['images']:

			payload += '''

			   <div class ="col-md-8 col-lg-6 col-sm-10">
			   <hr>
		          <h5> {}</h5>
		          <img class = "img-responsive img-thumbnail" src="{}" alt="" />
		       </div>

			'''.format(image['image_description'], image['image_link'])


		for table in step['tables']:
			payload += '''
			<div class = "col-md-8 col-lg-6 col-sm-10">
			<hr>
			<h5>{}</h5>   
				
				        
				  <table class="table table-bordered table-condensed">
				  <thead>
				      <tr>

			'''.format(table['table_title'])
			for header in table['table_headers']:
				payload += '''
				        <th>{}</th>
				        '''.format(header)
		

			payload += '''
			   		 </tr>
			   
				    </thead>
				    <tbody>
				    '''
			for row in table['table_rows']:
				payload += '''
						<tr>'''

				for i in row:
					payload += "<td>{}</td>".format(i)
				payload += '''
						</tr>'''


			payload += '''
				    </tbody>
				  </table>

			</div>
			'''

		payload += '''
		    	 </div>
			 	</div>
			        
			  </div>
			</div><hr>'''
		return payload

	def construct_requirements_html(self):
		payload = '''
				        <div class = "col-md-4 col-sm-4 col-lg-4">

					       <div class="requirements">
					          <div class="alert alert-warning">
					            <p>Before starting this tutorial, please ensure you have the following:  </p>
					          </div>
					            <a href="#" class="list-group-item active">
					                  REQUIREMENTS 
					            </a>
			    '''

		for dic in self.content['requirements']:
			k = dic['requirement']
			v = dic['link']

			payload += '''
			              		 <a href="{}" class="list-group-item">{}</a>
	          			'''.format(v,k)
		payload += '''
							  </div>
							</div>
				        </div>
				    </div>
				    <hr>
			
					    '''
		return payload

	def aggregate_steps_html(self):
		payload = ""
		for i, step in enumerate(self.content['steps']):
			payload+= self.construct_step_html(step, i+1)
		return payload

	def construct_html(self):
		doc_start = '''
			<!DOCTYPE html>
			<html>
			'''
		doc_head_start = ''' 
				<head>
				'''
		doc_head_end = ''' 
				</head>

				<body>

				'''
		doc_head_tag = \
			doc_head_start + \
				self.content['setup']['javascript_links'] + \
				self.content['setup']['bootstrap_cdn'] +  \
			doc_head_end
		doc_end = '''
				</body>

				</html>

				'''

		doc_title = '''
					<div class="container">
					   <div class ="row">
					      <div class = "col-md-6 col-lg-6 col-sm-9 col-xs-9">
					        <h1 class= "page-header">{}</h1>
					    </div>
					  </div>
					</div>
			'''.format(self.content['title'])

		doc_header = '''
					<div class="container">
					   <div class ="row">
					      <div class = "col-md-8 col-lg-8 col-sm-9 col-xs-9">
					       <p>
					          {}
					      <p>
					      <hr> 
					    </div>
					  </div>
					</div>
					'''.format(self.content['header'])
		if self.content['end_result_image']:	
			doc_end_result_preview = '''
					<div class="container">
					   <div class ="row">
					      <div class = "col-md-7 col-lg-6 col-sm-10 col-xs-10">
					       <h3>  Preview of end result: </h3>
					                  <h4> {}</h4>
					        <img class = "img-responsive img-thumbnail" src="{}" alt="" />
					        <br /><br />
					    </div>
					  </div>
					</div>
					'''.format(\
							self.content['end_result_image']['end_result_image_description'], \
							self.content['end_result_image']['end_result_image_link']\
							)
		else:
			doc_end_result_preview =""
		TEMPLATE =  \
			doc_start + \
				doc_head_tag + \
				doc_title+ \
				doc_header+ \
				self.construct_overview_html()+\
				self.construct_requirements_html()+\
				self.aggregate_steps_html()+\
				doc_end_result_preview+\
			doc_end
		return TEMPLATE

