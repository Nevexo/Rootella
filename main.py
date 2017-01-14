print("Rootella is starting cold.")
version = "1.0 ALPHA"
import subprocess, platform, sys, time, os
print(" ██╗ ██╗ ██████╗  ██████╗  ██████╗ ████████╗███████╗██╗     ██╗      █████╗ ")
print("████████╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██╔════╝██║     ██║     ██╔══██╗")
print("╚██╔═██╔╝██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██║     ██║     ███████║")
print("████████╗██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██║     ██║     ██╔══██║")
print("╚██╔═██╔╝██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗███████╗███████╗██║  ██║")
print(" ╚═╝ ╚═╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝")
if platform.system() == "Windows":
    print("#################################\nWindows Detected. Rootella only works on Linux and MacOS.\nWe suggest Nexus Root Toolkit for Windows\nor you can use Ubuntu on Windows.\n#################################")
    sys.exit()
if os.getuid() != 0:
    sys.exit("############\nPlease run Rootella as sudo\nsudo python rootella.py\n############")
def execute(arg):
    s = subprocess.check_output(arg.split()).decode("utf-8")
    if arg[0] != "fastboot":
        s = str(s[25:])
    s = str(s).rstrip()
    s = s.split('\t')
    return s
def executeR(arg):
    s = subprocess.check_output(arg.split()).decode("utf-8")
    s = s.rstrip()
    s = s.split(' ')
    return s
def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))   # \b: non-deleting backspace


def reboot():
    print("###########################")
    print("Reboot your Device\n1.Reboot System (Boot into Android)\n2.Reboot Fastboot (Reboot into bootloader)\n3.Reboot Recovery (Reboot into recovery)")
    print("###########################")
    reply = int(input("Selection> "))
    if reply == 1:
        print("Rebooting system...")
        executeR("adb reboot")
        menu()
    elif reply == 2:
        print("Rebooting to Fastboot.")
        execute("sudo adb reboot bootloader")
        menu()
    elif reply == 3:
        print("Rebooting into recovery...")
        executeR("adb reboot recovery")
        menu()
    else:
        print("Unknown selection...")
        time.sleep(1)
        menu()

def menu():
    cmds = 2
    size = executeR("stty size")
    print(size)
    for i in range(int(size[0])):
        print("\n")
    hash = "#"
    for i in range(int(size[1])):
        hash = hash + "#"
    hash = hash[1:]
    print(hash)
    string = "PLATFORM: " + platform.system().rstrip().upper()
    stdout(string.rjust(int(size[1])))
    stdout('#rootella V: {0}'.format(version))
    sys.stdout.flush()
    print()
    print("0. Quit")
    print("1. Reboot")
    for i in range(int(size[0]) - 4 - cmds):
        print("")
    print(hash)
    select = int(input("Selection> "))
    if select == 0:
        sys.exit("Thanks for using Rootella, see you soon!")
    if select == 1:
        reboot()
def deviceLoc():
    running = execute("adb devices")
    print(running)
    if len(running) < 2:
        fastboot = execute("fastboot devices")
        print(fastboot)
        if len(fastboot) < 2:
            return False
        arr = ["FASTBOOT"]
        arr.append(fastboot)
        return arr
    else:
        arr = ['RUNNING']
        arr.append(running)
        return arr
def startupChecks():

    devices = deviceLoc()
    if devices == False:
        print("No devices where detected. Please make sure it's connected, on and developer options are enabled.")
        input("Press enter to continue. CTRL C to exit.")
        startupChecks()
    if len(devices) > 3:
        print("We've detected more than one device\nPlease only connect the device you want to use the toolkit with. Unplug the others.")
        input("Press ENTER to continue...\n################################")
        startupChecks()
    if devices[2] == "unauthorized":
        print("#################################")
        print("Looks like your device is unauthorized\nPlease authorize this computer on your phone now.\nWe suggest ticking 'Always allow from this computer' to stop errors/crashes.")
        input("Press ENTER to continue...\n################################")
        startupChecks()
    time.sleep(2)
    menu()
print("Spinning up Android Developer Bridge Daemon...")
execute("adb start-server")
startupChecks()
