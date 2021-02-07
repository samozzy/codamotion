from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from model_utils import Choices 

class User(AbstractUser):
	# Give us scope to do some fancy user things later
    pass


## FEATURED ITEMS ##
# TODO: Make work
class BaseModel(models.Model):
	title = models.CharField(max_length=150)
	body_text = models.TextField(null=True,blank=True)
	order = models.IntegerField(default=1)

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
	image = models.ImageField(blank=True,null=True)

	def save(self, *args, **kwargs):
		if not self.pk or not self.slug:
			self.slug = slugify(self.title)
		super(CaseStudy, self).save(*args, **kwargs)

	def __str__(self):
		return self.title 

class ProductType(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField()

	def get_products(self):
		return Product.objects.filter(product_type=self)

	def save(self, *args, **kwargs):
		if not self.pk:
			self.slug = slugify(self.name)
		super(ProductType, self).save(*args, **kwargs)

	def __str__(self):
		return self.name 


class Product(BaseModel):
	product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

	image = models.ImageField(blank=True,null=True)

	def __str__(self):
		return self.title + ' (' + str(self.product_type) + ')'

	def slug(self):
		return slugify(self.title)

	def full_slug(self):
		# Slightly dependent on this matching urls.py until the end of time 
		base = self.product_type.slug 
		product = self.slug() 
		return '/' + str(base) + '#' + str(product)

	def get_components(self):
		return Component.objects.filter(product_link=self)

class Component(BaseModel):
	image = models.ImageField(blank=True,null=True)
	product_link = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.title + ' (' + str(self.product_link) + ')'

class Application(BaseModel):
	image = models.ImageField(blank=True,null=True)
	product_link = models.ManyToManyField(Product)

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
	body_text = models.TextField(blank=True,null=True,
		help_text="This will appear above all the other content on the page")
	menu = models.ManyToManyField(SiteMenu, blank=True)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	testimonial = models.ForeignKey('Testimonial', on_delete=models.DO_NOTHING, blank=True, null=True,
		help_text="This will appear below all the other content on the page")
	## TODO: Validate that parent cannot be itself 
	## TODO: Add a computed_slug field that is the slug + the parent's slug and updated on every save

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

	def page_children(self):
		return Page.objects.filter(parent=self)

	def __str__(self):
		return self.title 

class ContentObject(models.Model):
	title = models.CharField(max_length=250,blank=True,null=True)
	body_text = models.TextField()
	page = models.ForeignKey(Page, on_delete=models.CASCADE)

	def __str__(self):
		if self.title:
			return self.title 
		else:
			return_string = (self.body_text[:30] + '..') if len(self.body_text) > 30 else self.body_text
			return return_string

class FeaturedItem(models.Model):
	page = models.ForeignKey(Page, on_delete=models.DO_NOTHING)

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
	body_text = models.TextField(blank=True,null=True)

	objects = EventForthcomingManager()
	forthcoming_events = EventForthcomingManager()

	def __str__(self):
		title_string = self.title + ' from ' + str(self.start_date.strftime("%a %d %B, %Y"))
		if self.end_date:
			title_string += ' to ' + str(self.end_date.strftime("%a %d %B, %Y"))
		return title_string

	def is_forthcoming(self):
		# Duplicated due to wanting to display it in the admin
		# TODO: Can we DRY this up? 
		if self.end_date:
			if self.end_date >= date.today():
				return True 
			else:
				return False 
		elif self.start_date >= date.today():
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
	about = models.TextField()

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
	source = models.CharField(max_length=200)

	def __str__(self):
		quote = (self.quote[:30] + '..') if len(self.quote) > 30 else self.quote
		return_string = '"' + quote + '" -' + self.source 
		return return_string

class Vacancy(models.Model):
	class Meta:
		verbose_name = 'Vacancy'
		verbose_name_plural = 'Vacancies'

	title = models.CharField(max_length=200)
	body_text = models.TextField(blank=True,null=True)
	deadline = models.DateField(blank=True,null=True)

	def __str__(self):
		return self.title 

class Contact(models.Model):
	class Meta:
		verbose_name = 'Contact Form Response'
		verbose_name_plural = 'Contact Form Responses'

	name = models.CharField(max_length=200)
	email = models.EmailField()
	message = models.TextField()

	def __str__(self):
		message = (self.message[:30] + '..') if len(self.message) > 30 else self.message
		return self.name + ' "' + message + '"'

