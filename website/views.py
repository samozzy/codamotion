from datetime import date
from django.contrib import messages, auth
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import FileResponse, HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from .models import (Page, SiteMenu, Application, Product, CaseStudy, TeamMember, 
	History, Vacancy, Event, Contact, CompanyInfo, ReasonsToChoose, Distributor)
from .forms import ContactForm 

# Codamotion Website Views
class BaseView(generic.DetailView):
	form_class = ContactForm 
	success_message = 'Message submitted successfully.'

	# self.object WOULD give us the Page item IF we use a DetailView
	# We somehow need to use a DetailView AND a CreateView
	# We don't necessarily need the success_message if we can put that 
	# in the form class?
	# Could we run the form as a POST into a separate view which then
	# goes back to the page it came from? Where GET to that view basically 
	# doesn't exist and just redirects to /home 

	def get_success_url(self):
		# Stay where we are on sucess 
		return self.request.path 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['header_menu'] = SiteMenu.objects.filter(title='H').first().get_pages() or None 
		context['footer_menu'] = SiteMenu.objects.filter(title='F').first().get_pages() or None 
		context['tagline'] = CompanyInfo.objects.first().tagline 
		context['company_text'] = CompanyInfo.objects.first().company_text

		if self.object.list_data:
			model_queryset = {
				'Movement Analysis - Clinical': ReasonsToChoose.objects.filter(category="clinical"),
				'Movement Analysis - Research': ReasonsToChoose.objects.filter(category="research"),
				'Case Studies': CaseStudy.objects.all(),
				'Events': Event.objects.all(),
				'Team Members': TeamMember.objects.all(),
				'History': History.objects.all(),
				'Contact Distributors': Distributor.objects.all()
			}
			if self.object.list_data[0:3] == 'PR-': 
				# Special case: Product list data types are generated programmatically,
				# so where we're listing products we'll grab them this way.
				product = str(Page.model_queryset[self.object.list_data]).replace('Product - ','')
				context['list_data'] = Product.objets.filter(product_type=product)
			else:
				context['list_data'] = model_queryset[self.object.list_data]

		return context

class HomeView(BaseView):
	# featured_list = ReasonsToChoose.objects.filter(featured=True)
	# featured_list += CaseStudy.objects.filter(featured=True)
	# featured_list += Product.objects.filter(featured=True)
	# featured_list += Component.objects.filter(featured=True)
	# featured_list += Application.objects.filter(featured=True)
	# featured_list += ResearchApplication.objects.filter(featured=True)
	model = Page 
	template_name = 'website/structure/base.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['featured_list'] = featured_list
		context['title'] = "Codamotion"
		context['home_header'] = True 
		return context 

class MovementAnalysisClinicalView(generic.ListView):
	model = ReasonsToChoose 
	template_name = 'website/clinical.html'
	context_object_name = 'reasons'

	def get_queryset(self, **kwargs):
		return ReasonsToChoose.objects.filter(category='clinical')


class MovementAnalysisResearchView(generic.ListView):
	model = ReasonsToChoose
	template_name = 'website/research.html'
	context_object_name = 'reasons'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['applications'] = Application.objects.all()
		return context

	def get_queryset(self, **kwargs):
		return ReasonsToChoose.objects.filter(category='research')


class ProductListView(generic.ListView):
	template_name = 'website/product-list.html'
	allow_empty = False 
	context_object_name = 'products' 

	def get_queryset(self, **kwargs):
		return Product.objects.filter(product_type__slug=self.kwargs['product_type'])

class PageView(BaseView):
	model = Page
	template_name = 'website/structure/base.html'
	context_object_name = 'page'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.object.title 
		return context 


class CaseStudyListView(generic.ListView):
	model = CaseStudy
	template_name = 'website/case-study-list.html'
	context_object_name = 'case_studies'

class CaseStudySingleView(generic.DetailView):
	model = CaseStudy
	template_name = 'website/case-study-single.html' 
	context_object_name = 'case_study'

class TeamView(generic.ListView):
	model = TeamMember
	template_name = 'website/team.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['management'] = TeamMember.objects.all().filter(person_type='MGMT')
		context['key_contacts'] = TeamMember.objects.all().filter(person_type='KEYC')
		context['advisors'] = TeamMember.objects.all().filter(person_type='ADVS')
		context['full_team'] = TeamMember.objects.all()
		return context 

class HistoryView(generic.ListView):
	model = History 
	template_name = 'website/history.html'
	context_object_name = 'history'

class VacancyListView(generic.ListView):
	model = Vacancy 
	template_name = 'website/vacancies.html'
	context_object_name = 'vacancies'

class EventListView(generic.ListView):
	model = Event 
	template_name = 'website/event.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['past_events'] = Event.objects.filter(end_date__lt=date.today())
		context['forthcoming_events'] = Event.objects.forthcoming_events()
		return context

class ContactView(generic.ListView):
	model = Contact 
	template_name = 'website/structure/base.html' 
	form_class = ContactForm 

class DistributorView(generic.ListView):
	model = Distributor 
	context_object_name = 'distributors'
	template_name = 'website/distributor.html' 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		contacts_objects = Contact.objects.all() 
		head_office = CompanyInfo.objects.first() 
		context['contacts'] = [head_office]
		for c in contacts_objects:
			context['contacts'].append(c)

		return context 