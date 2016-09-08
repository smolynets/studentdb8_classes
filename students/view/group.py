# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.group import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.student import Student
from django.views.generic import UpdateView, CreateView, ListView
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
        fields = ['title',
                  'leader',
                  'notes',]

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        # add buttons
        self.helper.layout[-1] = FormActions(
        Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
        Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
        )  


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








def groups_edit(request, pk):
    groups = Group.objects.filter(pk=pk)
    students = Student.objects.filter(student_group_id=groups)
    
    if request.method == "POST":
      data = Group.objects.get(pk=pk)
      students = Student.objects.all()
      # was form add button clicked?
      if request.POST.get('add_button') is not None:
        # errors collection
        errors = {}
        # data for group object
        
        data.notes = request.POST.get('notes', '').strip()
        
        
        # validate user input
        title = request.POST.get('title', '').strip()
        if not title:
          errors['title'] = u"Імʼя є обовʼязковим."
        else:
          data.title = title
        leader = request.POST.get('leader', '').strip()
        try:
          st = Student.objects.filter(pk=leader)
          data.leader = st[0]
        except:
            return HttpResponseRedirect( u'%s?status_message=Редагування групи скасовано!Група  не містить студентів!' % reverse('groups'))
          
        
        # save student
        if not errors:
          
          data.save()
          # redirect to students list
          return HttpResponseRedirect( u'%s?status_message=Групу успішно редаговано!'  % reverse('groups'))
        else:
          # render form with errors and previous user input
          return render(request, 'students/groups_edit.html',
          {'students': Student.objects.all().order_by('last_name'),'errors': errors})
      elif request.POST.get('cancel_button') is not None:
        # redirect to home page on cancel button
        return HttpResponseRedirect( u'%s?status_message=Редагування групи скасовано!' % reverse('groups'))
    else:
     # initial form render
     return render(request, 'students/groups_edit.html',
     {'pk': pk, 'group': groups[0], 'students': students})


def groups_delete(request, pk):
    groups = Group.objects.filter(pk=pk)
    
    if request.method == "POST":
        if request.POST.get('yes') is not None:
          try:
            groups.delete()
            return HttpResponseRedirect( u'%s?status_message=Групу  успішно  видалено!'  % reverse('groups'))
          except:
            return HttpResponseRedirect( u'%s?status_message=Видалення  неможливе,  оскілки  в  даній  групі  є  студенти. Будь - ласка, спочатку  видаліть  студентів!'  % reverse('groups'))
        elif request.POST.get('cancel_button') is not None:
          return HttpResponseRedirect( u'%s?status_message=Видалення  групи  скасовано!'  % reverse('groups'))
        
    else:
        return render(request,
                      'students/groups_delete.html',
                      {'pk': pk, 'group': groups[0]})



def groups_one(request, pk):
   gp = Group.objects.filter(pk=pk)
   students = Student.objects.filter(student_group_id=gp)
   if len(students) > 0:
     # try to order students list
     order_by = request.GET.get('order_by', '')
     if order_by in ('last_name', 'first_name', 'ticket', '#'):
       students = students.order_by(order_by)
       if request.GET.get('reverse', '') == '1':
         students = students.reverse()
     # paginate students
     paginator = Paginator(students, 3)
     page = request.GET.get('page')
     try:
       students = paginator.page(page)
     except PageNotAnInteger:
       # If page is not an integer, deliver first page.
       students = paginator.page(1)
     except EmptyPage:
       # If page is out of range (e.g. 9999), deliver
       # last page of results.
       students = paginator.page(paginator.num_pages)
     return render(request, 'students/groups_one.html',
       {'students': students, 'pk': pk, 'group': gp[0],})
   else:
     return render(request, 'students/groups_one_null.html',
       {'students': students, 'pk': pk, 'group': gp[0],})
