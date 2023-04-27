import pyautogui as pg
import pyperclip
import time

commands = []
command = ''

def update_command_list(path = 'commands.txt'):
    global commands, command
    print('[log]: updating commands list: \033[33mstarted')
    try:
        # opening file with commands in read mode
        with open(path, 'r') as comms:
            # reading inforamtion from file
            red = comms.read()
            # creating a for loop to separate all commands in deffernet cell in "commands"
            for i in red.split(' '):
                if '--------------' not in i:
                    command += f'{i} '
                if '--------------' in i:
                    command += i.replace('\n', ' ').split(' ')[0]
                    commands.append(command)
                    command = ''
                    command += i.replace('\n', ' ').split(' ')[2] + ' '
            print('\033[37m[log]: updating commands list:\033[32m done')
    except FileNotFoundError:
        print(f'\033[37m[log]:\033[31m error \033[37m\ninvalid file path: {path}')


def send_to_jasper():
    print('\033[37[log]: menter "send_to_jasper"')
    for send_command in commands:
        print(send_command, '\n') 
        pg.moveTo(410, 889)                             # moving cursor to the textbar
        pg.click()                                      # clicking on it to start writing text
        pyperclip.copy(send_command.replace('\n', ' ')) # copying text that i need to enter
        pg.hotkey('ctrl', 'v')                          # entering text from command.txt
        pg.press('enter')                               # sending it to jasper
        print('[log]: waiting for respond 20s')
        time.sleep(20)                                  # waiting 20s fo jasper's respond

        pg.moveTo(1466, 615)                            # moving cursor to the copy button
        pg.click()                                      # copying jasper's respond to clipboard

        paste = pyperclip.paste()                       # saving jasper's respond to the variable
        print(paste)

        print('[log]: saving respond to "respond.txt"') 
        with open('respond.txt', 'a') as respond_file:  # opening "respond.txt" to write respond in it
            text = f'{paste.strip()}\n-----------\n'    # formating respond to make it easyer to read
            respond_file.write(text)                    # writing respond to "respond.txt"

    for i in range(5):
        print('\033[32m!!!DONE!!!')

def main():
    time.sleep(5)
    print('\033[37m[log]: first step  : enter')
    update_command_list(path = 'commands.txt')
    print('\033[37m[log]: first step  : \033[32mdone \n[log]: enter second: \033[33mstart')
    send_to_jasper()
    print('\033[37m[log]: second step : \033[32mdone')
    

if __name__ == '__main__':
    main()
#| coded by c0dem