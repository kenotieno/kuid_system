from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentID
from django.core.mail import send_mail

@receiver(post_save, sender=StudentID)
def send_id_found_notification(sender, instance, created, **kwargs):
    if instance.status == 'FOUND':
        subject = f"ID Found Notification: {instance.id_number}"
        message = f"""
        The following ID has been marked as found:
        
        ID Number: {instance.id_number}
        Student Name: {instance.student_name}
        Found By: {instance.found_by or 'Anonymous'}
        Found Date: {instance.found_date}
        
        Please contact the administration to claim it.
        """
        
        # Send to admin or appropriate recipient
        send_mail(
            subject,
            message,
            'from@example.com',
            ['admin@example.com'],
            fail_silently=False,
        )