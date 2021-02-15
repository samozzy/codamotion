from django import template
from itertools import chain 
from ..models import Application, Product, CaseStudy, ProductType

register = template.Library() 

@register.simple_tag 
def app_related_items(app_pk):
	# Get the related items for a given application
	app = Application.objects.get(pk=app_pk)
	related = list(chain(
		app.case_study_link.all(),
		app.product_link.all()
	))
	return related 