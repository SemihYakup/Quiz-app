from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Quiz, Question


def home(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quizapp/home.html', {'quizzes': quizzes})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesap oluşturuldu! Giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quizapp/signup.html', {'form': form})


def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = list(quiz.questions.all())
    total = len(questions)

    if total == 0:
        messages.error(request, 'Bu testte henüz soru yok.')
        return redirect('quizapp:home')

    q_index = int(request.GET.get('q', 0))
    if q_index >= total:
        q_index = total - 1

    question = questions[q_index]

    return render(request, 'quizapp/quiz_detail.html', {
        'quiz': quiz,
        'question': question,
        'q_index': q_index,
        'total': total,
        'prev_index': q_index - 1,
        'next_index': q_index + 1,
        'is_last': q_index == total - 1,
        'range': range(total),
    })


def quiz_submit(request, pk):
    if request.method != 'POST':
        return redirect('quizapp:home')

    quiz = get_object_or_404(Quiz, pk=pk)
    questions = list(quiz.questions.all())

    score = 0
    total_points = 0
    results = []

    for q in questions:
        answer = request.POST.get(f'q_{q.id}', '')
        is_correct = answer == q.correct_answer
        if is_correct:
            score += q.points
        total_points += q.points
        results.append({
            'question': q,
            'given': answer,
            'correct': q.correct_answer,
            'is_correct': is_correct,
        })

    # Yüzde hesapla
    percentage = round((score / total_points * 100)) if total_points > 0 else 0

    # Kullanıcının belirlediği eşikler — quiz'e bağlı değil, sabit
    if percentage >= 85:
        verdict = 'mukemmel'
        verdict_text = '🎉 Mükemmel!'
        verdict_color = '#16a34a'
    elif percentage >= 70:
        verdict = 'cok_iyi'
        verdict_text = '👏 Çok İyi!'
        verdict_color = '#2563eb'
    elif percentage >= 50:
        verdict = 'iyi'
        verdict_text = '👍 İyi'
        verdict_color = '#ca8a04'
    elif percentage >= 30:
        verdict = 'orta'
        verdict_text = '😐 Orta'
        verdict_color = '#ea580c'
    else:
        verdict = 'kotu'
        verdict_text = '📚 Yetersiz'
        verdict_color = '#dc2626'

    return render(request, 'quizapp/result.html', {
        'quiz': quiz,
        'score': score,
        'total_points': total_points,
        'total_questions': len(questions),
        'correct_count': sum(1 for r in results if r['is_correct']),
        'results': results,
        'percentage': percentage,
        'verdict_text': verdict_text,
        'verdict_color': verdict_color,
    })

@login_required
def my_quizzes(request):
    quizzes = Quiz.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'quizapp/my_quizzes.html', {'quizzes': quizzes})


@login_required
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', '').strip()
        if not title:
            messages.error(request, 'Test adı boş olamaz.')
            return render(request, 'quizapp/create_quiz.html')
        quiz = Quiz.objects.create(
            title=title,
            category=category,
            created_by=request.user
        )
        messages.success(request, 'Test oluşturuldu! Şimdi soru ekleyebilirsiniz.')
        return redirect('quizapp:add_question', pk=quiz.pk)
    return render(request, 'quizapp/create_quiz.html')


@login_required
def add_question(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, created_by=request.user)
    questions = quiz.questions.all()

    if request.method == 'POST':
        Question.objects.create(
            quiz=quiz,
            question_text=request.POST['question'],
            choice1=request.POST['choice1'],
            choice2=request.POST['choice2'],
            choice3=request.POST['choice3'],
            choice4=request.POST['choice4'],
            correct_answer=request.POST['correct'],
            points=int(request.POST.get('points', 3)),
            image=request.FILES.get('image'),
        )
        messages.success(request, 'Soru eklendi!')
        return redirect('quizapp:add_question', pk=quiz.pk)

    return render(request, 'quizapp/add_question.html', {
        'quiz': quiz,
        'questions': questions,
    })


@login_required
def delete_question(request, quiz_pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk, quiz__created_by=request.user)
    if request.method == 'POST':
        question.delete()
    return redirect('quizapp:add_question', pk=quiz_pk)


@login_required
def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, created_by=request.user)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Test silindi.')
    return redirect('quizapp:my_quizzes')