import os
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NotificationManager:
    """Manages sending notifications via different channels (email, SMS, WhatsApp)"""
    
    def __init__(self):
        """Initialize notification channels with credentials from environment variables"""
        # Email configuration
        self.smtp_address = os.environ.get("EMAIL_PROVIDER_SMTP_ADDRESS")
        self.email = os.environ.get("MY_EMAIL")
        self.email_password = os.environ.get("MY_EMAIL_PASSWORD")
        
        # Twilio configuration
        self.twilio_sid = os.environ.get('TWILIO_SID')
        self.twilio_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_virtual_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self.twilio_verified_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
        self.whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER")
        
        # Validate required environment variables
        self._validate_config()
        
        # Set up Twilio client
        self.client = Client(self.twilio_sid, self.twilio_token)
    
    def _validate_config(self):
        """Validate that all required configuration variables are present"""
        required_vars = [
            "EMAIL_PROVIDER_SMTP_ADDRESS", "MY_EMAIL", "MY_EMAIL_PASSWORD",
            "TWILIO_SID", "TWILIO_AUTH_TOKEN", "TWILIO_VIRTUAL_NUMBER", 
            "TWILIO_VERIFIED_NUMBER", "TWILIO_WHATSAPP_NUMBER"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
            print("Some notification methods may not work correctly.")

    def send_sms(self, message_body):
        """
        Send SMS notification via Twilio
        
        Args:
            message_body: Text message to send
        """
        try:
            message = self.client.messages.create(
                from_=self.twilio_virtual_number,
                body=message_body,
                to=self.twilio_verified_number
            )
            print(f"SMS sent successfully (SID: {message.sid})")
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False

    def send_whatsapp(self, message_body):
        """
        Send WhatsApp notification via Twilio
        
        Args:
            message_body: Text message to send
        """
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                body=message_body,
                to=f'whatsapp:{self.twilio_verified_number}'
            )
            print(f"WhatsApp message sent successfully (SID: {message.sid})")
            return True
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
            return False

    def send_emails(self, email_list, email_body):
        """
        Send email notifications to a list of recipients
        
        Args:
            email_list: List of recipient email addresses
            email_body: Email message content
        """
        # Skip if no recipients
        if not email_list:
            print("No recipients provided for email notification")
            return
        
        try:
            # Create SMTP connection
            with smtplib.SMTP(self.smtp_address) as connection:
                connection.starttls()
                connection.login(self.email, self.email_password)
                
                # Format email message
                message = f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                
                # Send to each recipient
                successful = 0
                for email in email_list:
                    try:
                        connection.sendmail(
                            from_addr=self.email,
                            to_addrs=email,
                            msg=message
                        )
                        successful += 1
                    except Exception as e:
                        print(f"Failed to send email to {email}: {e}")
                
                print(f"Successfully sent {successful} out of {len(email_list)} emails")
                
        except Exception as e:
            print(f"Email service error: {e}")