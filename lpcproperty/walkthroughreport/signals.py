from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import WalkthroughReport

@receiver(post_save, sender=WalkthroughReport)
def notify_client_on_report_create(sender, instance, created, **kwargs):
    if not created:
        return

    client = instance.user
    if not client.email:
        return

    subject = "New Walkthrough Report Created"

    text_content = (
        f"Date: {instance.datetime.strftime('%Y-%m-%d')}\n"
        f"Property Address: {instance.property.address if instance.property else 'N/A'}\n"
        f"Description: {instance.description or 'N/A'}"
    )

    html_content = f"""
    <div style="background:#eef2f7;padding:40px 0;font-family:Inter,Arial,Helvetica,sans-serif;">
    <div style="
        max-width:620px;
        margin:0 auto;
        background:#ffffff;
        border-radius:12px;
        box-shadow:0 10px 25px rgba(0,0,0,0.08);
        overflow:hidden;
    ">

        <!-- Header -->
        <div style="background:#1e3a8a;padding:22px 30px;color:#ffffff;">
        <h2 style="margin:0;font-weight:600;">
            Walkthrough Report Created
        </h2>
        </div>

        <!-- Body -->
        <div style="padding:30px;color:#1f2937;">
        <table style="width:100%;border-collapse:collapse;">
            <tr>
            <td style="padding:10px 0;font-weight:600;width:160px;color:#374151;">Date</td>
            <td style="padding:10px 0;">{instance.datetime.strftime('%Y-%m-%d')}</td>
            </tr>
            <tr>
            <td style="padding:10px 0;font-weight:600;color:#374151;">Property Address</td>
            <td style="padding:10px 0;">{instance.property.address if instance.property else 'N/A'}</td>
            </tr>
            <tr>
            <td style="padding:10px 0;font-weight:600;color:#374151;vertical-align:top;">Description</td>
            <td style="padding:10px 0;">{instance.description or 'N/A'}</td>
            </tr>
        </table>

        <!-- Button -->
        <div style="text-align:center;margin-top:30px;">
            <a href="https://backend.lotuspmc.com/login/"
            style="
                display:inline-block;
                background:#1e3a8a;
                color:#ffffff;
                text-decoration:none;
                padding:12px 26px;
                border-radius:6px;
                font-weight:600;
            ">
            Login to View Report
            </a>
        </div>
        </div>

        <!-- Footer -->
        <div style="background:#f1f5f9;padding:16px 30px;font-size:12px;color:#64748b;">
        Please log in to your dashboard to review the full walkthrough details and take any required action , This is an automated notification. Please do not reply.
        </div>

    </div>
    </div>
    """
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [client.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
