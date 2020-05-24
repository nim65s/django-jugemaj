"""Views for django-jugemaj."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ndh.mixins import NDHFormMixin, SuperUserRequiredMixin

from .forms import ElectionForm
from .models import Candidate, Election, NamedCandidate, Vote


class ElectionDetailView(DetailView):
    """View to detail an Election."""
    model = Election


class ElectionListView(ListView):
    """View to list Elections."""
    model = Election


class ElectionCreateView(SuperUserRequiredMixin, NDHFormMixin, CreateView):
    """View to create an Election."""
    model = Election
    form_class = ElectionForm

    def form_valid(self, form):
        """Set the election creator."""
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CandidateCreateView(LoginRequiredMixin, NDHFormMixin, CreateView):
    """View to create a Candidate to an Election."""
    model = NamedCandidate
    fields = ("name", )

    def form_valid(self, form):
        """Set the right Election for this Candidate."""
        ret = super().form_valid(form)
        election = get_object_or_404(Election, slug=self.kwargs.get("slug"))
        Candidate.objects.create(election=election, content_object=form.instance)
        return ret

    def get_success_url(self):
        """Redirect to the Election page."""
        return get_object_or_404(Election, slug=self.kwargs.get("slug")).get_absolute_url()


class VoteView(LoginRequiredMixin, NDHFormMixin, UpdateView):
    """Views to let users vote for a Candidate."""
    model = Vote
    fields = ("choice", )
