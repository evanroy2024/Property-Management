from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from propertydetails.models import PropertyManagement
from .models import (
    ServiceRequest,
    PrearrivalInformation,
    DepartureInformation,
    ConciergeServiceRequest,
)


# =========================
# COMMON EMAIL TEMPLATE
# =========================
def build_email(title, rows_html, button_text):
    return f"""
    <div style="background:#eef2f7;padding:40px 0;font-family:Inter,Arial,Helvetica,sans-serif;">
      <div style="
          max-width:620px;
          margin:0 auto;
          background:#ffffff;
          border-radius:12px;
          box-shadow:0 10px 25px rgba(0,0,0,0.08);
          overflow:hidden;
      ">

        <div style="background:#1e3a8a;padding:22px 30px;color:#ffffff;">
          <h2 style="margin:0;font-weight:600;">{title}</h2>
        </div>

        <div style="padding:30px;color:#1f2937;">
          <table style="width:100%;border-collapse:collapse;">
            {rows_html}
          </table>

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
              {button_text}
            </a>
          </div>
        </div>

        <div style="background:#f1f5f9;padding:16px 30px;font-size:12px;color:#64748b;">
          Our team will review this request and take action as required.
          <br>
          This is an automated notification. Please do not reply.
        </div>

      </div>
    </div>
    """


# =========================
# COMMON NOTIFIER
# =========================
def notify_service(instance, service_name, details_rows):
    client = instance.user
    property_obj = PropertyManagement.objects.filter(client=client).first()

    # ---- CLIENT EMAIL ----
    if client and client.email:
        subject = f"{service_name} Submitted"

        html_content = build_email(
            title=f"{service_name} Submitted",
            rows_html=details_rows,
            button_text="Login to View Details",
        )

        email = EmailMultiAlternatives(
            subject,
            service_name,
            settings.DEFAULT_FROM_EMAIL,
            [client.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    # ---- MANAGER EMAIL ----
    if property_obj:
        manager_emails = []

        if property_obj.client_manager and property_obj.client_manager.email:
            manager_emails.append(property_obj.client_manager.email)

        if property_obj.secondary_client_manager and property_obj.secondary_client_manager.email:
            manager_emails.append(property_obj.secondary_client_manager.email)

        if manager_emails:
            subject = f"New {service_name}"

            manager_rows = f"""
            <tr><td style="padding:10px 0;font-weight:600;width:160px;color:#374151;">Client</td>
                <td style="padding:10px 0;">{client.first_name} {client.last_name}</td></tr>
            <tr><td style="padding:10px 0;font-weight:600;color:#374151;">Email</td>
                <td style="padding:10px 0;">{client.email}</td></tr>
            <tr><td style="padding:10px 0;font-weight:600;color:#374151;">Property</td>
                <td style="padding:10px 0;">{property_obj.address}</td></tr>
            {details_rows}
            """

            html_content = build_email(
                title=f"New {service_name}",
                rows_html=manager_rows,
                button_text="Login to Dashboard",
            )

            email = EmailMultiAlternatives(
                subject,
                service_name,
                settings.DEFAULT_FROM_EMAIL,
                manager_emails,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()


# =========================
# SERVICE REQUEST
# =========================
@receiver(post_save, sender=ServiceRequest)
def service_request_notify(sender, instance, created, **kwargs):
    if not created:
        return

    rows = f"""
    <tr><td style="padding:10px 0;font-weight:600;width:160px;color:#374151;">Request Type</td>
        <td style="padding:10px 0;">{instance.request_type}</td></tr>
    <tr><td style="padding:10px 0;font-weight:600;color:#374151;">Description</td>
        <td style="padding:10px 0;">{instance.description}</td></tr>
    """
    notify_service(instance, "Service Request", rows)


# =========================
# PRE-ARRIVAL INFORMATION
# =========================
@receiver(post_save, sender=PrearrivalInformation)
def prearrival_notify(sender, instance, created, **kwargs):
    if not created:
        return

    rows = f"""
    <tr><td style="padding:10px 0;font-weight:600;width:160px;color:#374151;">Arrival Date</td>
        <td style="padding:10px 0;">{instance.arrival_date}</td></tr>
    <tr><td style="padding:10px 0;font-weight:600;color:#374151;">Arrival Time</td>
        <td style="padding:10px 0;">{instance.arrival_time}</td></tr>
    """
    notify_service(instance, "Pre-Arrival Information", rows)


# =========================
# DEPARTURE INFORMATION
# =========================
@receiver(post_save, sender=DepartureInformation)
def departure_notify(sender, instance, created, **kwargs):
    if not created:
        return

    rows = f"""
    <tr><td style="padding:10px 0;font-weight:600;width:160px;color:#374151;">Departure Date</td>
        <td style="padding:10px 0;">{instance.departure_date}</td></tr>
    <tr><td style="padding:10px 0;font-weight:600;color:#374151;">Departure Time</td>
        <td style="padding:10px 0;">{instance.departure_time}</td></tr>
    """
    notify_service(instance, "Departure Information", rows)


# =========================
# CONCIERGE SERVICE
# =========================
@receiver(post_save, sender=ConciergeServiceRequest)
def concierge_notify(sender, instance, created, **kwargs):
    if not created:
        return

    rows = f"""
    <tr><td style="padding:10px 0;font-weight:600;width:160px;color:#374151;">Description</td>
        <td style="padding:10px 0;">{instance.description}</td></tr>
    """
    notify_service(instance, "Concierge Service Request", rows)
