from datetime import date
from django.contrib import messages, auth
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import FileResponse, HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from .models import (Page, SiteMenu, Application, Product, ProductType, CaseStudy, TeamMember, 
	History, Vacancy, Event, Contact, CompanyInfo, ReasonsToChoose, Distributor, 
	Testimonial)
from .forms import ContactForm 

# Codamotion Website Views
class BaseView(SuccessMessageMixin, CreateView):
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
		# Stay where we are on success 
		return self.request.path 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['header_menu'] = SiteMenu.objects.filter(title='H').first().get_pages() or None 
		context['product_type_list'] = ProductType.objects.all() 
		context['footer_menu'] = SiteMenu.objects.filter(title='F').first().get_pages() or None 
		context['tagline'] = CompanyInfo.objects.first().tagline 
		context['company_text'] = CompanyInfo.objects.first().company_text
		if Testimonial.objects.first():
			context['page'] = {'testimonial': Testimonial.objects.first()}

		# if Page.objects.get(slug=)

		return context

class PageView(generic.DetailView, BaseView):
	model = Page
	allow_empty = False 
	template_name = 'website/structure/base.html'
	context_object_name = 'page'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.object.title 
		if self.object and type(self.object).__name__ == 'Page': 
			# Handler for Page items using list_data, rather than the more 'simple' list pages.
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
					context['list_data_items'] = Product.objets.filter(product_type=product)
					context['include_string'] = 'website/list-layout/pr.html'
				else:
					context['list_data_items'] = model_queryset[self.object.get_list_data_display()]
					context['include_string'] = 'website/list-layout/' + self.object.list_data + '.html'

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

class MovementAnalysisClinicalView(BaseView):
	template_name = 'website/clinical.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['reasons'] = ReasonsToChoose.objects.filter(category='clinical')
		context['title'] = 'Movement Analysis for Clinical Services'

		return context

class MovementAnalysisResearchView(BaseView):
	template_name = 'website/research.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Movement Analysis for Research Facilities'
		context['applications'] = Application.objects.all()
		context['reasons'] = ReasonsToChoose.objects.filter(category='research')
		return context


class ProductListView(BaseView, generic.ListView):
	template_name = 'website/product-list.html'
	# allow_empty = False 
	context_object_name = 'products' 
	model = Product 

	def get_queryset(self, **kwargs):
		return Product.objects.filter(product_type__slug=self.kwargs['product_type'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = ProductType.objects.get(slug=self.kwargs['product_type']).name
		return context 


class CaseStudyListView(BaseView, generic.ListView):
	template_name = 'website/case-study-list.html'
	model = CaseStudy 
	context_object_name = 'case_studies'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Case Studies'
		return context

class CaseStudySingleView(generic.DetailView, BaseView):
	model = CaseStudy
	template_name = 'website/case-study-single.html' 
	context_object_name = 'case_study'

class TeamView(BaseView, generic.ListView):
	template_name = 'website/team.html'
	model = TeamMember

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Codamotion Team'
		context['management'] = TeamMember.objects.all().filter(person_type='MGMT')
		context['key_contacts'] = TeamMember.objects.all().filter(person_type='KEYC')
		context['advisors'] = TeamMember.objects.all().filter(person_type='ADVS')
		context['full_team'] = TeamMember.objects.all()
		return context 

class HistoryView(BaseView, generic.ListView):
	model = History 
	template_name = 'website/history.html'
	context_object_name = 'history'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'The History of Codamotion'
		return context 

class VacancyListView(BaseView, generic.ListView):
	model = Vacancy
	template_name = 'website/vacancies.html'
	context_object_name = 'vacancies'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Working at Codamotion'
		context['page']['testimonial'] = None
		return context 

class EventListView(BaseView, generic.ListView):
	template_name = 'website/event.html'
	model = Event 
	context_object_name = 'events'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Forthcoming Events'
		context['past_events'] = Event.objects.filter(end_date__lt=date.today())
		context['forthcoming_events'] = Event.objects.forthcoming_events()
		return context

class DistributorView(BaseView, generic.ListView):
	template_name = 'website/distributor.html' 
	model = Distributor
	context_object_name = 'distributors'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['head_office'] = CompanyInfo.objects.first() 
		context['title'] = 'Contact Codamotion'

		return context 