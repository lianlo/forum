from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Question, Tag, Answer
from .utils import ObjectCreateMixin, ObjectDetailMixin
from .forms import TagForm, QuestionForm, AnswerForm

from django.core.paginator import Paginator

from django.db.models import Q


class Search:
    def get_question_answer(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            questions = Question.objects.filter(Q(title__icontains=search_query) |
                                                Q(body__icontains=search_query) |
                                                Q(answer__body__icontains=search_query))
        else:
            questions = Question.objects.all()
        return questions


class QuestionsList(View):
    def get(self, request):
        questions_per_page = 4
        questions = Search().get_question_answer(request)

        paginator = Paginator(questions, questions_per_page)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context = {
            'question_search_response': questions,
            'questions': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
        }

        return render(request, 'forum/index.html', context=context)


class QuestionDetail(View):
    def get(self, request, slug):
        form = AnswerForm()
        question = get_object_or_404(Question, slug__iexact=slug)
        answers = question.answer_set.all()
        answers_number = question.answer_set.count()

        context = {
            'question': question,
            'form': form,
            'answers': answers,
            'answers_number': answers_number
        }

        return render(request, 'forum/question_detail.html', context=context)

    def post(self, request, slug):
        bound_form = AnswerForm(request.POST)
        question = get_object_or_404(Question, slug__iexact=slug)

        if bound_form.is_valid():
            new_answer = bound_form.save()
            question.answer_set.add(new_answer)

            return redirect(question)
        return render(request, 'forum/answer_create_form.html', context={'form': bound_form})


class QuestionCreate(ObjectCreateMixin, View):
    form_model = QuestionForm
    template = 'forum/question_create_form.html'


class TagCreate(ObjectCreateMixin, View):
    form_model = TagForm
    template = 'forum/tag_create.html'


class TagDetail(View, ObjectDetailMixin):
    model = Tag
    template = 'forum/tag_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'forum/tags_list.html', context={'tags': tags})

