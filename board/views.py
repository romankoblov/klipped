from django.core.paginator import Paginator

def topic(request):
    """docstring for topic"""
    return 

def main(request):
    """docstring for topic"""
    pass
    
def settings(request):
    """docstring for topic"""
    pass
    
def search(request):
    """docstring for topic"""
    pass

def sections(request):
    """Gets list of board sections"""
    return Section.objects.all().order_by('slug')

def categories(request):
    """Gets list of board sections with categories: [b c d a aa ad]"""
    data = sections(request)
    g = {}
    for i in data: # group sections by their position
        try:
            k = i.pop(0)
            u[k].append(i)
        except KeyError:
            u.update({k : [i]})
    return sorted(g, key=lambda sect: sect.group.order)

def post(request, section, pid):
    """Gets post"""
    return Post.objects.filter(section__slug=section, pid=pid)
        
def section(request, section, page=1):
    """
    Gets 20 threads from current section with
    OP post and last 5 posts in each thread
    """
    onpage = 20
    lp = 5 # number of last posts
    threads = Thread.objects.filter(op_post__section=section).order_by('id')
    pt = Paginator(threads, onpage).page(page)
    posts = [Post.objects.filter(op_post__id=t)[:-lp] for t in pt]
    return posts
    
def thread(request, section, op_post):
    """Gets thread and its posts"""
    return Post.objects.filter(thread__id=int(op_post), section=section)
    