from django.db import models

class Category(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 50)
    sub_category = models.ForeignKey(SubCategory, on_delete = models.CASCADE)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

class Posting(models.Model):
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    account    = models.ForeignKey('account.Account', on_delete = models.CASCADE) 

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    content    = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)
    posting    = models.ForeignKey(Posting, on_delete = models.CASCADE)
    account    = models.ForeignKey('account.Account', on_delete = models.CASCADE, related_name = 'comments_wrote', null = True)
    likes      = models.ManyToManyField('account.Account', through = 'LikeComment')

    class Meta:
        db_table = 'comments'

class LikeComment(models.Model):
    account = models.ForeignKey('account.Account', on_delete = models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)

    class Meta:
        db_table = 'like_comments'
