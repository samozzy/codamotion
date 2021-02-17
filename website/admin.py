from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import (User, Page, ContentObject, SiteMenu,
	Event, History, CompanyInfo, TeamMember, Distributor, Testimonial, 
	ReasonsToChoose, CaseStudy, ProductType, Product, Component, Application,
	ResearchApplication, Vacancy, Contact)

# Models to be exposed to the admin
class ContentObjectInline(admin.TabularInline):
	model = ContentObject 
	min_num = 0
	extra = 0

def make_featured(modeladmin,request,queryset):
	queryset.update(featured=True)

def remove_featured(modeladmin,request,queryset):
	queryset.update(featured=False)

def move_down(modeladmin,request,queryset):
	# Increase number 
	for item in queryset:
		item.order += 1 
		item.save() 

def move_up(modeladmin,request,queryset):
	# Decrease number
	for item in queryset:
		if item.order == 1:
			continue 
		else:
			item.order -= 1
			item.save() 

def set_order(modeladmin,request,queryset):
	counter = 1
	for item in queryset:
		item.order = counter 
		item.save() 
		counter += 1

class PageMenuInline(admin.TabularInline):
	# class Meta:
	verbose_name: "Pages"
	model = Page.menu.through 
	min_num = 0 
	extra = 0 

class PageAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'featured']
	prepopulated_fields = {"slug": ("title",)}
	inlines = [ContentObjectInline]
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}

	fieldsets = (
		(None, {
			'fields':(
				'title',
				'slug',
				'featured',
				'image',
				'body_text',
				'testimonial',
				('menu', 'parent', 'page_children_html'),
				),
			}),
		# ('Layout Options', {
		# 	'fields': (('list_data','list_data_format','list_data_heading_links'),),
		# 	'classes': ('collapse',),
		#  }),
	 )

	actions = [make_featured,remove_featured]


class SiteMenuAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		title_choice_count = len(SiteMenu.menu_choices)
		if num_objects >= title_choice_count:
			return False
		else:
			return True 
	inlines = [PageMenuInline]

class EventAdmin(admin.ModelAdmin):
	list_display = ['title', 'start_date', 'end_date', 'is_forthcoming', 'location']

class CompanyInfoAdmin(admin.ModelAdmin):
	def has_add_permission(self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False 
		else:
			return True 

class TeamMemberAdmin(admin.ModelAdmin):
	list_display = ['person_name', 'role', 'person_type']
	list_filter = ['person_type']

class DistributorAdmin(admin.ModelAdmin):
	list_display = ['name', 'area', 'order']
	actions = [set_order,move_up,move_down]

class ReasonsToChooseAdmin(admin.ModelAdmin):
	list_display = ['title', 'category','order']
	actions = [make_featured,remove_featured,set_order,move_up,move_down]

class ApplicationAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}
	list_display = ['title','featured','order']
	actions = [make_featured,remove_featured,set_order,move_up,move_down]

class ApplicationInline(admin.TabularInline):
	model = Application.product_link.through
	min_num = 0
	extra = 0

class ComponentInline(admin.TabularInline):
	model = Component 
	min_num = 0
	extra = 0

	fieldsets = (
		(None, {
			'fields': (
				'title',
				'body_text',
				'image', 
			),
		}),
	)
	actions = [make_featured,remove_featured]

class CaseStudyAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("title",)}
	list_display =['title', 'featured','order','has_image']
	actions = [make_featured,remove_featured,set_order,move_up,move_down]


def toggle_grid(modeladmin,request,queryset):
	for item in queryset:
		if item.grid_list == True:
			item.grid_list = False 
		else:
			item.grid_list = True 
		item.save() 

class ProductTypeAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ['name','slug','grid_list']
	actions = [toggle_grid]


class ProductAdmin(admin.ModelAdmin):
	inlines = [ComponentInline, ApplicationInline]
	actions = [make_featured,remove_featured,move_up,move_down,set_order]
	list_display = ['title', 'product_type', 'order', 'component_count']
	list_filter = ['product_type']

class ContactAdmin(admin.ModelAdmin):
	list_display = ['name','email', 'submission_date']

class HistoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'order']

class TestimonialAdmin(admin.ModelAdmin):
	list_display = ['quote','source','used_in']
	readonly_fields = ['used_in']

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(ReasonsToChoose, ReasonsToChooseAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vacancy)

admin.site.register(SiteMenu, SiteMenuAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Contact, ContactAdmin)

admin.site.register(Application, ApplicationAdmin)