from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
  class Meta: 
    model = Project
    fields = ['title','description','tags','demo_link','source_link','featured_image']
    widgets = {
      'tags':forms.CheckboxSelectMultiple(),
    }
  def __init__(self,*args,**kwargs):
    super(ProjectForm,self).__init__(*args,**kwargs)
    for _,field in self.fields.items():
      field.widget.attrs.update({'class':'input'})
    
