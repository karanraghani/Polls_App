from django.contrib import admin
from .models import Question, Choice

# Register your models here.

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		('Question',		 {'fields': ['question_text']}),
		('Data Information', {'fields': ['pub_date']}),
	]

	# for the choices to be shown along the question in the admin view
	inlines = [ChoiceInline] #inline feature of admin

	# for displaying additional information about question in the lists of questions
	list_display = ('question_text', 'pub_date', 'was_published_recently')  #list display is feature of admin

	#filter by date
	list_filter = ['pub_date']

	# adding search feature
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
#admin.site.register(Question)