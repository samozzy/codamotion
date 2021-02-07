from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

app_name = 'website'

product_types = ['complete-movement-analysis-systems','other-measurement-components','data-hubs','software','3d-measurement']

urlpatterns = [] 
for product in product_types:
	urlpatterns += path((product+'/'), views.ProductListView.as_view(), name=('product-'+product), kwargs={'product_type':product}),


urlpatterns += [
	path('', views.HomeView.as_view(), name='index'),
	path('movement-analysis-for-research-facilities/', views.MovementAnalysisResearchView.as_view(), name='mvmt-research'),
	path('movement-analysis-for-clinical-services/', views.MovementAnalysisClinicalView.as_view(), name='mvmt-clinical'),

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

	# Any other Page objects caught here: Pages that override the above are handled via views.py
	path('<slug:slug>/', views.PageView.as_view(), name='pages'),
]

handler404 = views.PageNotFoundView.as_view()