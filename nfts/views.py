from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import Project


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'nfts/project.html'

    def get_context_data(self, **kwargs):
        project = self.get_object()
        nfts = project.nfts.all()

        context = super().get_context_data(**kwargs)
        context['nfts'] = nfts

        return context
