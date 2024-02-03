from taggit.models import Tag


class TagMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

# class PermissionRequiredMixin:
#     def get(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseRedirect(reverse_lazy('accounts:login'))
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseRedirect(reverse_lazy('accounts:login'))
#         return super().post(request, *args, **kwargs)
