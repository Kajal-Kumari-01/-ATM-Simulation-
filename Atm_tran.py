import streamlit as st
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Atm:
    def __init__(self):
        self.pin = "111612"
        self.balance = 0
        self.current_option = None
        self.email = "kajalkashyapsingh01@gmail.com"  # Set your default email here
        self.verification_code = None

    def menu(self):
        st.title("ATM Simulation")
        self.current_option = st.selectbox(
            "Choose an option", 
            ["Generate New PIN", "Change PIN", "Balance Enquiry", "Withdraw", "Exit"], 
            # key="menu_option_unique"
        )
        
        if self.current_option == "Generate New PIN":
            self.pin_generator()
        elif self.current_option == "Change PIN":
            self.pin_change()
        elif self.current_option == "Balance Enquiry":
            self.balance_enquiry()
        elif self.current_option == "Withdraw":
            self.withdrawal()
        elif self.current_option == "Exit":
            st.write("Exiting...")

    def pin_generator(self):
        new_pin = st.text_input("Enter your new PIN", type="password", key="new_pin_unique")
        new_balance = st.number_input("Enter your initial balance", min_value=0, key="new_balance_unique")
        
        if st.button("Set PIN and Balance", key="set_pin_unique"):
            if new_pin:
                self.pin = new_pin
                self.balance = new_balance
                st.success("PIN and balance set successfully.")
                # Send email notification for PIN generation
                if self.send_email_notification("PIN and balance set", self.email):
                    st.success("Email notification sent.")
                else:
                    st.error("Failed to send email.")
            else:
                st.error("PIN cannot be empty.")
            self.menu()

    def pin_change(self):
        old_pin = st.text_input("Enter your old PIN", type="password", key="old_pin_unique")
        new_pin = st.text_input("Enter your new PIN", type="password", key="new_pin_change_unique")
        user_email = st.text_input("Enter your email for verification", key="user_email_unique")
        
        if st.button("Send Verification Code", key="send_verification_unique"):
            if old_pin == self.pin:
                self.verification_code = random.randint(100000, 999999)  # Generate a random 6-digit code
                if self.send_email_verification(user_email, self.verification_code):
                    st.success("Verification code sent to your email.")
                else:
                    st.error("Failed to send email.")
            else:
                st.error("Incorrect old PIN.")
        
        verification_code_input = st.text_input("Enter the verification code sent to your email", key="verification_code_input_unique")

        if st.button("Change PIN", key="change_pin_unique"):
            if verification_code_input == str(self.verification_code):
                if new_pin:
                    self.pin = new_pin
                    st.success("PIN changed successfully.")
                    # Send email notification for PIN change
                    if self.send_email_notification("PIN changed", user_email):
                        st.success("Email notification sent.")
                    else:
                        st.error("Failed to send email.")
                else:
                    st.error("New PIN cannot be empty.")
            else:
                st.error("Incorrect verification code.")
            self.menu()

    def balance_enquiry(self):
        if st.button("Show Balance", key="show_balance_unique"):
            st.info(f"Your balance is {self.balance}. Your PIN is {self.pin}.")
            self.menu()

    def withdrawal(self):
        old_pin = st.text_input("Enter your PIN", type="password", key="withdraw_pin_unique")
        withdraw_amount = st.number_input("Enter amount to withdraw", min_value=0, key="withdraw_amount_unique")
        
        if st.button("Withdraw", key="withdraw_button_unique"):
            if old_pin == self.pin:
                if self.balance >= withdraw_amount:
                    self.balance -= withdraw_amount
                    st.success(f"Transaction successful. New balance: {self.balance}.")
                    # Send email notification for withdrawal
                    if self.send_email_notification(f"Withdrawal of amount {withdraw_amount}", self.email):
                        st.success("Email notification sent.")
                    else:
                        st.error("Failed to send email.")
                else:
                    st.error("Insufficient funds.")
            else:
                st.error("Incorrect PIN.")
            self.menu()

    def send_email_verification(self, to_email, verification_code):
        try:
            # Sender and receiver details
            sender_email = "ishika0870@gmail.com"  # Replace with your email
            password = "iflz geig vuyd pwfe"  # Use app-specific password or environment variable

            # Set up the email content
            subject = "ATM PIN Change Verification Code"
            body = f"Your verification code is: {verification_code}"

            # Create the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Send the email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, msg.as_string())
            return True
        except Exception as e:
            st.error(f"Error sending verification email: {e}")
            return False

    def send_email_notification(self, action, to_email):
        try:
            # Sender and receiver details
            sender_email = "ishika0870@gmail.com"  # Replace with your email
            password = "iflz geig vuyd pwfe"  # Use app-specific password or environment variable

            # Set up the email content
            subject = f"ATM Notification: {action}"
            body = f"Dear customer, your account has been updated: {action}.\n\nRegards,\nATM Team"

            # Create the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Send the email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, to_email, msg.as_string())
            return True
        except Exception as e:
            st.error(f"Error sending email notification: {e}")
            return False

# Create an instance of the Atm class and run the menu
atm = Atm()
atm.menu()

