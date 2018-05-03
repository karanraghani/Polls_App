import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		time = timezone.now()
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(),True)

class QuestionIndexViewTests(TestCase):
	def test_no_question(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No Polls available")
		self.assertQuerysetEqual(response.context['list_of_questions'],[])

	def test_past_question(self):
		create_question("past question",-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['list_of_questions'],
			['<Question: past question>']
			)

	def test_future_question(self):
		create_question(question_text="future_question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertEqual( response.status_code, 200)
		self.assertContains( response, "No Polls available")

	def test_future_and_past_question(self):
		create_question(question_text="past question", days=-30)
		create_question(question_text="future_question", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['list_of_questions'],
			['<Question: past question>']
			)

	def test_two_past_question(self):
		create_question(question_text="past question 1", days=-30)
		create_question(question_text="past question 2", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['list_of_questions'],
			['<Question: past question 2>','<Question: past question 1>']
			)

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		future_question = create_question(question_text="future question",days=30)
		response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		past_question = create_question(question_text="past question", days=-30)
		response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
		self.assertContains(response, past_question.question_text)







