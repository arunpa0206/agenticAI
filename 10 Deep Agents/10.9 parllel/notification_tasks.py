# notification_tasks.py

import random
import time

notification_results={}

def generate_ticket(
    flight
):

    time.sleep(1)

    notification_results[
        "ticket"
    ]=f"""
BOOKING CONFIRMED

Airline : {flight['airline']}
Flight : {flight['flight']}
Price : {flight['price']}
Gate : G{random.randint(1,15)}
Seat : {random.randint(1,30)}A
"""

def send_confirmation_email():
    time.sleep(1)

def update_booking_record():
    time.sleep(1)