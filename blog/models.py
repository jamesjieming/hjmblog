import markdown
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
# 分类


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=70)
    body = models.TextField(verbose_name='正文')
    # 创建时间
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    # 修改时间
    modified_time = models.DateTimeField(verbose_name='修改时间')
    # 摘要
    excerpt = models.CharField(verbose_name='摘要', max_length=200, blank=True)
    # 分类外键一对多
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    # 标签外键
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 作者外键一对多
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    # 注意 views 字段的类型为 PositiveIntegerField，该类型的值只允许为正整数或 0，因为阅读量不可能为负值。
    views = models.PositiveIntegerField(default=0, editable=False)
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 这里生成摘要的方案是，先将 body 中的 Markdown 文本转为 HTML 文本，去掉 HTML 文本里的 HTML 标签，然后摘取文本的前 54 个字符作为摘要。
        # 去掉 HTML 标签的目的是防止前 54 个字符中存在块级 HTML 标签而使得摘要格式比较难看。可以看到很多网站都采用这样一种生成摘要的方式。
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'title']

    def __str__(self):
        return self.title
