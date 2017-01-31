try:
    import subprocess, platform, sys, time, os
except:
    print("Check that all dependencies are installed...")
def init(type):
    global debug
    if type == "cold":
        debug = False
        print("Rootella is starting cold.")
    else:
        print("Rootella is starting warm")
    global version
    time.sleep(0.1)
    version = "1.0 ALPHA"
    print("Rootella " + version)
    print(" ██╗ ██╗ ██████╗  ██████╗  ██████╗ ████████╗███████╗██╗     ██╗      █████╗ ")
    print("████████╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝██╔════╝██║     ██║     ██╔══██╗")
    print("╚██╔═██╔╝██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██║     ██║     ███████║")
    print("████████╗██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██║     ██║     ██╔══██║")
    print("╚██╔═██╔╝██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗███████╗███████╗██║  ██║")
    print(" ╚═╝ ╚═╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝")
    time.sleep(1)
    if debug == True:
        print("Bebug mode started virtual device mouted.")
    if platform.system() == "Windows":
        print("#################################\nWindows Detected. Rootella only works on Linux and MacOS.\nWe suggest Nexus Root Toolkit for Windows\nor you can use Ubuntu on Windows.\n#################################")
        sys.exit()
    if os.getuid() != 0:
        sys.exit("############\nPlease run Rootella as sudo\nsudo python rootella.py\n############")
    else:
        print("-- You are root --")
        if type == "cold":
            print("Spinning up Android Developer Bridge Daemon...")
            execute("adb start-server")
            global devices
            devices = []
        else:
            print("ADB Already running.")
        startupChecks()
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
    global debug
    global devices
    if debug == False:
        cmds = 3
    else:
        cmds = 4
    size = executeR("stty size")
    print(size)
    for i in range(int(size[0])):
        print("\n")
    hash = "#"
    for i in range(int(size[1])):
        hash = hash + "#"
    hash = hash[1:]
    print(hash)
    if debug == True:
        string = "PLATFORM: " + platform.system().rstrip().upper() + " | DEBUG | " + devices[1]
    else:
        string = "PLATFORM: " + platform.system().rstrip().upper() + " | " + devices[1]
    stdout(string.rjust(int(size[1])))
    stdout('#rootella V: {0}'.format(version))
    sys.stdout.flush()
    print()
    print("0. Quit")
    print("1. Reboot")
    print("990. Restart Rootella")
    if debug == True:
        print("999. Debug Menu")
    for i in range(int(size[0]) - 4 - cmds):
        print("")
    print(hash)
    select = int(input("Selection> "))
    if select == 0:
        sys.exit("Thanks for using Rootella, see you soon!")
    if select == 1:
        reboot()
    if select == 990:
        print("Restart now...")
        time.sleep(1)
        init("warm")
    if select == 999:
        if debug == True:
            print("--Debug Menu--\n1. Add another device and restart\n2. Update Entry\n3. Device List\n4. Exit Debug\n--------------")
            answer = int(input("Option> "))
            if answer == 1:
                answer = input("Device name> ")
                devices.append('ADB')
                devices.append(answer.upper())
                devices.append("AUTHORIZED")
                print("Calling restart...")
                time.sleep(1)
                init("warm")
            if answer == 2:
                print(devices)
                loc = int(input("Entry?> "))
                new = str(input("New content?> "))
                devices[loc] = new
                print(devices)
                print("Devices list updated.")
                answer = input("Preform startup checks? [Y/N]?> ").upper()
                if answer == "Y":
                    startupChecks()
                else:
                    menu()
            if answer == 3:
                print("Devices (Includes virtual devices): ")
                print(devices)
                input("Press enter to continue")
                menu()
            if answer == 4:
                print("Exiting debug mode. Rootella will do a full cold restart and search for ADB/Fastboot devices...")
                time.sleep(2)
                debug = False
                init("cold")
def deviceLoc():
    running = execute("adb devices")
    print(running)
    if len(running) == 0:
        fastboot = execute("fastboot devices")
        print(fastboot)
        if len(fastboot) < 2:
            return False
        arr = ["FASTBOOT"]
        for i in running:
            arr.append(i)
        return arr
    else:
        arr = ['RUNNING']
        for i in running:
            arr.append(i)
        if arr == ['RUNNING', '']:
            return False
        return arr
def startupChecks():
    global devices
    global debug
    if debug == True:
        print("Device list (Contains Virtual Device): ")
        print(devices)
        time.sleep(1)
    if len(devices) > 3:
        print("We've detected more than one device\nPlease only connect the device you want to use the toolkit with. Unplug the others.")
        input("Press ENTER to continue...\n################################")
        if debug == True:
            print("You're running in debug mode with multiple devices, we'll automatically remove the device named " + devices[1] + " and rescan.")
            devices.remove(devices[0])
            devices.remove(devices[1])
            devices.remove(devices[2])
        startupChecks()
    if debug == False:
        devices = deviceLoc()
    if devices == False and debug == False:
        print("No devices where detected. Please make sure it's connected, on and developer options are enabled.")
        answer = input("Press enter to continue. CTRL C to exit. Or type DEBUG to force the startup. \n").upper()
        if answer == "DEBUG":
            if devices != False:
                devices.append('RUNNING', 'VIRTUALDEVICE01', 'AUTHORIZED')
                print(devices)
            else:
                devices = ['RUNNING', 'VIRTUALDEVICE01', 'AUTHORIZED']
            debug = True
            print("Restarting Rootella...")
            time.sleep(1)
            init("warm")
        startupChecks()
    if devices[2] == "unauthorized":
        print("#################################")
        print("Looks like your device is unauthorized\nPlease authorize this computer on your phone now.\nWe suggest ticking 'Always allow from this computer' to stop errors/crashes.")
        input("Press ENTER to continue...\n################################")
        if debug == True:
            print("You're in debug mode with an unauthorized device.")
        startupChecks()
    time.sleep(2)
    menu()
init("cold")
