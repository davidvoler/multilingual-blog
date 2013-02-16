from django.forms import ModelForm

from infra.models import UserProfile

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = (
                  #'theme',
                  'lang',
                  'd_lang')
        