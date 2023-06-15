from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def get_date(post):
    return post['date']


# Create your views here.
class StartingPageView(ListView):
    model = Post
    template_name = 'Blog/index.html'
    ordering = ['date']
    context_object_name = "posts"

    def get_queryset(self):
        query = super().get_queryset()
        data = query[:3]
        return data


class AllPostsView(ListView):
    model = Post
    template_name = 'Blog/all_posts.html'
    ordering = ['-date']
    context_object_name = "posts"


class DetailPageView(View):
    def is_stored_post(self, request, post_id):
        stored_post = request.session["stored_posts"]
        if stored_post is not None:
            is_saved_for_later = post_id in stored_post
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        return render(request, 'Blog/post_details.html', {'post': post,
                                                          'comment_form': CommentForm(),
                                                          "is_saved_for_later": self.is_stored_post(request, post.id)
                                                          })

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))

        return render(request, 'Blog/post_details.html', {'post': post,
                                                          'comment_form': CommentForm(),
                                                          "is_saved_for_later": self.is_stored_post(request, post.id)
                                                          })


class ReadLaterView(View):

    def get(self, request):
        context = {}
        stored_posts_id = request.session.get("stored_posts")
        if stored_posts_id is None or len(stored_posts_id) == 0:
            context["posts"] = []
            context["has_posts"] = False

        else:
            posts = Post.objects.filter(id__in=stored_posts_id)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, 'Blog/stored_posts.html', context)

    def post(self, request, ):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
