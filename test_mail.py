from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import asyncio

conf = ConnectionConfig(
    MAIL_USERNAME="mststudyai@gmail.com",
    MAIL_PASSWORD="asmhkoewnnabiokn",
    MAIL_FROM="yourgmail@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_test():
    message = MessageSchema(
        subject="Test Email",
        recipients=["mststudyai@gmail.com"],
        body="Hello bro this is test email",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

asyncio.run(send_test())