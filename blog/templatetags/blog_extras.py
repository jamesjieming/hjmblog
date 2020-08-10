from django import template
from django.db.models import Count

from blog.models import Post, Category, Tag

register = template.Library()


# 最新文章模版标签
# show_recent_posts 标签可以接收参数，默认为 5，即显示 5 篇文章，
# 如果要控制其显示 10 篇文章，可以使用 {% show_recent_posts 10 %} 这种方式传入参数。
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list':Post.objects.all().order_by('-created_time')[:num],
    }


# 归档模版标签
# 这里 Post.objects.dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间（已去重），且是
# Python 的 date 对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是 created_time ，即 Post
# 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。例如我们写了 3 篇文章，
# 分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
# 那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


# 分类模版标签
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    # 这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，
    # 它会返回数据库中全部 Category 的记录，但同时它还会做一些额外的事情，
    # 在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。
    # 代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），
    # 然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


# 标签云模版标签
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }
