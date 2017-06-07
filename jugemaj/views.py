from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages


from .models import Election, Candidate, Vote
from .forms import VoteFormSet


class ElectionDetailView(DetailView):
    model = Election


class ElectionListView(ListView):
    model = Election


class ElectionCreateView(UserPassesTestMixin, CreateView):
    model = Election
    fields = ("title", "description", "end")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CandidateCreateView(LoginRequiredMixin, CreateView):
    model = Candidate
    fields = ("name",)

    def form_valid(self, form):
        form.instance.election = get_object_or_404(Election, slug=self.kwargs.get("slug"))
        return super().form_valid(form)


@login_required
def vote(request, slug):
    election = get_object_or_404(Election, slug=slug)
    candidates = {}
    for candidate in election.candidate_set.all():
        Vote.objects.get_or_create(elector=request.user, candidate=candidate)
        candidates[candidate.pk] = candidate.name
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
