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
from django.contrib.auth.decorators import login_required

import shutil, os

# Create your views here.
def index(request):
  if request.user.is_authenticated:
    return render(request, 'main/index.html')
  else:
    return HttpResponseRedirect("accounts/login")

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

  def form_invalid(self, form):
      return render(self.request, 'main/upload.html', {'form': form})

class ListView(LoginRequiredMixin, generic.TemplateView):

  template_name = 'main/list.html'

  def get_context_data(self, **kwargs):
    # 継承先のメソッドを呼び出す
    context = super().get_context_data(**kwargs)
    # context[""] = 
    """自分が作成したExcelだけ表示"""
    login_user_name = self.request.user.username
    if not default_storage.exists(os.path.join(settings.MEDIA_ROOT, "excel", login_user_name)):
      warning_message = "このユーザーでは一度もファイル作成が行われていません。"
      context = {
        'warning_message': warning_message,
      }
      return context
    file_list = default_storage.listdir(os.path.join(settings.MEDIA_ROOT, "excel", login_user_name))[1]
    context = {
      'file_list': file_list,
      'login_user_name': login_user_name,
    }
    return context

@login_required
def dell_file(request):
  #CheckBox=Onのファイル名を取得
  checks_value = request.POST.getlist('checks')
  #ログインユーザー名を取得
  login_user_name = request.user.username

  #Excelファイルの格納パスを取得
  if checks_value:
    for file in checks_value:
      path = os.path.join(settings.MEDIA_ROOT, "excel", login_user_name, file)
      #CheckBox=ONのファイルをサーバから削除
      default_storage.delete(path)
    return render(request, 'main/delete.html', {'checks_value': checks_value})
  else:
    login_user_name = request.user.username
    file_list = default_storage.listdir(os.path.join(settings.MEDIA_ROOT, "excel", login_user_name))[1]
    warning_message = "削除対象ファイルが選択されていません。"

    context = {
      'file_list': file_list,
      'login_user_name': login_user_name,
      'warning_message': warning_message,
    }
    return render(request, 'main/list.html', context)