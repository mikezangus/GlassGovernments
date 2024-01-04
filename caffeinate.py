import subprocess


def start_caffeinate():
    print("Starting caffeinate")
    process = subprocess.Popen(["caffeinate"])
    return process


def stop_caffeinate(process):
    print("Stopping caffeinate")
    process.terminate()