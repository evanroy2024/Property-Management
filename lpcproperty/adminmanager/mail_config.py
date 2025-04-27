from .models import MailConfiguration

def get_mail_settings():
    mail_config = MailConfiguration.objects.first()
    if mail_config:
        return {
            'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST': mail_config.email_host,
            'EMAIL_PORT': mail_config.email_port,
            'EMAIL_USE_TLS': mail_config.use_tls,
            'EMAIL_USE_SSL': mail_config.use_ssl,
            'EMAIL_HOST_USER': mail_config.email_host_user,
            'EMAIL_HOST_PASSWORD': mail_config.email_host_password,
            'DEFAULT_FROM_EMAIL': mail_config.default_from_email,
        }
    else:
        return None
