from django.db import models

from bloggy import settings


class Comment(models.Model):
    post = models.ForeignKey('bloggy.Article', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', blank=True,
                             null=True)
    parent = models.ForeignKey('self', related_name='reply_set', null=True, on_delete=models.PROTECT)
    comment_content = models.TextField()
    comment_author_name = models.TextField(null=True, blank=True)
    comment_author_email = models.TextField(null=True, blank=True)
    comment_author_url = models.TextField(null=True, blank=True)
    comment_author_ip = models.GenericIPAddressField(default="0.0.0.0", null=True, blank=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['comment_date']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment_content, self.user.get_full_name() if self.user else '-')

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
