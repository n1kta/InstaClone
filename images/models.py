from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from account.models import Profile


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images_user')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images_profile', blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dashboard_detail', args=[self.slug])

    def get_review(self):
        return self.post_review.filter(parent__isnull=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Image, related_name='post_review', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.text}"
