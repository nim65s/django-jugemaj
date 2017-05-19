from django.conf.urls import url

from .views import ElectionCreateView, CandidateCreateView, vote, ElectionDetailView, ElectionListView


app_name = 'jugemaj'
urlpatterns = [
    # url(r'^$', ElectionListView.as_view(), name='elections'),
    # url(r'^election$', ElectionCreateView.as_view(), name='create_election'),
    url(r'^election/(?P<slug>[^/]+)/$', ElectionDetailView.as_view(), name='election'),
    url(r'^election/(?P<slug>[^/]+)/candidate$', CandidateCreateView.as_view(), name='create_candidate'),
    url(r'^election/(?P<slug>[^/]+)/vote$', vote, name='vote'),
]
