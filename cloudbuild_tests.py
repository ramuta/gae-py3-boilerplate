import os
import sys
import subprocess
import time
import urllib.request


# Function for checking if emulator started or not
def emulator_started(port="8002"):
    try:
        if urllib.request.urlopen("http://0.0.0.0:{}".format(port)).status == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


# Prepare the correct port number and the main command based on the user's input
print("Preparing to run tests.")
emulator_port = "8002"
os.environ["TESTING"] = "yes"

# Google Cloud Build does not add PyTest into path, that's why it needs to be called directly
if "gcloud" in sys.argv:
    main_command = "/builder/home/.local/bin/pytest -p no:warnings"
else:  # BitBucket pipelines
    main_command = "pytest -p no:warnings"

storage = "--no-store-on-disk"

# Run datastore emulator
emulator_command = 'gcloud beta emulators datastore start --consistency=1 {storage} --project=test ' \
                   '--host-port=0.0.0.0:{port}'.format(storage=storage, port=emulator_port)

run_datastore = subprocess.Popen(emulator_command.split(), stdout=subprocess.PIPE)

# wait for the Emulator to start
print("Checking if emulator has started yet...")
while not emulator_started(port=emulator_port):
    print("Emulator hasn't started yet. Let's wait 5 seconds and check again. (It may take a while, so please be patient.)")
    time.sleep(5)

print("Yaaay, the emulator is on! Now we can start our tests.")

run_main_command = subprocess.Popen(main_command.split(), stdout=subprocess.PIPE)
run_main_command.wait()  # wait for process to finish; this also sets the returncode variable inside 'res'

if run_main_command.returncode != 0:
    print("os.wait:exit status != 0\n")
else:
    print("os.wait:({},{})".format(run_main_command.pid, run_main_command.returncode))

# access the output from stdout
result = run_main_command.stdout.readlines()

for line in result:
    print(line.decode("utf-8"))

# print("after read: {}".format(result))

run_datastore.terminate()
run_main_command.terminate()

print("Tests completed.")
