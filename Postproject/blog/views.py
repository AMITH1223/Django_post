from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.shortcuts import redirect
from .forms import PostForm
import csv
import chardet
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer


# Viewing of Post list
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

# Viewing of Post list in detail
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

# Post creation from forms
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

# post edit part from forms
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

 # Post uploading
def post_bulk_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        try:
            raw_data = csv_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] if result['encoding'] else 'utf-8'
            file_data = raw_data.decode(encoding).splitlines()
            reader = csv.reader(file_data)
            for row in reader:
                title, content, author_id = row
                author = User.objects.get(pk=author_id)
                Post.objects.create(title=title, content=content, author=author)
        except UnicodeDecodeError:
            return render(request, 'post_bulk_upload.html', {'error': 'File encoding error. Please upload a valid CSV file.'})
        except Exception as e:
            return render(request, 'post_bulk_upload.html', {'error': str(e)})
        return redirect('post_list')
    return render(request, 'post_bulk_upload.html')

# create a post by api
class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Retrive or destroy the post detail
class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer