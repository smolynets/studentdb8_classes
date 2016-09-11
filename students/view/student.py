# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.student import Student
from ..models.group import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from PIL import Image
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Button







#########################################################################
#stud_list
class StudentList(ListView):
  model = Student
  context_object_name = 'students'
  template_name = 'students/stud.html'
  def get_context_data(self, **kwargs):
    """This method adds extra variables to template"""
    # get original context data from parent class
    context = super(StudentList, self).get_context_data(**kwargs)
    # tell template not to show logo on a page
    context['show_logo'] = False
    # return context mapping
    return context
  def get_queryset(self):
    """Order students by last_name."""
    # get original query set
    qs = super(StudentList, self).get_queryset()
    # order by last name
    return qs.order_by('last_name')










##########################################################################

#stud_add
 
#crispy

class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(StudentCreateForm,self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

            # return HttpResponseRedirect(
            #     u'%s?status_message=5' %  reverse('main'))


        # set form tag attributes
        self.helper.form_action = reverse('s_add')
        # self.helper.form_action = u'%s?status_message=5' % reverse('s_add')

        self.helper.form_method = 'POST'
        self.helper.form_class = 'col-sm-12 form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-8 input-group'

        # add buttons
        # self.helper.layout.fields.append(self)
        self.helper.layout.fields.append(FormActions(
            Submit('add_button', (u'Зберегти'), css_class="btn btn-primary"),
            Submit('cancel_button', (u'Скасувати'), css_class="btn btn-link"),
)) 


class StudentCreate(CreateView):
  model = Student
  template_name = 'students/students_add.html'
  form_class = StudentCreateForm
  def get_success_url(self):
    return u'%s?status_message=Студента успішно створено!' % reverse('main')
  def post(self, request, *args, **kwargs):
    if request.POST.get('cancel_button'):
      return HttpResponseRedirect(u'%s?status_message=Створення студента відмінено!'% reverse('main'))
    else:
      return super(StudentCreate, self).post(request, *args, **kwargs)
    




#########################################################

#stud_edit

   #crispy
class StudentUpdateForm(ModelForm):
  class Meta:
    model = Student
  def __init__(self, *args, **kwargs):
      super(StudentUpdateForm, self).__init__(*args, **kwargs)
      self.helper = FormHelper(self)
      # set form tag attributes
      self.helper.form_action = reverse('students_edit',kwargs={'pk': kwargs['instance'].id})
      self.helper.form_method = 'POST'
      self.helper.form_class = 'form-horizontal'
      # set form field properties
      self.helper.help_text_inline = True
      self.helper.html5_required = True
      self.helper.label_class = 'col-sm-2 control-label'
      self.helper.field_class = 'col-sm-10'
      # add buttons
      self.helper.layout.fields.append(FormActions(
        Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
        Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
      ))



class StudentUpdate(UpdateView):
  model = Student
  template_name = 'students/students_edit.html'
  form_class = StudentUpdateForm
  def get_success_url(self):
    return u'%s?status_message=Студента успішно збережено!' % reverse('main')
  def post(self, request, *args, **kwargs):
    if request.POST.get('cancel_button'):
      return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!'% reverse('main'))
    else:
      return super(StudentUpdate, self).post(request, *args, **kwargs)




##############################################################

#stud_delete
class StudentDelete(DeleteView):
  model = Student
  template_name = 'students/students_delete.html'
  def get_success_url(self):
    return u'%s?status_message=Студента успішно видалено!' % reverse('main')
  



