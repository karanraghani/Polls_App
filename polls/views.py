from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.views import generic
from django.urls import reverse

# Create your views here.

#Implemnting Generic Views using "generic" as Superclass.
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'list_of_questions'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultView(generic.DetailView):
	model = Question
	template_name = 'polls/result.html'
'''
def index(request):
	list_of_questions = Question.objects.order_by('-pub_date')
	return render(request,'polls/index.html', {'list_of_questions': list_of_questions})

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,'polls/detail.html', {'question': question})

def results(request, question_id):
	return HttpResponse(f"You are looking at result of question {question_id}")
'''
def vote(request, question_id):
	question = get_object_or_404(Question,pk=question_id)
	try:
		selected_choice = Choice.objects.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You did not select a choice"
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		
		# now we redirect insted of render(as if done so by clicking back button it will post the form again)
		# reverse generates url and takes view name and agruments if any
		return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
	
