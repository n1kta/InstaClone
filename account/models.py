from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile_user', on_delete=models.CASCADE, blank=True, null=True)
    date_of_birthday = models.DateField(auto_now_add=True)
    avatar_image = ImageField(upload_to='users/%Y/%m/%d', default='/Users/nikitalebediev/Downloads/account.png')

    def take_avatar_image(self):
        return self.avatar_image

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} Follows {self.user_to}'


User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))
