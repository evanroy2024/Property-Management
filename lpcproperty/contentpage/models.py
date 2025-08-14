from django.db import models

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('account', 'Account'),
        ('billing', 'Billing'),
        ('technical', 'Technical'),
        ('general', 'General'),
        ('services', 'Services'),
        ('membership', 'Membership'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def __str__(self):
        return self.question


from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/')
    comment = models.TextField()

    def __str__(self):
        return self.name

from django.db import models

class UserMessage(models.Model):
    NEED_CHOICES = [
        ('management', 'Property Management'),
        ('maintenance', 'Maintenance'),
        ('rental', 'Rental Inquiry'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    need_type = models.CharField(max_length=50, choices=NEED_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.need_type}"
