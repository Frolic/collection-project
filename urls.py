from django.contrib import admin

from django.conf import settings
from django.conf.urls.defaults import *

#from main.views import save_profile,save_theme,add_idea,add_comment, list_articles, list_ideas, login_user,logout_user, list_comments,list_idea_comments,add_idea_comment, idea_vote_up,idea_vote_down,new_user,activate_user
#from catalogue.views import list_coins, show_catalogue, convert_coins

import django.views.static

admin.autodiscover()
import os.path

PROJECT_ROOT = os.path.dirname(__file__)

urlpatterns = patterns('',
 #Static
 (r'^.*captchas/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/captchas')}),
 (r'^.*img/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/img')}),
 (r'^.*css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/css')}),
 (r'^.*js/(?P<path>.*)$', 'django.views.static.serve',{'document_root': os.path.join(PROJECT_ROOT,'media/js')}),

 #Catalogue
 (r'^convert_coins$', 'catalogue.views.convert_coins'),
 (r'^katalog(\d*)$', 'catalogue.views.show_catalogue'),
 (r'^katalog/coins$', 'catalogue.views.list_coins', {}, 'custom_list'),
 (r'^coin/add_to_catalogue/(\d+)$', 'catalogue.views.add_to_catalogue', {}, 'add_to_catalogue'),
 (r'^coin/info/(\d+)/$', 'catalogue.views.coin_info', {}, 'coin_info'), 
 #Site features
 (r'^$', 'main.views.list_articles'),
 (r'^vote/up/(\d+)$', 'main.views.idea_vote_up'),
 (r'^vote/down/(\d+)$', 'main.views.idea_vote_down'),
 
 (r'^ideas/$', 'main.views.list_ideas'),
 (r'^idea/add_comment$', 'main.views.add_idea_comment'),
 (r'^idea/add_idea$', 'main.views.add_idea'),
 (r'^idea/comments/(\d+)$', 'main.views.list_idea_comments'),
 
 (r'^comments/(\d+)$', 'main.views.list_comments'),
 (r'^add_comment$', 'main.views.add_comment'),
 #User
 (r'^login$', 'main.views.login_user'),
 (r'^logout$', 'main.views.logout_user'),
 (r'^user_settings/save$', 'main.views.save_profile'),
 (r'^user_settings/save/(\d+)$', 'main.views.save_theme'),
 (r'^new_user$', 'main.views.new_user'),
 (r'^activate_user/(\w+)/(\d+)$', 'main.views.activate_user'),



    # Example:
    # (r'hours_ahead^collection/', include('collection.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),



)

if settings.DEBUG:
    from os.path import join, dirname
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

