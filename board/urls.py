from django.conf.urls.defaults import *

urlpatterns = patterns('board.views', 
    (r'^$', 'main'),
    (r'^/api/', 'api'),
    (r'^/settings', 'settings'),
    (r'^/search/', 'search'),
    (r'^/(?P<section>\w+)/$', 'section'),
    (r'^/(?P<section>\w+)/p/(?P<page>\d+)$', 'section'),
    (r'^/(?P<section>\w+)/(?P<topic>\d+)$', 'topic'),
)

#2-ch.ru/b/30000
#2-ch.ru/b/31500 -> 2-ch.ru/b/30000#31500
#2-ch.ru/api/sections
#2-ch.ru/api/b/
#2-ch.ru/api/b/t/30000 - thread posts
#2-ch.ru/api/b/30000
#2-ch.ru/api/b/31500
