import subprocess


def start_caffeinate():
    process = subprocess.Popen(["caffeinate"])
    return process


def stop_caffeinate(process):
    process.terminate()