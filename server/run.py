import os
import subprocess
import time
import requests
import json

# set the GitHub repository URL and the path to the local repository
github_repo = 'https://github.com/<username>/<repository>.git'
local_repo = '/path/to/local/repo'

# set the command to run the code from the local repository
run_command = 'python main.py'

# set the loop delay in seconds
loop_delay = 60

# set the Pushbullet API key and device ID
api_key = '<your_pushbullet_api_key>'
device_id = 'uju2QWs1fK8sjzBZpUJ99E'

# initialize the process and error variables
process = None
error = False

# function to send a Pushbullet notification
def send_notification(title, message):
    headers = {
        'Access-Token': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'note',
        'title': title,
        'body': message
    }
    url = 'https://api.pushbullet.com/v2/devices/' + device_id + '/pushes'
    response = requests.post(url, headers=headers, data=json.dumps(data))

while True:
    try:
        # check if user input is available
        if os.isatty(0):
            # if user input is available, prompt for action
            action = input('\nDo you want to (u)pdate or (s)top the program? ')

            if action.lower() == 'u':
                # if the user wants to update, pull the latest code
                subprocess.call(['git', 'pull'], cwd=local_repo)
                send_notification('Code updated', 'The code has been updated from GitHub.')

            elif action.lower() == 's':
                # if the user wants to stop, kill the process and exit the loop
                if process is not None:
                    process.kill()
                send_notification('Program stopped', 'The program has been stopped by the user.')
                break

        # kill the previous process, if it exists
        if process is not None:
            process.kill()

        # run the code from the local repository in the background
        subprocess.call(['nohup', 'sh', '-c', run_command + ' > log.txt 2>&1 &'], cwd=local_repo)

        # reset the error flag
        error = False

        # wait for the loop delay
        time.sleep(loop_delay)

    except KeyboardInterrupt:
        # if the user interrupts the program, prompt for action
        action = input('\nDo you want to (u)pdate or (s)top the program? ')

        if action.lower() == 'u':
            # if the user wants to update, pull the latest code and restart the loop
            subprocess.call(['git', 'pull'], cwd=local_repo)
            send_notification('Code updated', 'The code has been updated from GitHub.')

        elif action.lower() == 's':
            # if the user wants to stop, kill the process and exit the loop
            if process is not None:
                process.kill()
            send_notification('Program stopped', 'The program has been stopped by the user.')
            break

        else:
            # if the user enters an invalid action, continue the loop
            continue

    except:
        # if an error occurs, set the error flag and send a notification
        error = True
        send_notification('Error', 'An error has occurred in the program.')

    if error:
        # if an error occurred in
        # check if the process is running
        process_running = False
        for line in subprocess.check_output(['ps', '-ef']).splitlines():
            if run_command.encode() in line:
                process_running = True
                break

        if not process_running:
            # if the process is not running, set the error flag and send a notification
            error = True
            send_notification('Error', 'The program is not running.')


    if error:
        # if an error occurred, kill the process and restart the loop
        if process is not None:
            process.kill()
        time.sleep(5)
        continue
