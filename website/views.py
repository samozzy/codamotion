from datetime import date
from django.contrib import messages, auth
from django.contrib.messages.views import SuccessMessageMixin 
from django.http import FileResponse, HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.utils.text import slugify 
from django.urls import reverse, reverse_lazy
from itertools import chain 
from .models import (Page, SiteMenu, Application, ResearchApplication, Product, ProductType, CaseStudy, TeamMember, 
	History, Vacancy, Event, Contact, Component, CompanyInfo, ReasonsToChoose, Distributor, 
	Testimonial)
from .forms import ContactForm 

# Codamotion Website Views
class BaseView(SuccessMessageMixin, CreateView):
	form_class = ContactForm 
	success_message = 'Message submitted successfully.'

	def get_success_url(self):
		# Stay where we are on success of the contact form 
		return self.request.path 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if SiteMenu.objects.filter(title='H'): 
			context['header_menu'] = SiteMenu.objects.filter(title='H').first().get_pages().exclude(slug='contact') or None 
		## The contact page should always go at the end of the menu so a quick special case workaround above.
		context['product_type_list'] = ProductType.objects.all() 
		if SiteMenu.objects.filter(title='F'):
			context['footer_menu'] = SiteMenu.objects.filter(title='F').first().get_pages() or None 
		context['company_info'] = CompanyInfo.objects.first() 

		if type(self.object).__name__ != 'Page':
			# If we're not looking at a Page, we can do some...
			# 			PAGE OVERRIDES
			# If Page objects are created for existing pages (in urls.py)
			# AND have matching slugs, that Page can throw some overrides or body_text, etc.
			# [It feels a bit hacky but it works]
			context['page'] = {}

			# Work out if there's a Page matching the final slug in the path
			page_request = self.request.path 
			if page_request == '/':
				# Special case for the home page (as '/' is not a valid Django slug)
				page_override = Page.objects.filter(slug='home').first() or None 
			else:
				# Remove the opening and trailing / 
				page_request = self.request.path[1:-1]
				# Go through any parent pages and get to the root slug
				f = page_request.find('/')
				while f >= 0:
					page_request = page_request[(f+1):]
					f = page_request.find('/')

				page_override = Page.objects.filter(slug=page_request).first() or None 
				# Would use objects.get() but that gives us an error that filter().first() doesn't

			if page_override:
				# Use the page if there is one 
				context['page'] = page_override
			else:
				# No page? Here are the defaults 
				context['page']['testimonial'] = Testimonial.objects.first() or None 

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
			# TODO: Work out if this goes away... [It may simply be heavily reduced]
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

class PageNotFoundView(generic.TemplateView):
	template_name = 'website/error/404.html'

class HomeView(BaseView):
	template_name = 'website/home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Welcome to Codamotion"
		context['home_header'] = True 

		featured_list = list(chain(
			Page.objects.filter(featured=True),
			ReasonsToChoose.objects.filter(featured=True),
			CaseStudy.objects.filter(featured=True),
			ProductType.objects.filter(featured=True),
			Product.objects.filter(featured=True),
			Component.objects.filter(featured=True),
			Application.objects.filter(featured=True),
			ResearchApplication.objects.filter(featured=True),
		))
		context['featured_list'] = featured_list
		return context 

class MovementAnalysisClinicalView(BaseView):
	template_name = 'website/reasons.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Movement Analysis for Clinical Services'
		context['applications'] = Application.objects.filter(reason_to_choose='clinical').prefetch_related('product_link').prefetch_related('case_study_link').values() 
		context['reasons'] = ReasonsToChoose.objects.filter(category='clinical')
		context['header'] = 'Clinical Services'
		context['application_header'] = 'Clinical Applications'

		return context

class MovementAnalysisResearchView(BaseView):
	template_name = 'website/reasons.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Movement Analysis for Research Facilities'
		context['applications'] = Application.objects.filter(reason_to_choose='research').prefetch_related('product_link').prefetch_related('case_study_link').values()
		context['reasons'] = ReasonsToChoose.objects.filter(category='research')
		context['header'] = 'Research Facilities'
		context['application_header'] = 'Research Applications'
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
		context['title'] = ProductType.objects.get(slug=self.kwargs['product_type']).title
		context['product_type'] = ProductType.objects.get(slug=self.kwargs['product_type'])
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.object.title 
		return context 

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
		context['page']['testimonial'] = None 
		return context 

class VacancyListView(BaseView, generic.ListView):
	model = Vacancy
	template_name = 'website/vacancies.html'
	context_object_name = 'vacancies'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Working at Codamotion'
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

class VisionView(BaseView, generic.ListView):
	model = CompanyInfo
	template_name = 'website/vision.html'
	context_object_name = 'vision'

	def get_queryset(self, **kwargs):
		if CompanyInfo.objects.first():
			return CompanyInfo.objects.first().vision
		else:
			return None 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Vision & Ethos'

		return context 