import csv
import time
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

sender_email = os.environ.get('SENDER_EMAIL')
email_password = os.environ.get('EMAIL_PASSWORD')

# change the email subject here before sending
subject = "Get Certified in Molecular Docking – Limited Seats for December Batch" 

#read email body from email.txt
def read_email_content():
    try:
        with open('email-body.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: email-body.txt not found")
        return None
    except Exception as e:
        print(f"Error reading email-body.txt content: {e}")
        return None

#read emails.csv
def read_email_list():
    try:
        with open('emails.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            emails = [row[0].strip() for row in reader if len(row) >= 1 and row[0].strip() != '']
            return emails
    except FileNotFoundError:
        print("Error: emails.csv not found")
        return []
    except Exception as e:
        print(f"Error reading emails.csv: {e}")
        return []

#create and return smtp connection
def create_smtp_connection():
    try:
        server = smtplib.SMTP_SSL('smtpout.secureserver.net', 465)
        server.login(sender_email, email_password)
        return server
    except Exception as e:
        print(f"Error: Failed to create SMTP connection: {e}")
        return None

#send emails
def send_individual_email(server, recipient, content):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient
    msg.set_content(content)
    
    #attach poster image
    try:
        with open('poster.jpeg', 'rb') as img:
            img_data = img.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename='poster.jpeg')
    except FileNotFoundError:
        print("Warning: poster.jpeg not found, sending without attachment")
    except Exception as e:
        print(f"Warning: Could not attach image: {e}")
    
    try:
        server.send_message(msg)
        return True
    except Exception as e:
        return False, str(e)

def main():
    BATCH_SIZE = 25  # Number of emails before reconnecting
    EMAIL_DELAY = 2  # Seconds between individual emails
    BATCH_DELAY = 20  # Seconds between batches
    
    print("Starting individual email sending process...")
    
    # Read email content and list
    content = read_email_content()
    if not content:
        return
    
    emails = read_email_list()
    if not emails:
        return
    
    total_emails = len(emails)
    print(f"📧 Found {total_emails} email addresses")
    
    sent_count = 0
    failed_count = 0
    server = None
    
    for i, email in enumerate(emails, 1):
        # Create new connection at start or after each batch
        if i == 1 or (i - 1) % BATCH_SIZE == 0:
            if server:
                try:
                    server.quit()
                except:
                    pass
                time.sleep(BATCH_DELAY)
            
            print(f"\nCreating SMTP connection (Batch {((i-1) // BATCH_SIZE) + 1})")
            server = create_smtp_connection()
            if not server:
                print("Error: Failed to create SMTP connection. Stopping.")
                break
        
        # Send individual email
        result = send_individual_email(server, email, content)
        
        if result is True:
            sent_count += 1
            print(f"✅ Sent to {email} ({i}/{total_emails})")
        else:
            failed_count += 1
            error_msg = result[1] if isinstance(result, tuple) else "Unknown error"
            print(f"❌ Failed to send to {email}: {error_msg}")
            
            # Log failed email
            with open('failed_emails.log', 'a', encoding='utf-8') as log:
                log.write(f"{email} — {error_msg}\n")
        
        # Delay between emails (except for the last email)
        if i < total_emails:
            time.sleep(EMAIL_DELAY)
        
        # Progress update every batch
        if i % BATCH_SIZE == 0:
            print(f"Progress: {i}/{total_emails} processed (Sent: {sent_count}, Failed: {failed_count})")
    
    # Clean up connection
    if server:
        try:
            server.quit()
        except:
            pass
    
    # Final summary
    print(f"\nEmail sending complete!")
    print(f"Final Results:")
    print(f"Total emails: {total_emails}")
    print(f"Successfully sent: {sent_count}")
    print(f"Failed: {failed_count}")
    
    if failed_count > 0:
        print(f"Check 'failed_emails.log' for details on failed emails")

if __name__ == "__main__":
    main()
