from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_share(request, post_id):
    #Pobranie posta na podstawie jego identyfikatora.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #Formularz zostal wyslany.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Weryfikacja pól formularza zakończyła się powodzeniem...
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {} \n\n Komentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

            #...więc mozna wysłać wiadomość.
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #Trzy posty na kadej stronie 
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #Jezeli zmienna page nie jest liczba calkowita,
        #wowczas pobierana jest pierwsza strona wynikow.
        posts = paginator.page(1)
    except EmptyPage:
        #Jezeli zmienna page ma wartosc wieksza niz numer ostatniej strony
        #wynikow, wtedy pobierana jest ostatnia strona wynikow.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day =day)
    return render(request,'blog/post/detail.html', {'post':post})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
# Create your views here.
