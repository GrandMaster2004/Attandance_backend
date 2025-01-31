import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_attachment(receiver_email, sender_email, password, subject, content, file_path):
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject

  # Attach the text content
  message.attach(MIMEText(content, "plain"))

  # Attach the file
  with open(file_path, "rb") as file:
    message.attach(MIMEApplication(file.read(), Name=file_path))

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(sender_email, password)
  server.sendmail(sender_email, receiver_email, message.as_string())
  server.quit()

# Example usage
receiver_email = "yashvardhangond95@gmail.com"
sender_email = "eurekadigital6@gmail.com"
password = "yags nldl objv doyv"
subject = "Email with attachment"
content = "This is the content of the email."
file_path = "output_cse.xlsx"  # Replace with the actual path to your file

send_email_with_attachment(receiver_email, sender_email, password, subject, content, file_path)
print("Email sent successfully!")