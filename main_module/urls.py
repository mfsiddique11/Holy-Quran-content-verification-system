from django.conf.urls import url
from . import views
from . import about
from . import references
from . import ourwork
from . import developers
app_name='main_module'
urlpatterns = [
    url('' , views.index , name='main_module_index'),
    #path('results/' , viewsR.results , name='result'),
    url('about/' , about.about ),
    url('references/' , references.references ),
    url('ourwork/' , ourwork.ourwork ),
    url('developers/' , developers.developers ),
]
