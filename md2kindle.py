#!/usr/bin/env python3
import os
import sys
import argparse
import smtplib
import tempfile
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from pathlib import Path
from dotenv import load_dotenv

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert Markdown files to Kindle format and send to device')
    parser.add_argument('markdown_file', help='Path to the Markdown file')
    parser.add_argument('--title', help='Book title (defaults to filename)')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--cover', help='Path to cover image')
    parser.add_argument('--format', choices=['epub', 'pdf'], default='epub', 
                        help='Output format (default: epub)')
    parser.add_argument('--no-send', action='store_true', help='Convert only, don\'t send via email')
    parser.add_argument('--output', help='Output file path (defaults to input file with new extension)')
    return parser.parse_args()

def check_dependencies():
    try:
        subprocess.run(['pandoc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: Pandoc is not installed or not in PATH.")
        print("Please install Pandoc: https://pandoc.org/installing.html")
        sys.exit(1)

def convert_markdown(args):
    input_file = Path(args.markdown_file)
    
    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.with_suffix(f'.{args.format}')
    
    # Build pandoc command
    cmd = ['pandoc', str(input_file), '-o', str(output_file), '--standalone']
    
    # Add metadata if provided
    if args.title:
        cmd.extend(['--metadata', f'title={args.title}'])
    else:
        cmd.extend(['--metadata', f'title={input_file.stem}'])
        
    if args.author:
        cmd.extend(['--metadata', f'author={args.author}'])
    
    # Add cover image if provided
    if args.cover and os.path.exists(args.cover):
        cmd.extend(['--epub-cover-image', args.cover])
    
    # Run pandoc
    try:
        print(f"Converting {input_file} to {output_file}...")
        subprocess.run(cmd, check=True)
        print(f"Conversion complete: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

def send_to_kindle(output_file, args):
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

def main():
    args = parse_arguments()
    
    # Check if input file exists
    if not os.path.exists(args.markdown_file):
        print(f"Error: File not found: {args.markdown_file}")
        sys.exit(1)
    
    # Check for pandoc
    check_dependencies()
    
    # Convert markdown to specified format
    output_file = convert_markdown(args)
    
    # Send to Kindle unless --no-send flag is used
    if not args.no_send:
        send_to_kindle(output_file, args)
    
    print("Done!")

if __name__ == "__main__":
    main()
