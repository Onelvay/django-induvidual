from django import forms
from .models import Post, Comment

# Форма для создания и редактирования постов
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Поля, которые будут отображаться в форме

# Форма для добавления комментариев
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # В комментарии нужно только содержание

from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from .models import Post

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Привязка комментария к посту
            comment.author = request.user  # Автор комментария - текущий пользователь
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blogs/comment_form.html', {'form': form})