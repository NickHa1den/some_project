from django import forms
from taggit.forms import TagField

from blog.models import Post, Category, Comment


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Категория не выбрана',
                                      widget=forms.Select(attrs={'class': 'form-control py-2',
                                                                 'placeholder': 'Выберите категорию'}))

    class Meta:
        model = Post
        fields = ('title', 'category', 'body', 'snippet', 'images', 'tags', 'status')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название поста'}),
            'snippet': forms.Textarea(attrs={'placeholder': 'Краткое описание', 'rows': 2}),
            'images': forms.FileInput(attrs={'placeholder': 'Фотография, иллюстрация'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Метки'}),
            'status': forms.Select(attrs={'placeholder': 'Статус поста'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control py-2', 'autocomplete': 'off'})

        self.fields['body'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['full_description'].required = False
        self.fields['images'].required = False


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'snippet', 'images')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название статьи'}),
            'snippet': forms.Textarea(attrs={'placeholder': 'Краткое описание', 'rows': 2}),
            'images': forms.FileInput(attrs={'placeholder': 'Фотография, иллюстрация'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control py-2', 'autocomplete': 'off'})

        self.fields['body'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['body'].required = False
        self.fields['images'].required = False


class CommentForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 4, 'placeholder': 'Добавьте свой комментарий...', 'class': 'form-control py-2'}))

    class Meta:
        model = Comment
        fields = ('content',)

        # widgets = {
        #     'content': forms.Textarea(
        #         attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'})
        # }
