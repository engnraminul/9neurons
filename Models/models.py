from django.db import models
from Login.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sub_Category, self).save(*args, **kwargs)

class Model(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Reject", "Reject"),
        ("Aprove", "Aprove"),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True, blank=True)
    content = RichTextUploadingField(blank=False, null=False)
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS, default="Pending", max_length=20)
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    class Meta:
        ordering = ['publish_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Model, self).save(*args, **kwargs)
    

class Files(models.Model):
    model_name = models.ForeignKey(Model, on_delete=models.CASCADE)
    file = models.FileField(upload_to= 'files', null=True, blank=True)