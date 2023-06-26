from django.urls import path, re_path
from django.conf.urls import include

from users_new.views import UsersView, SingleUserView, ContactsView, ContactsViewList, UsersFirebaseView

urlpatterns = [
    re_path(r'^db/$', UsersView.as_view()),
    re_path(r'^(?P<pk>\d+)$', SingleUserView.as_view()),
    re_path(r'^contacts/(?P<pk>\d+)$', ContactsView.as_view()),
    re_path(r'^fire/$', UsersFirebaseView.as_view()),
    re_path(r'^contactsList/(?P<pk>\d+)$', ContactsViewList.as_view()),
]