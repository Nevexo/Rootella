try:
    import subprocess, platform, sys, time, os
except:
    print("Check that all dependencies are installed...")
def init(type):
    global debug
    if type == "cold":
        debug = False
        global supportedDevices
        print("Rootella is starting cold.")
        instance = open("supportedDevices.txt", "r")
        supportedDevices = []
        for line in instance.readlines():
            supportedDevices.append(line.rstrip())
    else:
        print("Rootella is starting warm")
    global version
    time.sleep(0.5)
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
        if type == "cold":
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
def clear():
    size = executeR("stty size")
    for i in range(int(size[0])):
        print("")
def r(string):
    clear()
    size = executeR("stty size")
    width2 = round(int(size[1])/2.5)
    width = ""
    for i in range(width2):
        width = width + " "
    print(width + " ██╗ ██╗ ██████╗")
    print(width + "████████╗██╔══██╗")
    print(width + "╚██╔═██╔╝██████╔╝")
    print(width + "████████╗██╔══██╗")
    print(width + "╚██╔═██╔╝██║  ██║")
    print(width + " ╚═╝ ╚═╝ ╚═╝  ╚═╝")
    print(width + string)
    size = round(int(size[0]))
    size = size/2.5
    for i in range(int(size)):
        print("")
def executeR(arg):
    try:
        s = subprocess.check_output(arg.split()).decode("utf-8")
        s = s.rstrip()
        s = s.split(' ')
        return s
    except:
        return False
def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))   # \b: non-deleting backspace

def install(imageType, fileLocation):
    r("Flashing recovery")
    try:
        data = executeR("sudo fastboot flash recovery " + str(fileLocation))
        return True
    except:
        r("Something's not right.")
        print("The install failed, We'll try to reboot your device into recovery. Make sure it's working fine.")
        return False

def reboot():
    print("###########################")
    print("Reboot your Device\n1.Reboot System (Boot into Android)\n2.Reboot Fastboot (Reboot into bootloader)\n3.Reboot Recovery (Reboot into recovery)")
    print("###########################")
    reply = int(input("Selection> "))
    if reply == 1:
        r("Rebooting device...")
        executeR("adb reboot")
        r("Waiting for device")
        for i in range(50):
            system = deviceLoc()
            if type(system) != bool:
                menu()
            else:
                time.sleep(5)
        startupChecks()
    elif reply == 2:
        r("Booting to fastboot")
        execute("sudo adb reboot bootloader")
        startupChecks()
    elif reply == 3:
        r("Rebooting to recovery")
        executeR("adb reboot recovery")
        r("Waiting for device")
        for i in range(10):
            system = deviceLoc()
            if type(system) != bool:
                menu()
            else:
                time.sleep(5)
        startupChecks()
    else:
        r("Unknown Selection")
        time.sleep(1)
        menu()

def menu():
    global debug
    global devices
    global system
    cmds = 7
    if debug == True:
        cmds = cmds + 1
    size = executeR("stty size")
    print(size)
    for i in range(int(size[0])):
        print("\n")
    hash = "#"
    for i in range(int(size[1])):
        hash = hash + "#"
    hash = hash[1:]
    print(hash)
    if devices[0] == "RUNNING":
        productinfo = executeR("sudo adb -s " + str(devices[1]) + " shell getprop ro.product.model")
        deviceName = ""
        loop = 0
        for i in productinfo:
            if loop == 0:
                deviceName = i
            else:
                deviceName = deviceName + " " + i
            loop = loop + 1
        if debug == True:
            string = "PLATFORM: " + platform.system().rstrip().upper() + " | DEBUG | " + devices[1]
        else:
            string = "PLATFORM: " + platform.system().rstrip().upper() + " | " + deviceName
            stdout(string.rjust(int(size[1])))
    stdout('#rootella V: {0}'.format(version))
    sys.stdout.flush()
    print()
    print("0. Quit")
    print("1. Reboot")
    print("2. Check connectivity")
    print("3. Temporarily boot TWRP")
    print("4. Flash custom recovery")
    print("5. Unlock system bootloader")
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
    if select == 2:
        print("Checking with ADB... Please wait.")
        startupChecks()
    if select == 3:
        if os.path.isfile("twrp.img") == False:
            clear()
            print("====TWRP Quick Boot====\nAs we currently don't have a TWRP downloader,\nPlease download the required TWRP\nimage for " + system[0] + " and name the file\n'twrp.img'")
            input("Press ENTER to continue... ")
            menu()
        r("Rebooting to fastboot")
        executeR("adb reboot bootloader")
        r("Waiting for device")
        for i in range(10):
            system = deviceLoc()
            if type(system) != bool:
                if system[0] == "FASTBOOT":
                    print("Device online... Booting into TWRP.")
                    info = executeR("sudo fastboot boot twrp.img")
                    time.sleep(1)
                    r("Waiting for device")
                    for i in range(10):
                        system = deviceLoc()
                        if type(system) != bool:
                            if system[0] == "RUNNING":
                                r("TWRP booted!")
                                time.sleep(2)
                                menu()
                        else:
                            time.sleep(5)
            else:
                time.sleep(5)
    if select == 4:
        r("Custom Recovery")
        print("This tool will flash a custom recovery to your device, the bootloader must be unlocked, if it's not, this tool will fail.")
        answer = input("Continue? [y/N]> ").lower()
        if answer == "y":
            r("Rebooting to fastboot")
            executeR("adb reboot bootloader")
            r("Waiting for device")
            for i in range(10):
                system = deviceLoc()
                if type(system) != bool:
                    fileLoc = input("File location (.img)> ")
                    if os.path.isfile(fileLoc):
                        if install("recovery", fileLoc):
                            r("Recovery flashed!")
                            time.sleep(2)
                            r("Rebooting device...")
                            executeR("sudo fastboot reboot")
                            r("Waiting for device")
                            time.sleep(1)
                            for i in range(20):
                                system = deviceLoc()
                                if type(system) != bool:
                                    menu()
                                else:
                                    time.sleep(5)
                            startupChecks()
                        else:
                            menu()
                    else:
                        print("File not found.")
                else:
                    time.sleep(5)
        else:
            menu()
    if select == 5:
        r("Bootloader unlock")
        print("This tool will unlock your device's bootloader")
        print("THIS WILL ERASE YOUR DATA AND PROBABLY VOID YOUR DEVICE WARRENTLY.")
        answer = input("Are you sure you want to do this? [y/N]> ").lower()
        if answer == "y":
            print("Okay, let's go, I've got the torch...")
            time.sleep(0.26)
            r("Rebooting to fastboot")
            executeR("adb reboot bootloader")
            r("Waiting for device")
            for i in range(10):
                system = deviceLoc()
                if type(system) != bool:
                    if system[0] == "FASTBOOT":
                        r("Take a look at your phone.")
                        print("Please use the volume buttons and power button to select 'Yes' on the bootloader message. ")
                        try:
                            info = executeR("sudo fastboot oem unlock")
                            r("Bootloader unlocked!")
                            print("We've unlocked your bootloader, hit the power button on your phone to boot into recovery to flash your ROM :D")
                            input("Press enter to continue")
                            init("warm")
                        except:
                            print("Something has gone wrong. Reboot your device and make sure it's working correctly.")
                            input("Press ENTER to continue... ")
                            init("warm")
                    else:
                        r("Something not right.")
                        print("Something has gone wrong. We'll reboot your phone, make sure it's working.")
                        executeR("sudo fastboot reboot")
                else:
                    time.sleep(5)
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

    if len(running) == 1:
        fastboot = subprocess.check_output("sudo fastboot devices".split()).decode("utf-8")
        fastboot = fastboot.split("\t")
        if len(fastboot) < 2:
            return False
        fastboot[1] = fastboot[1].rstrip()
        arr = ["FASTBOOT"]
        for i in fastboot:
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
    devices = deviceLoc()
    global debug
    if debug == True:
        print("Device list (Contains Virtual Device): ")
        print(devices)
        time.sleep(1)
    if debug == False:
        devices = deviceLoc()
    if devices == False and debug == False:
        r("Device not found")
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
        devices = []
        startupChecks()
    if len(devices) > 3:
        print("We've detected more than one device\nPlease only connect the device you want to use the toolkit with. Unplug the others.")
        input("Press ENTER to continue...\n################################")
        if debug == True:
            print("You're running in debug mode with multiple devices, we'll automatically remove the device named " + devices[1] + " and rescan.")
            devices.remove(devices[0])
            devices.remove(devices[1])
            devices.remove(devices[2])
        startupChecks()
    if devices[2] == "unauthorized":
        print("#################################")
        print("Looks like your device is unauthorized\nPlease authorize this computer on your phone now.\nWe suggest ticking 'Always allow from this computer' to stop errors/crashes.")
        input("Press ENTER to continue...\n################################")
        if debug == True:
            print("Debug mode set, changing unauthorized to authorized automatically.")
            devices[2] = "AUTHORIZED"
        startupChecks()
    if devices[0] == "FASTBOOT":
        r("Device verification error.")
        time.sleep(1)
        print("As the device is in fastboot, we couldn't verify that it's comptable. We suggest you boot into recovery or Android.")
        answer = input("Press ENTER to continue without verification or type reboot to boot into android> ")
        if answer == "reboot":
            r("Rebooting device")
            execute("sudo fastboot reboot")
            time.sleep(10)
            init("warm")
        else:
            menu()
    else:
        global system
        global supportedDevices
        system = executeR("sudo adb -s "+str(devices[1])+" shell getprop ro.product.device")
        if system[0] in supportedDevices:
            #r(system[0] + " connected!")
            time.sleep(2)
            menu()
        else:
            if system[0] == "/sbin/sh:":
                r("Please reboot your device")
                print("Please reboot your device into Android, we can't verify the device as it's either in temp boot or using an old recovery.")
                input("Press ENTER to continue... ")
                init("warm")
            else:
                r(system[0] + " not supported")
                print("Your connected device, " + system[0] + " is currently not supported. Sorry!")
                input("Press ENTER to continue or CTRL + C to exit... ")
                init("warm")
init("cold")
