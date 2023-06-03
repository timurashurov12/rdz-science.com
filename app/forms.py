from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Blog, Category
from django import forms
from ckeditor.widgets import CKEditorWidget

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Старый пароль'),}),
        
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Новый пароль'),
            }),
        
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Подтвердите новый пароль'),
            }),
        
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите email'),
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = _('Введите логин')
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = _('Введите пароль')
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] =_('Подтвердите пароль')
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = _('Ваш логин')

        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = _('Ваш email')

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _("Введите название"),
        }),
        required=True,
    )
    description = forms.CharField(
        widget=CKEditorWidget(attrs={
            'class': 'form-control',
            'placeholder': _("Введите описание"),
            'required': True,
        }),
        required=True
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        required=True,
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        }),
        required=False,
    )

    class Meta:
        model = Blog
        fields = ['title', 'description', 'category', 'file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['delete_images'] = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple, required=False)
        
        if self.instance.pk:
            self.fields['delete_images'].choices = [(image.id, str(image)) for image in self.instance.images.all()]
        else:
            self.fields['delete_images'].choices = []

    def save(self, commit=True):
        article = super().save(commit=False)
        if self.user:
            article.user = self.user

        # Сохранение данных в полях title_ru, title_en, title_uz
        article.title_ru = self.cleaned_data['title']
        article.title_en = self.cleaned_data['title']
        article.title_uz = self.cleaned_data['title']

        # Сохранение данных в полях description_ru, description_en, description_uz
        article.description_ru = self.cleaned_data['description']
        article.description_en = self.cleaned_data['description']
        article.description_uz = self.cleaned_data['description']

        if commit:
            article.save()
        return article
