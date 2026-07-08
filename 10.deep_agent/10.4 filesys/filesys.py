import json
import os
import csv


class FileService:


    @staticmethod
    def create_external_records(
        state
    ):

        plan = state[
            "travel_plan"
        ]

        customer = state[
            "customer"
        ]


        BASE = (
            "external_storage"
        )

        TICKET = (
            f"{BASE}/tickets"
        )

        BOOKING = (
            f"{BASE}/booking_records"
        )


        os.makedirs(
            TICKET,
            exist_ok=True
        )

        os.makedirs(
            BOOKING,
            exist_ok=True
        )


        booking_data = {

            **plan,

            **customer,

            "payment_status":
            state[
                "payment_status"
            ],

            "booking_status":
            "CONFIRMED"
        }


        ticket_file=(

            f"{TICKET}/"
            f"{plan['flight_id']}_ticket.txt"
        )


        with open(
            ticket_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "FLIGHT TICKET\n\n"
            )

            for k,v in booking_data.items():

                file.write(
                    f"{k}: {v}\n"
                )


        json_file=(

            f"{BOOKING}/"
            f"{plan['flight_id']}.json"
        )


        with open(
            json_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                booking_data,
                file,
                indent=4
            )


        csv_file=(

            f"{BOOKING}/booking_records.csv"
        )


        exists=os.path.exists(
            csv_file
        )


        with open(
            csv_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer=csv.DictWriter(

                file,

                fieldnames=
                booking_data.keys()
            )

            if not exists:

                writer.writeheader()

            writer.writerow(
                booking_data
            )


        return (

            "External files created"
        )