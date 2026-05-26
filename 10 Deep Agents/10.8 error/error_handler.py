# error_handler.py

import time


def handle_error():

    print(
        "\n[ERROR HANDLER]"
    )

    time.sleep(2)

    retry=int(
        time.time()
    )


    if retry % 2 != 0:

        print(
            "Recovered"
        )

        return {

            "status":
            "success"

        }


    print(
        "Retry failed"
    )

    return {

        "status":
        "error",

        "error_type":
        "SEARCH_FAILURE",

        "message":
        "Flight search unavailable"

    }