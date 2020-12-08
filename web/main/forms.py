from django import forms
from django.conf import settings
from django.core.files.storage import default_storage
import os, random, string

class UploadForm(forms.Form):
  """PDFアップロード用フォーム"""
  """saveメソッドはアップロードしたPDFを一時フォルダに保存する。"""
  document = forms.FileField(label="PDFアップロード",
    widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

  def save(self):
    upload_files = self.files.getlist('document')
    # 一時フォルダの生成
    temp_dir = os.path.join(settings.MEDIA_ROOT, self.create_dir(10))
    for pdf in upload_files:
      # 一時フォルダに保存
      default_storage.save(os.path.join(temp_dir, pdf.name), pdf)
    return temp_dir

  def create_dir(self, n):
    """一時フォルダ命名生成関数"""
    return 'pdf\\' + ''.join(random.choices(string.ascii_letters + string.digits, k=n))