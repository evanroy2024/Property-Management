from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from sms_service import SlickTextSMSService

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
    <div style="background:#eef2f7;padding:40px 0;font-family:Roboto,Arial,Helvetica,sans-serif;">
      <div style="
          max-width:640px;
          margin:0 auto;
          background:#ffffff;
          border-radius:14px;
          box-shadow:0 10px 25px rgba(0,0,0,0.08);
          overflow:hidden;
      ">

        <!-- HEADER -->
        <div style="
            background:#1e3a8a;
            padding:30px 40px;
            color:#ffffff;
            display:flex;
            align-items:flex-start;
        ">
          <img src="https://backend.lotuspmc.com/static/logo.png"
               alt="Logo"
               style="height:60px;">

          <div style="
              font-size:16px;
              font-weight:500;
              margin-top:17px;
              margin-left:85px;
          ">
            Thank you for contacting us
          </div>
        </div>

        <!-- TITLE -->
        <div style="padding:28px 40px 10px 40px;">
          <div style="
              background:#1e3a8a;
              color:#ffffff;
              padding:20px 26px;
              border-radius:8px;
              font-size:18px;
              font-weight:600;
          ">
            Service Request Submittal Confirmed
          </div>
        </div>

        <!-- CONTENT -->
        <div style="padding:24px 40px;color:#1f2937;">
          <table style="width:100%;border-collapse:collapse;">
            {rows_html}
          </table>

          <div style="text-align:center;margin-top:36px;">
            <a href="https://backend.lotuspmc.com/login/"
               style="
                 display:inline-block;
                 background:#cfe9f6;
                 color:#000000;
                 text-decoration:none;
                 padding:16px 38px;
                 border-radius:8px;
                 font-weight:600;
                 font-size:14px;
               ">
              {button_text}
            </a>
          </div>
        </div>

        <!-- FOOTER -->
        <div style="background:#f1f5f9;padding:18px 40px;font-size:12px;color:#64748b;">
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

def send_sms_notifications(client, property_obj, service_name, sms_message):
    sms = SlickTextSMSService()

    # ---- CLIENT SMS ----
    if client and client.phone_number:
        sms.create_contact(
            phone_number=client.phone_number,
            first_name=client.first_name,
            last_name=client.last_name,
            email=client.email
        )
        sms.send_sms(client.phone_number, sms_message)

    # ---- MANAGER SMS ----
    if property_obj:
        managers = []

        if property_obj.client_manager and property_obj.client_manager.phone_number:
            managers.append(property_obj.client_manager)

        if property_obj.secondary_client_manager and property_obj.secondary_client_manager.phone_number:
            managers.append(property_obj.secondary_client_manager)

        for manager in managers:
            sms.create_contact(
                phone_number=manager.phone_number,
                first_name=manager.first_name,
                last_name=manager.last_name,
                email=manager.email
            )
            sms.send_sms(manager.phone_number, sms_message)

def notify_service(instance, service_name, details_rows):
    client = instance.user
    property_obj = PropertyManagement.objects.filter(client=client).first()

    # =====================
    # COMMON ROWS (EMAIL)
    # =====================
    common_rows = f"""
    <tr><td style="padding:10px 0;font-weight:600;width:160px;">Client</td>
        <td style="padding:10px 0;">{client.first_name} {client.last_name}</td></tr>

    <tr><td style="padding:10px 0;font-weight:600;">Email</td>
        <td style="padding:10px 0;">{client.email}</td></tr>

    <tr><td style="padding:10px 0;font-weight:600;">Property</td>
        <td style="padding:10px 0;">{property_obj.address if property_obj else 'N/A'}</td></tr>
    """

    full_email_rows = common_rows + details_rows

    # =====================
    # EMAIL HTML
    # =====================
    html_content = build_email(
        title=f"{service_name} Submitted",
        rows_html=full_email_rows,
        button_text="Login to View Details",
    )

    # =====================
    # SMS TEXT (SAME DATA)
    # =====================
    def html_to_text(html):
        import re
        text = re.sub(r'<.*?>', '', html)
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        formatted = []
        i = 0
        while i < len(lines) - 1:
            formatted.append(f"{lines[i]}: {lines[i+1]}")
            i += 2

        return "\n".join(formatted)


    sms_message = f"""
{service_name} Submitted

{html_to_text(full_email_rows)}

Login:
https://backend.lotuspmc.com/login
""".strip()

    # ---- CLIENT EMAIL ----
    if client.email:
        email = EmailMultiAlternatives(
            f"{service_name} Submitted",
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
            email = EmailMultiAlternatives(
                f"New {service_name}",
                service_name,
                settings.DEFAULT_FROM_EMAIL,
                manager_emails,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

    # ---- SMS ----
    send_sms_notifications(client, property_obj, service_name, sms_message)

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
