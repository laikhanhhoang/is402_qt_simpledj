# polls/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
    # Lấy latest 5 question có id hợp lệ
    latest_question_list = Question.objects.filter(id__isnull=False).order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'latest_question_list': latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

from django.shortcuts import render, get_object_or_404
from .models import Question

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)

    # Tạo danh sách choices kèm percent
    choices_with_percent = []
    for choice in choices:
        if total_votes > 0:
            percent = choice.votes / total_votes * 100
        else:
            percent = 0
        choices_with_percent.append({
            'choice_text': choice.choice_text,
            'votes': choice.votes,
            'percent': percent
        })

    return render(request, 'polls/results.html', {
        'question': question,
        'choices': choices_with_percent
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Trả lại trang detail với lỗi
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect tới trang results
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))