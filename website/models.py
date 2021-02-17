from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.utils import timezone as dj_timezone 
from model_utils import Choices 

class User(AbstractUser):
	# Give us scope to do some fancy user things later
    pass


## FEATURED ITEMS ##
class BaseModel(models.Model):
	title = models.CharField(max_length=150)
	body_text = models.TextField(null=True,blank=True, help_text="You can use Markdown here for rich text.")
	order = models.IntegerField(default=1)
	featured = models.BooleanField(default=False)

	def has_image(self):
		# self.image returns True as it has a File reference 
		if not self.image:
			return False 
		else:
			return True 
	has_image.boolean = True 

	class Meta:
		abstract = True 

class ReasonsToChoose(BaseModel):
	class Meta:
		verbose_name = 'Reasons to Choose'
		verbose_name_plural = verbose_name

	category_choices = Choices('research','clinical')
	category = models.CharField(choices=category_choices, default=category_choices.clinical,max_length=10)

	def __str__(self):
		return self.title 

class CaseStudy(BaseModel):
	class Meta:
		verbose_name_plural = "Case Studies"

	slug = models.SlugField()

	lead_text = models.CharField(blank=True,null=True, max_length=300)
	list_text = models.CharField(blank=True,null=True,max_length=300,
		help_text="If you want something other than the lead text to appear in the Case Study list, put that here.")
	image = models.ImageField(blank=True,null=True)

	def save(self, *args, **kwargs):
		if not self.pk or not self.slug:
			self.slug = slugify(self.title)
		super(CaseStudy, self).save(*args, **kwargs)

	def full_slug(self):
		return '/case-studies/' + self.slug

	def prefix_name(self):
		return 'Case Study: ' + self.title 

	def __str__(self):
		return self.title 

class ProductType(models.Model):
	class Meta:
		ordering = ['name']

	name = models.CharField(max_length=50)
	slug = models.SlugField()
	grid_list = models.BooleanField(default=False,help_text="Use a grid list at the top of the product list page")

	def get_products(self):
		return Product.objects.filter(product_type=self)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = slugify(self.name)
		super(ProductType, self).save(*args, **kwargs)

	def __str__(self):
		return self.name 


class Product(BaseModel):
	class Meta:
		ordering = ['product_type','order','title']

	product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

	image = models.ImageField(blank=True,null=True)

	def __str__(self):
		return self.title + ' (' + str(self.product_type) + ')'

	def slug(self):
		return slugify(self.title)

	def full_slug(self):
		# Ensure that urls.py matches this
		base = self.product_type.slug 
		product = self.slug() 
		return '/' + str(base) + '#' + str(product)

	def prefix_name(self):
		return 'Solution: ' + self.title

	def get_components(self):
		return Component.objects.filter(product_link=self)

	def component_count(self):
		return self.get_components().count() 

class Component(BaseModel):
	image = models.ImageField(blank=True,null=True)
	product_link = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.title + ' (' + str(self.product_link) + ')'

class Application(BaseModel):
	image = models.ImageField(blank=True,null=True)
	product_link = models.ManyToManyField(Product, blank=True)
	case_study_link = models.ManyToManyField(CaseStudy, blank=True)
	reason_categories = Choices('research','clinical')
	reason_to_choose = models.CharField(choices=reason_categories, default=reason_categories.research, max_length=15,
		help_text='Does this Application belong to "Clinical Services" or "Research Facilities"?')

	def full_slug(self):
		if self.reason_to_choose == 'research':
			slug = '/movement-analysis-for-research-facilities/#'
		else:
			slug = '/movement-analysis-for-clinical-services/#'
		slug += slugify(self.title)
		return slug 

	def __str__(self):
		if self.title:
			text = self.title 
		else:
			text = (self.body_text[:30] + '..') if len(self.body_text) > 30 else self.body_text
		return text

class History(BaseModel):
	class Meta:
		verbose_name_plural = 'History'
		ordering = ['order']

	image = models.ImageField(blank=True,null=True)

	def __str__(self):
		return self.title 

class ResearchApplication(BaseModel):
	lead_text = models.CharField(max_length=300)
	related_products = models.ManyToManyField(Product) 
	#TODO: Can we limit the number of related products to 4?

	def __str__(self):
		return self.title 

## CONTENT TYPES ##

class SiteMenu(models.Model):
	class Meta:
		verbose_name = 'Menu'
		verbose_name_plural = 'Menus'

	menu_choices = {
		('H', 'Header'),
		('F', 'Footer'),
	}

	title = models.CharField(choices=menu_choices, default='H', unique=True, max_length=1)
	## TODO [LATER]: Include option for external link OR redirect page 

	def __str__(self):
		return self.get_title_display() 

	def get_pages(self):
		return Page.objects.filter(menu=self)

class Page(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	image = models.ImageField(blank=True,null=True) # TOOD: Does this exist?
	featured = models.BooleanField(default=False)
	body_text = models.TextField(blank=True,null=True,
		help_text="This will appear above all the other content on the page. You can use Markdown here.")
	menu = models.ManyToManyField(SiteMenu, blank=True)
	testimonial = models.ForeignKey('Testimonial', on_delete=models.SET_NULL, blank=True, null=True,
		help_text="This will appear below all the other content on the page")

	# 'list-grid.html' can be used to add a list component to a page
	# model_queryset lists the human-readable name and the corresponding queryset is in views.py, as we can't do querysets in models.py

	# It could be possible to use BaseModle.__subclasses__() but 
	# there are too many fringe filter cases. Something to think about.
	model_queryset = {
		'MA-CLI': 'Movement Analysis - Clinical',
		'MA-RES': 'Movement Analysis - Research',
		'CASE': 'Case Studies',
		'EVENT': 'Events',
		'TEAM': 'Team Members',
		'HIST': 'History',
		'DISTR': 'Contact Distributors',
	}
	# Add the Product Types programmatically 
	# TODO: Bring this back
	# for t in ProductType.objects.all():
	# 	product_string = 'PR-' + t.name[0:3]
	# 	model_queryset[product_string] = 'Product - ' + t.name 
	# TODO: Work out if list data is actually staying at all... 

	list_data_choices = []
	for m in model_queryset:
		list_data_choices.append((m,model_queryset[m]))

	list_data = models.CharField(choices=list_data_choices, max_length=100, blank=True, null=True)
	list_data_heading_links = models.BooleanField(
		default=False,
		help_text = "Selecting this will mean that when used in a menu, this page will add jump links for its sub-items.",
		verbose_name = "Add heading links"
	)
	list_data_format = models.CharField(
		choices=Choices('grid','accordion','accordion - card','people','columns'), 
		max_length=20, 
		default='grid',
		verbose_name = 'List Layout',
		help_text = 'How would you like the data to be shown?'
	)

	def get_content(self):
		return ContentObject.objects.filter(page=self)

	def __str__(self):
		return self.title 

class ContentObject(models.Model):
	title = models.CharField(max_length=250,blank=True,null=True)
	body_text = models.TextField(help_text="You can use Markdown here.")
	page = models.ForeignKey(Page, on_delete=models.CASCADE)

	def __str__(self):
		if self.title:
			return self.title 
		else:
			return_string = (self.body_text[:30] + '..') if len(self.body_text) > 30 else self.body_text
			return return_string

## DATA TYPES ##
class EventForthcomingManager(models.Manager):
	def forthcoming_events(self):
		query_one = Event.objects.filter(end_date__isnull=True).filter(start_date__gte=date.today())
		query_two = Event.objects.filter(end_date__gte=date.today())
		forthcoming = query_one | query_two 

		return forthcoming 

class Event(models.Model):
	start_date = models.DateField()
	end_date = models.DateField(blank=True,null=True)
	location = models.CharField(
		max_length=200,
	)
	title = models.CharField(max_length=350)
	link = models.URLField(blank=True,null=True)
	image = models.ImageField(blank=True,null=True)
	body_text = models.TextField(blank=True,null=True, help_text="You can use Markdown here.")

	objects = EventForthcomingManager()
	forthcoming_events = EventForthcomingManager()

	def __str__(self):
		title_string = self.title + ' from ' + str(self.start_date.strftime("%a %d %B, %Y"))
		if self.end_date:
			title_string += ' to ' + str(self.end_date.strftime("%a %d %B, %Y"))
		return title_string

	def clean(self):
		if self.end_date < self.start_date:
			raise ValidationError('Event cannot end before it starts')

	def save(self, *args, **kwargs):
		self.full_clean() 
		super(Event, self).save(*args, **kwargs)

	def is_forthcoming(self):
		# Duplicated due to wanting to display it in the admin
		ref_date = self.end_date if self.end_date else self.start_date

		if ref_date >= date.today():
			return True 
		else:
			return False 

	is_forthcoming.boolean = True 

class CompanyInfo(models.Model):
	class Meta:
		verbose_name = 'Company Info'
		verbose_name_plural = verbose_name

	email = models.EmailField()
	phone_number = models.CharField(max_length=20)
	address = models.TextField()
	company_text = models.TextField(help_text="About the company, eg. registration info, company number")
	tagline = models.CharField(max_length=350)
	vision = models.TextField()

	def __str__(self):
		return 'Company Info'

class TeamMember(models.Model):
	type_choices = {
		('MGMT', 'Management'),
		('KEYC', 'Key Contact'),
		('ADVS', 'Advisors'),
	}
	person_type = models.CharField(choices=type_choices, default='KEYC',max_length=4)

	person_name = models.CharField(max_length=200)
	image = models.ImageField(blank=True,null=True)
	role = models.CharField(max_length=140, blank=True,null=True)
	bio = models.TextField(blank=True,null=True)

	def __str__(self):
		return_string = self.person_name 
		if self.role:
			return_string += ' (' + self.role + ')'
		return return_string

class Distributor(models.Model):
	area = models.CharField(max_length=100)
	name = models.CharField(max_length=150)
	website = models.URLField(blank=True,null=True)
	phone_number = models.CharField(max_length=16,blank=True,null=True)
	address = models.TextField(blank=True,null=True)

	def __str__(self):
		return self.name + ' (' + self.area + ')'

class Testimonial(models.Model):
	quote = models.TextField()
	source = models.CharField(max_length=200,blank=True,null=True)

	def used_in(self):
		return list(Page.objects.filter(testimonial=self).all())

	def __str__(self):
		quote = (self.quote[:30] + '..') if len(self.quote) > 30 else self.quote
		return_string = '"' + quote + '"'
		if self.source:
			return_string += ' -' + self.source 
		return return_string

class Vacancy(models.Model):
	class Meta:
		verbose_name = 'Vacancy'
		verbose_name_plural = 'Vacancies'

	title = models.CharField(max_length=200)
	body_text = models.TextField(blank=True,null=True, help_text="You can use Markdown here.")
	deadline = models.DateField(blank=True,null=True)

	def __str__(self):
		return self.title 

class Contact(models.Model):
	class Meta:
		verbose_name = 'Contact Form Response'
		verbose_name_plural = 'Contact Form Responses'
		ordering = ['-submission_date']

	name = models.CharField(max_length=200)
	email = models.EmailField()
	message = models.TextField()
	submission_date = models.DateTimeField(default=dj_timezone.now)

	def __str__(self):
		message = (self.message[:30] + '..') if len(self.message) > 30 else self.message
		return self.name + ' "' + message + '" on ' + str(self.submission_date)

