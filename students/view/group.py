# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.group import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.student import Student
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, Button




#########################################################################
#group_list
class GroupList(ListView):
  model = Group
  context_object_name = 'groups'
  template_name = 'students/grup.html'
  def get_context_data(self, **kwargs):
    """This method adds extra variables to template"""
    # get original context data from parent class
    context = super(GroupList, self).get_context_data(**kwargs)
    # tell template not to show logo on a page
    context['show_logo'] = False
    # return context mapping
    return context
  def get_queryset(self):
    """Order groups by title."""
    # get original query set
    qs = super(GroupList, self).get_queryset()
    # order by title
    return qs.order_by('title')



##########################################################################

#group_add
 
#crispy

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(GroupCreateForm,self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

            # return HttpResponseRedirect(
            #     u'%s?status_message=5' %  reverse('main'))


        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
        # self.helper.form_action = u'%s?status_message=5' % reverse('groups_add')

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


class GroupCreate(CreateView):
  model = Group
  template_name = 'students/groups_add.html'
  form_class = GroupCreateForm
  def get_success_url(self):
    return u'%s?status_message=Групу успішно створено!' % reverse('groups')
  def post(self, request, *args, **kwargs):
    if request.POST.get('cancel_button'):
      return HttpResponseRedirect(u'%s?status_message=Створення групи відмінено!'% reverse('groups'))
    else:
      return super(GroupCreate, self).post(request, *args, **kwargs)






##################################################################################

#group_edit

   #crispy
class GroupUpdateForm(ModelForm):
  class Meta:
    model = Group
  def __init__(self, *args, **kwargs):
      super(GroupUpdateForm, self).__init__(*args, **kwargs)
      self.helper = FormHelper(self)
      # set form tag attributes
      self.helper.form_action = reverse('groups_edit',kwargs={'pk': kwargs['instance'].id})
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



class GroupUpdate(UpdateView):
  model = Group
  template_name = 'students/groups_edit.html'
  form_class = GroupUpdateForm
  def get_success_url(self):
    return u'%s?status_message=Групу успішно відредаговано!' % reverse('groups')
  def post(self, request, *args, **kwargs):
    if request.POST.get('cancel_button'):
      return HttpResponseRedirect(u'%s?status_message=Редагування групи відмінено!'% reverse('groups'))
    else:
      return super(GroupUpdate, self).post(request, *args, **kwargs)



####################################################################################

#group delete

class GroupDelete(DeleteView):
  model = Group
  template_name = 'students/groups_delete.html'
  def get_success_url(self):
    return u'%s?status_message=Групу успішно видалено!' % reverse('groups')
  def post(self, request, *args, **kwargs):
    if request.POST.get('no_delete_button'):
      return HttpResponseRedirect(u'%s?status_message=Видалення  групи відмінено!'% reverse('groups'))
    else:
      try:
        return super(GroupDelete, self).post(request, *args, **kwargs)
      except:
        return HttpResponseRedirect( u'%s?status_message=Видалення  неможливе,  оскілки  в  даній  групі  є  студенти. Будь - ласка, спочатку  видаліть  студентів!'  % reverse('groups'))  
    
