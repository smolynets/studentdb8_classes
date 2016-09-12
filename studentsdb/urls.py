"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from students.view.student import StudentList, StudentCreate, StudentUpdate, StudentDelete
from students.view.group import GroupList, GroupCreate, GroupUpdate, GroupDelete
from students.view.exams import ExamList,ExamCreate, ExamUpdate, ExamDelete

from students.view.contact_admin import ContactView
from django.conf.urls import patterns, include,url
from django.contrib import admin
from settings import MEDIA_ROOT, DEBUG


urlpatterns = patterns('',
# Students urls
url(r'^$', StudentList.as_view(), name='main'),
url(r'^vid$', 'students.view.journal.vid', name='journal'),
url(r'^stud_add$', StudentCreate.as_view(), name='s_add'),
url(r'^students/(?P<pk>\d+)/edit/$',StudentUpdate.as_view(), name='students_edit'),
url(r'^students/(?P<pk>\d+)/delete/$',StudentDelete.as_view(), name='students_delete'),
#Groups urls
url(r'^grup$', GroupList.as_view(), name='groups'),
url(r'^groups_add$', GroupCreate.as_view(), name='groups_add'),
url(r'^groups/(?P<pk>\d+)/edit/$',GroupUpdate.as_view(), name='groups_edit'),
url(r'^groups/(?P<pk>\d+)/delete/$',GroupDelete.as_view(), name='groups_delete'),
url(r'^admin/', include(admin.site.urls)),
#exams url
url(r'^exams$', ExamList.as_view(), name='exams'),
url(r'^exam_add$',ExamCreate.as_view(), name='exam_add'),
url(r'^exams/(?P<pk>\d+)/edit/$',ExamUpdate.as_view(), name='exam_edit'),
url(r'^exams/(?P<pk>\d+)/delete/$',ExamDelete.as_view(), name='exam_delete'),
# Contact Admin Form
url(r'^contact-admin/$', ContactView.as_view(),
name='contact_admin'),
)
if DEBUG:
 # serve files from media folder
 urlpatterns += patterns('',
 url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
 'document_root': MEDIA_ROOT}))
