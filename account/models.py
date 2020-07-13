from django.db import models

class Account(models.Model):
    email_account  = models.URLField(unique = True)
    password       = models.CharField(max_length = 200, null = True)
    name           = models.CharField(max_length = 50, null = True)
    profile_image  = models.URLField(max_length = 2000, null = True)
    birthdate      = models.DateTimeField(null = True)
    created_at     = models.DateTimeField(auto_now_add = True)
    updated_at     = models.DateTimeField(auto_now = True, null = True)
    social_media   = models.ForeignKey('SocialMedia', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.email_account

class SocialMedia(models.Model):
    name = models.CharField(max_length = 50)
    icon = models.URLField(null = True)

    class Meta:
        db_table = 'social_media'

    def __str__(self):
        return self.name

