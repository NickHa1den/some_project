from django import forms
from taggit.forms import TagField

from blog.models import Post, Category

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'body', 'snippet', 'images', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Название статьи'}),
            'category': forms.Select(choices=choice_list,
                                     attrs={'class': 'form-control py-2', 'placeholder': 'Выберите категорию'}),
            'body': forms.Textarea(attrs={'class': 'form-control py-2', 'placeholder': 'Основной контент'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Краткое описание'}),
            'images': forms.FileInput(
                attrs={'class': 'form-control py-2', 'placeholder': 'Фотография, иллюстрация', 'required': False}),
            'tags': forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Тэги'})
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'snippet')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Название статьи'}),
            'body': forms.Textarea(attrs={'class': 'form-control py-2',
                                          'placeholder': 'Основной контент'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control py-2', 'placeholder': 'Краткое описание'}),
        }
