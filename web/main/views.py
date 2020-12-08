from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import UploadForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .utils import create_excel
from django.conf import settings
from django.core.files.storage import default_storage

import shutil, os

# Create your views here.
def index(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
  # return HttpResponse(f'hello world')
  if request.user.is_authenticated:
    return render(request, 'main/index.html', {'posts': posts})
  else:
    return HttpResponseRedirect("accounts/login")

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'main/post_detail.html', {'post': post})

class UploadView(LoginRequiredMixin, generic.FormView):
  form_class = UploadForm
  template_name = 'main/upload.html'

  def form_valid(self, form):
    user_name = self.request.user.username
    user_dir = os.path.join(settings.MEDIA_ROOT, "excel", user_name)
    if not os.path.isdir(user_dir):
      os.makedirs(user_dir)
    temp_dir = form.save()
    # temp_dir = 0
    err = create_excel(temp_dir, user_name)
    if err:
        shutil.rmtree(temp_dir)
        context = {
          'err': err,
        }
        return render(self.request, 'main/complete.html', context)
    shutil.rmtree(temp_dir)
    _, file_list = default_storage.listdir(os.path.join(settings.MEDIA_ROOT, "excel", user_name))
    messege = "正常終了しました"
    context = {
      'file_list': file_list,
      'user_name': user_name,
      'message': messege,
    }
    return render(self.request, 'main/complete.html', context)

  def form_imvalid(self, form):
      return render(self.request, 'main/upload.html', {'form': form})