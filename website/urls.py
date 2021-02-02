from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

app_name = 'website'

urlpatterns = [
	path('', views.HomeView.as_view(), name='index'),
	path('movement-analysis-for-research-facilities/', views.MovementAnalysisResearchView.as_view(), name='mvmt-research'),
	path('movement-analysis-for-clinical-services/', views.MovementAnalysisClinicalView.as_view(), name='mvmt-clinical'),


	# path('support/', views.PageView.as_view(), name='support'),
	path('case-studies/', views.CaseStudyListView.as_view(), name='case-study-list'),
	path('portfolio/<slug:slug>/', views.CaseStudySingleView.as_view(), name='case-study-single'),
	path('case-studies/<slug:slug>/', RedirectView.as_view(pattern_name='website:case-study-single', permanent=True)),

	path('about/', views.TeamView.as_view(), name='the-team'),

	path('about/', include([
		path('history/', views.HistoryView.as_view(), name='history'),
		path('vision-ethos/', views.VisionView.as_view(), name='vision-ethos'),
		path('working-at-codamotion/', views.VacancyListView.as_view(), name='vacancies'),
		path('the-team/', RedirectView.as_view(pattern_name='website:the-team', permanent=True)),
	])),
	path('forthcoming-events/', views.EventListView.as_view(), name='event-list'),

	path('contact/', views.DistributorView.as_view(), name='contact'),

	path('<slug:product_type>/', views.ProductListView.as_view(), name='product-list'),
	# path('<slug:slug>/', views.PageView.as_view(), name='pages'),
]

'''

/ - index
/movement-analysis-for-clinical-systems - Applications.filter(clinical)
/movement-analysis-for-research - Applications.filter(research)

/{ product-type } - Product list Products.all()
/support - Training and service contracts (Page) ~Nothing~

/case-studies - Case Study list CaseStudy.all()
/portfolio/{ case study }	CaseStudy.single

/about(/the-team/) - List of team Team.all()
/about/history - List of history inc. initial bit History.all()
/about/vision-ethos - Vision and Ethos That.single()
/forthcoming-events - List of Events Events.all()

/contact - Contact page ~Nothing~

/about/working-at-codamotion - Vacancies list Vacancies.all() 
'''
