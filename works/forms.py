from django.contrib.auth.models import User
from main.models import Work, Group, File
from django import forms


class AddFile(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)
        super(AddFile, self).__init__(*args, **kwargs)
        if initial:
            self.fields['user'].queryset = User.objects.filter(pk=initial['user'].pk)
            self.initial['user'] = initial['user']
            self.fields['work'].queryset = Work.objects.filter(pk=initial['work'].pk)
            self.initial['work'] = initial['work']

    class Meta:
        model = File
        fields = ['work', 'user', 'file']

        widgets = {
            'work': forms.Select(attrs={
                'hidden': 'True'
            }),
            'user': forms.Select(attrs={
                'hidden': 'True'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control mt-4'
            }),
        }


class CheckWork (forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial')
        super(CheckWork, self).__init__(*args, **kwargs)
        if initial:
            self.fields['user'].queryset = User.objects.filter(pk=initial['user'].pk)
            self.fields['work'].queryset = Work.objects.filter(pk=initial['work'].pk)

    class Meta:
        model = File
        fields = '__all__'
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'hidden': 'True'
            }),
            'work': forms.Select(attrs={
                'hidden': 'True'
            }),
            'user': forms.Select(attrs={
                'hidden': 'True'
            }),
            'status': forms.NumberInput(attrs={
                'hidden': 'True'
            }),
            'mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'required': 'True'
            }),
            'file': forms.FileInput(attrs={
                'hidden': 'True'
            }),
            'teach_ans': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_mark(self):
        mark = self.cleaned_data.get('mark')
        if mark > 5 or mark < 1:
            raise forms.ValidationError("Поставьте оценку от 1 до 5!")
        else:
            return mark


class AddWork(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)
        super(AddWork, self).__init__(*args, **kwargs)
        self.fields['Title'].empty_label = "Тип работы не выбран"
        if initial:
            self.fields['user'].queryset = User.objects.filter(pk=initial['user'].pk)
            self.initial['user'] = initial['user']
            self.fields['in_group'].queryset = Group.objects.filter(pk=initial['in_group'].pk)
            self.initial['in_group'] = initial['in_group']

    class Meta:
        model = Work
        fields = ['subject', 'Title', 'toDate', 'work_file', 'user', 'in_group']
        widgets = {
            'subject': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Предмет',
                'name': 'subject',
                'required': 'True',
            }),
            'Title': forms.Select(attrs={
                'class': 'form-control',
                'name': 'title',
                'required': 'True',
            }),
            'toDate': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'name': 'toDate'
            }),
            'work_file': forms.FileInput(attrs={
                'class': 'form-control',
                'name': 'file',
                'required': 'True',
            }),
            'user': forms.Select(attrs={
                'hidden': 'True'
            }),
            'in_group': forms.Select(attrs={
                'hidden': 'True'
            })
        }


