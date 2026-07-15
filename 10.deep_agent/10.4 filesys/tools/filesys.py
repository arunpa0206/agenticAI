# ====================================================
# FILESYSTEM STORAGE SERVICE
# ====================================================

import json
import os
import csv


# ====================================================
# TICKET FILE WRITER
# ====================================================

def create_ticket_file(booking_data, ticket_dir, flight_id):
    """
    Creates a user-readable plain text flight ticket file
    containing key booking details.
    """
    ticket_file = f"{ticket_dir}/{flight_id}_ticket.txt"
    with open(ticket_file, "w", encoding="utf-8") as file:
        file.write("FLIGHT TICKET\n\n")
        for k, v in booking_data.items():
            file.write(f"{k}: {v}\n")


# ====================================================
# JSON RECORD WRITER
# ====================================================

def create_json_record(booking_data, booking_dir, flight_id):
    """
    Saves a structured JSON file containing all booking information.
    """
    json_file = f"{booking_dir}/{flight_id}.json"
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(booking_data, file, indent=4)


# ====================================================
# CSV LOG UPDATER
# ====================================================

def update_csv_record(booking_data, booking_dir):
    """
    Appends the booking transaction row to the central booking_records.csv log file.
    Creates the header row if the file does not exist yet.
    """
    csv_file = f"{booking_dir}/booking_records.csv"
    exists = os.path.exists(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=booking_data.keys())
        if not exists:
            writer.writeheader()
        writer.writerow(booking_data)


# ====================================================
# MAIN RECORD ORCHESTRATION
# ====================================================

def create_external_records(state):
    """
    Decomposes and orchestrates writing the booking records to
    multiple file formats (txt, json, csv).
    """
    plan = state["travel_plan"]
    customer = state["customer"]

    # Base directories for file exports
    base = "external_storage"
    ticket_dir = f"{base}/tickets"
    booking_dir = f"{base}/booking_records"

    # Ensure targeted output directories exist
    os.makedirs(ticket_dir, exist_ok=True)
    os.makedirs(booking_dir, exist_ok=True)

    # Construct the final booking schema data
    booking_data = {
        **plan,
        **customer,
        "payment_status": state["payment_status"],
        "booking_status": "CONFIRMED"
    }

    # Execute individual sub-writers
    create_ticket_file(booking_data, ticket_dir, plan["flight_id"])
    create_json_record(booking_data, booking_dir, plan["flight_id"])
    update_csv_record(booking_data, booking_dir)

    return "External files created"


# ====================================================
# WRAPPER FOR BACKWARD COMPATIBILITY
# ====================================================

class FileService:
    """
    Static service container to map legacy calls to the new decomposed
    module-level functional layout.
    """
    @staticmethod
    def create_external_records(state):
        return create_external_records(state)