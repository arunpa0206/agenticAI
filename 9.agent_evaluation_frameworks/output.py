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


        thresholds = data.get("thresholds") or {}
        t_success = thresholds.get("success_rate", 80)
        t_tool = thresholds.get("tool_accuracy", 80)
        t_steps = thresholds.get("average_steps", 3)
        t_policy = thresholds.get("policy_compliance", 80)

        final_results.append({

            "intent":data["intent"],

            "metrics":{

                "success_rate":{

                    "value":success_rate,

                    "status":
                    "PASS"
                    if success_rate>=t_success
                    else "FAIL"
                },

                "tool_accuracy":{

                    "value":tool_rate,

                    "status":
                    "PASS"
                    if tool_rate>=t_tool
                    else "FAIL"
                },

                "average_steps":{

                    "value":average_steps,

                    "status":
                    "PASS"
                    if average_steps<=t_steps
                    else "FAIL"
                },

                "policy_compliance":{

                    "value":policy_rate,

                    "status":
                    "PASS"
                    if policy_rate>=t_policy
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