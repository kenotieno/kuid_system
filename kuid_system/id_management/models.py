from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Staff'),
        (3, 'Admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class StudentID(models.Model):
    STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
        ('RETURNED', 'Returned'),
    ]
    
    id_number = models.CharField(max_length=20, unique=True, verbose_name="ID Number")
    student_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='FOUND')
    found_by = models.CharField(max_length=100, blank=True, null=True)
    found_date = models.DateField(blank=True, null=True)
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='claimed_ids'
    )
    date_claimed = models.DateTimeField(null=True, blank=True)
    lost_date = models.DateField(blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.id_number} - {self.student_name}"

    def save(self, *args, **kwargs):
        if not self.verification_code:
            import random
            self.verification_code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)
