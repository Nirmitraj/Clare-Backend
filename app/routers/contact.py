# app/routers/contact.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
from typing import Sequence
import smtplib, ssl, certifi

from app.config import settings

router = APIRouter(prefix="/contact", tags=["Public"])

class ContactIn(BaseModel):
    fullName: str
    phone: str
    email: EmailStr
    state: str
    youAre: str
    inquiry: str
    message: str = ""
    consentTxn: bool = False
    consentMkt: bool = False
    page: str | None = None
    submittedAt: str | None = None

def _send_email(data: ContactIn) -> None:
    smtp_host = settings.smtp_host
    smtp_port = int(settings.smtp_port or 587)
    smtp_user = settings.smtp_user
    smtp_pass = settings.smtp_pass
    smtp_from = settings.smtp_from or "no-reply@clareseniorcare.store"

    # recipients (allow string or list in future)
    recipients: Sequence[str] = []
    if settings.smtp_to:
        recipients = [settings.smtp_to] if isinstance(settings.smtp_to, str) else list(settings.smtp_to)
    if not recipients:
        recipients = ["info@clareseniorcare.store"]

    if not all([smtp_host, smtp_user, smtp_pass]):
        raise RuntimeError("SMTP not configured (SMTP_HOST/USER/PASS).")

    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = f"Clare Contact: {data.fullName} · {data.inquiry}".strip()
    msg["Reply-To"] = data.email

    html = f"""\
<h2>New Contact Form Submission</h2>
<p><b>Name:</b> {data.fullName}</p>
<p><b>Email:</b> {data.email}</p>
<p><b>Phone:</b> {data.phone}</p>
<p><b>State:</b> {data.state}</p>
<p><b>You are:</b> {data.youAre}</p>
<p><b>Inquiry:</b> {data.inquiry}</p>
<p><b>Message:</b><br>{(data.message or '').replace('\n','<br/>')}</p>
<hr>
<p><b>Transactional consent:</b> {data.consentTxn}</p>
<p><b>Marketing consent:</b> {data.consentMkt}</p>
<p><b>Page:</b> {data.page or '-'}</p>
<p><b>Submitted at:</b> {data.submittedAt or '-'}</p>
"""
    msg.set_content("HTML email required.")
    msg.add_alternative(html, subtype="html")

    ctx = ssl.create_default_context(cafile=certifi.where())

    if smtp_port == 465:
        # SMTPS
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ctx, timeout=20) as s:
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)
    else:
        # STARTTLS (typical on 587)
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as s:
            s.starttls(context=ctx)
            s.login(smtp_user, smtp_pass)
            s.send_message(msg)

@router.post("", status_code=status.HTTP_202_ACCEPTED)
def submit_contact(payload: ContactIn, bg: BackgroundTasks):
    try:
        bg.add_task(_send_email, payload)   # send in background
        return {"ok": True, "queued": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
