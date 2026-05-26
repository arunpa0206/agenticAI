import json


def generate_output(results):


    final_results=[]


    for id,data in results.items():

        count=data["count"]


        success_rate=round(

            data["success_total"]/count,
            2
        )

        tool_rate=round(

            data["tool_total"]/count,
            2
        )

        average_steps=round(

            data["step_total"]/count,
            2
        )

        policy_rate=round(

            data["policy_total"]/count,
            2
        )


        final_results.append({

            "id":data["id"],

            "intent":data["intent"],

            "metrics":{

                "success_rate":{

                    "value":success_rate,

                    "status":
                    "PASS"
                    if success_rate>=80
                    else "FAIL"
                },

                "tool_accuracy":{

                    "value":tool_rate,

                    "status":
                    "PASS"
                    if tool_rate>=80
                    else "FAIL"
                },

                "average_steps":{

                    "value":average_steps,

                    "status":
                    "PASS"
                    if average_steps<=3
                    else "FAIL"
                },

                "policy_compliance":{

                    "value":policy_rate,

                    "status":
                    "PASS"
                    if policy_rate>=80
                    else "FAIL"
                }

            }

        })


    with open(

        "output.json",
        "w"

    ) as f:

        json.dump(
            final_results,
            f,
            indent=4
        )