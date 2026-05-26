import os
import subprocess
import json
import re
import time

EXCLUDED = [
    "5 Advance Prompt Engineering For Agents",
    "7 MCP and RAG"
]

TIMEOUT = 5
BASE_DIR = os.getcwd()

projects = []
results = []


def get_order(path):
    rel = os.path.relpath(path, BASE_DIR)

    m = re.search(r'(\d+(\.\d+)?)', rel)

    if m:
        return float(m.group(1))

    return 999


# -----------------------------------
# Find projects containing main.py
# -----------------------------------

for root, dirs, files in os.walk(BASE_DIR):

    dirs[:] = [
        d for d in dirs
        if d not in EXCLUDED
    ]

    if "main.py" in files:
        projects.append(root)


projects.sort(key=get_order)

print("\n========== RUNNING ==========\n")


for project in projects:

    project_name = os.path.relpath(project)

    print(f"\nRunning : {project_name}")

    result = {
        "project": project_name,
        "status": "",
        "error": ""
    }

    try:

        # -----------------------------------
        # Check requirements.txt
        # -----------------------------------

        requirements = os.path.join(
            project,
            "requirements.txt"
        )

        if os.path.exists(requirements):

            print("Checking requirements...")

            check = subprocess.run(
                [
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "--dry-run",
                    "-r",
                    requirements
                ],
                capture_output=True,
                text=True
            )

            output = (
                check.stdout +
                check.stderr
            ).lower()

            if "would install" in output:

                print("Installing requirements.txt...")

                install = subprocess.run(
                    [
                        "python",
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        requirements
                    ],
                    capture_output=True,
                    text=True
                )

                if install.returncode != 0:

                    result["status"] = "FAIL"
                    result["error"] = install.stderr[:500]

                    print("Requirements installation FAILED")

                    results.append(result)
                    continue

                print("Requirements installed")

            else:

                print("Requirements already installed")

        else:

            print("No requirements.txt found")


        # -----------------------------------
        # Run main.py
        # -----------------------------------

        proc = subprocess.Popen(
            ["python", "main.py"],
            cwd=project,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        time.sleep(TIMEOUT)

        if proc.poll() is None:

            result["status"] = "PASS"

            print("PASS")

            proc.kill()

        else:

            stdout, stderr = proc.communicate()

            if proc.returncode == 0:

                result["status"] = "PASS"

                print("PASS")

            else:

                result["status"] = "FAIL"

                result["error"] = (
                    stderr[:500]
                    if stderr
                    else stdout[:500]
                )

                print("FAIL")


    except Exception as e:

        result["status"] = "FAIL"
        result["error"] = str(e)

        print("FAIL")


    results.append(result)


# -----------------------------------
# Save results
# -----------------------------------

with open("results.json", "w") as f:

    json.dump(
        results,
        f,
        indent=4
    )


print("\nResults saved -> results.json")