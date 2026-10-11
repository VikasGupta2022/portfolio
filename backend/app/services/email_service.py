import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

logger = logging.getLogger("uvicorn.error")

def send_email_notification(name: str, email: str, subject: str, message: str, ip: str = "unknown") -> bool:
    """
    Dispatches an email notification to the site owner (RECEIVER_EMAIL)
    whenever a new inquiry is submitted on the portfolio website.
    Uses SMTP (e.g. Gmail App Password, SendGrid, Resend) if configured in .env.
    """
    receiver = settings.RECEIVER_EMAIL
    smtp_host = getattr(settings, "SMTP_HOST", "")
    smtp_port = getattr(settings, "SMTP_PORT", 587)
    smtp_user = getattr(settings, "SMTP_USER", "")
    smtp_pass = getattr(settings, "SMTP_PASSWORD", "")

    # If SMTP is not configured, log and gracefully succeed
    if not (smtp_host and smtp_user and smtp_pass):
        logger.info(f"📬 Contact inquiry recorded from {name} ({email}) - Subject: {subject}. (SMTP not configured in .env)")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚀 Portfolio Inquiry: {subject} (from {name})"
        msg["From"] = f"Vikas Gupta Portfolio <{smtp_user}>"
        msg["To"] = receiver
        msg["Reply-To"] = email

        plain_text = f"""
New Portfolio Message:
----------------------------------------
From: {name} ({email})
Subject: {subject}
Client IP: {ip}

Message:
{message}
----------------------------------------
Sent from Vikas Gupta Portfolio Website
        """

        html_text = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <h2 style="color: #0ea5e9; margin-top: 0;">🚀 New Portfolio Inquiry</h2>
            <p style="font-size: 14px; color: #475569;">You have received a new message from your portfolio contact form:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                <tr>
                    <td style="padding: 8px; font-weight: bold; width: 100px; color: #334155;">Sender:</td>
                    <td style="padding: 8px; color: #0f172a;">{name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #334155;">Email:</td>
                    <td style="padding: 8px; color: #0f172a;"><a href="mailto:{email}">{email}</a></td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #334155;">Subject:</td>
                    <td style="padding: 8px; color: #0f172a;">{subject}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold; color: #334155;">IP Address:</td>
                    <td style="padding: 8px; color: #64748b;">{ip}</td>
                </tr>
            </table>
            <div style="background: #f8fafc; padding: 14px; border-left: 4px solid #0ea5e9; border-radius: 4px; margin-top: 14px;">
                <p style="margin: 0; white-space: pre-wrap; font-size: 15px; color: #1e293b;">{message}</p>
            </div>
            <p style="margin-top: 24px; font-size: 12px; color: #94a3b8;">Click 'Reply' in your email client to respond directly to {email}.</p>
        </div>
        """

        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_text, "html"))

        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)

        logger.info(f"✅ Email notification dispatched to {receiver} for inquiry #{subject}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to send SMTP email notification: {e}")
        return False
