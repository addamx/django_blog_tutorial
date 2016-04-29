from django.shortcuts import render,get_object_or_404, render_to_response,redirect
from django.http import HttpResponse, Http404
from article.models import Article

from django.contrib.syndication.views import Feed

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.paginator(paginator.num_pages)
        
    return render(request, 'home.html', {'post_list':post_list})

def detail(request, id):
    post = get_object_or_404(Article, id=str(id))
    return render_to_response('post.html', {'post':post})

def archives(request):
    post_list = Article.objects.all()
    return render_to_response('archives.html', \
                              {'post_list': post_list, 'error':False})

def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact = tag)
    except Article.DoesNotExist:
        raise Http404
    return render_to_response('archives.html',{'post_list':post_list})

def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            post_list = Article.objects.filter(title__icontains = s)
            if len(post_list) == 0:
                return render_to_response('archives.html', {'post_list':post_list, 'error':True})
            else:
                return render_to_response('archives.html', {'post_list':post_list, 'error':False})
    return redirect('/')
    
# RSS    
class RSSFeed(Feed):
    title = 'RSS feed - article'
    link = 'feeds/posts/'
    description = 'RSS feed - blog posts'
    
    def items(self):
        return Article.objects.order_by('-date_time')
    
    def item(self):
        return Article.objects.order_by('-date_time')
        
    def item_title(self, item):
        return item.title
        
    def item_pubdate(self, item):
        return item.date_time
        
    def item_description(self, item):
        return item.content
