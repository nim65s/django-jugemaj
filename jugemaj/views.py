from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from ndh.mixins import SuperUserRequiredMixin

from .forms import ElectionForm, VoteFormSet
from .models import Candidate, Election, NamedCandidate, Vote


class ElectionDetailView(DetailView):
    model = Election


class ElectionListView(ListView):
    model = Election


class ElectionCreateView(SuperUserRequiredMixin, CreateView):
    model = Election
    form_class = ElectionForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CandidateCreateView(LoginRequiredMixin, CreateView):
    model = NamedCandidate
    fields = ("name",)

    def form_valid(self, form):
        ret = super().form_valid(form)
        election = get_object_or_404(Election, slug=self.kwargs.get("slug"))
        Candidate.objects.create(election=election, content_object=form.instance)
        return ret

    def get_success_url(self):
        return get_object_or_404(Election, slug=self.kwargs.get("slug")).get_absolute_url()


@login_required
def vote(request, slug):
    election = get_object_or_404(Election, slug=slug)
    candidates = {}
    for candidate in election.candidate_set.all():
        Vote.objects.get_or_create(elector=request.user, candidate=candidate)
        candidates[candidate.pk] = candidate.content_object.name
    votes = Vote.objects.filter(elector=request.user, candidate__election=election)
    if request.method == "POST":
        formset = VoteFormSet(request.POST, queryset=votes)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Votre vote a été enregistré")
            return redirect(election)
        messages.error(request, "Corrigez les erreurs")
    else:
        formset = VoteFormSet(queryset=votes)
    return render(request, "jugemaj/vote.html", {"formset": formset, "candidates": candidates})
