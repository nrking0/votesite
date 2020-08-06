from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice, Voter
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:50]


class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Question
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    template_name = 'poll/vote.html'


class ResultsView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'poll/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if Voter.objects.filter(question_id=question_id, user_id=request.user.id).exists():
        return render(request, 'poll/vote.html', {
        'question': question,
        'error_message': "Sorry, but you have already voted."
        })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/vote.html', {
            'question': question,
            'error_message': "You didn't select a choice!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        v = Voter(user=request.user, question=question)
        v.save()
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})










# Create your views here.

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
 #   context = {'latest_question_list': latest_question_list}
  #  return render(request, 'poll/index.html', context)

#def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question': question})
    

#def results(request, question_id):
#    return HttpResponse("You're looking at the results of question %s." % question_id)
#
#def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
