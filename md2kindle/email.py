"""Email utility for sending files to Kindle devices."""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from pathlib import Path
from dotenv import load_dotenv


def send_to_kindle(output_file, args):
    """Send the converted file to a Kindle device via email.
    
    Args:
        output_file: Path to the converted file
        args: Command line arguments
    """
    load_dotenv()
    
    # Get email configuration from environment
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    kindle_email = os.getenv('KINDLE_EMAIL')
    
    # Check if all required env vars are set
    if not all([email_address, email_password, smtp_server, kindle_email]):
        print("Error: Missing email configuration in .env file.")
        print("Make sure EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, and KINDLE_EMAIL are set.")
        sys.exit(1)
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = kindle_email
    msg['Date'] = formatdate(localtime=True)
    
    # Set subject line to book title if available
    if args.title:
        msg['Subject'] = args.title
    else:
        msg['Subject'] = Path(output_file).stem
    
    # Attach converted file
    with open(output_file, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(output_file)}"')
        msg.attach(part)
    
    # Send email
    try:
        print(f"Sending {output_file} to {kindle_email}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)
        server.quit()
        print("File sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        sys.exit(1)