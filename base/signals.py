from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea
from django.conf import settings

@receiver(post_save, sender=Tarea)
def enviar_email_tarea_completada(sender, instance, created, **kwargs):
    if not created and instance.estado == 'completada':
        equipo = instance.proyecto.equipo
        emails = [integrante.email for integrante in equipo.integrantes.all() if integrante.email]

        if emails:
            send_mail(
                subject=f'La tarea: {instance.contenido} ',
                message = f'La tarea {instance.id} ha sido completada correctamente, el encargado {instance.asignado_a} cumplio su objetivo'  ,  
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )