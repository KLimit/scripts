#!/usr/bin/env python3
#
# Chalk: A line mode text editor
# (c) 2020 Brian Evans, All Rights Reserved
# 
# Chalk is available under the terms of the Floodgap Free
# Software License. A copy of the license should be included
# with this source code. An online copy can be found here:
# https://www.floodgap.com/software/ffsl/license.txt
#_


### Notes . . . .
# \001 and \002 fix a readline issue
# See: https://stackoverflow.com/questions/9468435/how-to-fix-column-calculation-in-python-readline-if-using-color-prompt
##################

###########################################################
#  Imports
###########################################################

import sys
import os
import re
import readline
import tempfile

###########################################################
#  Globals
###########################################################

content = []
paste_buffer = []
file_changed = False
filepath = ''
filename = 'scratch buffer'
view_loc = {'last': 0, 'count': 0}
__VERSION__ = '2.1.0'


###########################################################
#  Classes
###########################################################

class c:
    black = ''
    red = '\033[0;31m'
    b_red = '\033[1;31m'
    yellow = '\033[1;33m'
    green = '\033[0;32m'
    b_green = '\033[1;32m'
    cyan = '\033[0;36m'
    b_cyan = '\033[1;36m'
    purple = '\033[1;35m'
    blue = '\033[0;34m'
    b_blue = '\033[1;34m'
    white = '\033[1;37m'
    end = '\033[0m'
    invert = '\033[7m'
    bold = '\033[1m'


###########################################################
#  Functions
###########################################################

###                       #################################
### Utilities and helpers #################################

def pre_input_hook(txt):
    readline.insert_text(txt)
    readline.redisplay()

def input_editable(prompt, prefill=''):
    readline.set_pre_input_hook(lambda: pre_input_hook(prefill))
    try:
        edin = input(prompt)
    finally:
        readline.set_pre_input_hook(None)
    return edin


def validate_path(path):
    path_body_list = path.split('/')
    path_body_list.pop()
    path_body = '/'.join(path_body_list)
    is_path = os.path.isdir(path_body)
    if not is_path:
        return False
    return True

def check_file_writable(fnm):
    if os.path.exists(fnm):
        if os.path.isfile(fnm): # is it a file or a dir?
            return os.access(fnm, os.W_OK)
        else:
            return False
    pdir = os.path.dirname(fnm)
    if not pdir: pdir = '.'
    return os.access(pdir, os.W_OK)


def print_help():
    helptext = [
        "",
        "{}Commands are entered as the only entry for their row:{}".format(c.yellow, c.end),
        "",
        " {}.?{} - Print this help message".format(c.b_green, c.end),
        " {}.g{} - Print the ruler/guide".format(c.b_green, c.end),
        " {}.f{} - Print file info".format(c.b_green, c.end),
        "",
        " {}.d{} - Display the whole file".format(c.b_green, c.end),
        " {}.v{} - View range of lines (will request location/count)".format(c.b_green, c.end),
        " {}.m{} - View MORE (use after using .v to see more)".format(c.b_green, c.end),
        "",
        " {}.#{} - Edit a line (eg .27)".format(c.b_green, c.end),
        " {}.i{} - Insert empty line(s) (will request location/count)".format(c.b_green, c.end),
        " {}.x{} - Cut/copy line(s) (will request line range)".format(c.b_green, c.end),
        "",
        " {}.c{} - Copy to the paste buffer (will request line range)".format(c.b_green, c.end),
        " {}.p{} - Paste from the paste buffer (will request destination)".format(c.b_green, c.end),
        " {}.b{} - Buffer view (print the paste buffer)".format(c.b_green, c.end),
        "",
        " {}.s{} - Save changes to the document".format(c.b_green, c.end),
        " {}.a{} - Save as a new file (will request file location)".format(c.b_green, c.end),
        "  {}. {} - Finish writing/exit (will prompt for save)".format(c.b_green, c.end),
        "",
        " {}.r{} - Print the document to the default printer".format(c.b_green, c.end),
        "",
        "{}- - -{}".format(c.yellow, c.end),
        ""
    ]
    for x in helptext:
        print('{:8} {}'.format(' ',x))

# Print ruler will print the text guide/rule
# at the width of the current terminal - ui indent
def print_ruler():
    try:
        width = os.get_terminal_size()[0] - 9
    except:
        width = 60 - 9
    counter = "         "
    ticker = "         "
    current = 5
    while current < width - 5:
        counter += "{:5}".format(current)
        ticker += "....|"
        current += 5
    print(counter)
    print(ticker)


def print_file_info():
    user_can_write = os.access(filepath, os.W_OK)
    print('{}   Writing:{} {}{}'.format(c.yellow, c.white, filename, c.end))
    print('{}   Length :{} {} rows / {} chars{}'.format(c.yellow, c.white, len(content), get_character_count(), c.end))
    if not filepath:
        print('{}   You are in the scratch buffer. Use \033[3m.a\033[23m to save your work as a file{}'.format(c.bold, c.end))
    elif not user_can_write:
        print('{}   You do not have permission to write to {} >>{}'.format(c.bold, filename, c.end))

    if file_changed:
        print('{}   File has unsaved changes!{}\n'.format(c.bold, c.end))



# Print banner will print the program name,
def print_banner():
    print('\n   Chalk {} by sloum\n'.format(__VERSION__))
    print_file_info()
    print("   For a command list, enter {}.?\n{}".format(c.green, c.end))


def get_character_count():
    chars = 0
    for row in content:
        chars += len(row)
    return chars


# Build contents from file sets the absolute
# file path, the file name, and loads in any
# content contained in a file
def build_contents_from_file(path):
    # No path was given, just create an empty
    # content buffer and it can be saved later
    if not path:
        return

    global content
    global filepath
    global filename

    path = os.path.abspath(path)
    filepath = os.path.expanduser(path)
    filename = filepath.split('/')[-1]
    try:
        valid_path = validate_path(filepath)
        if not valid_path:
            print('Invalid file path')
            sys.exit(2)

        with open(filepath, 'r') as f:
            content = f.read().split('\n')
            if content[-1] == '':
                content.pop()
    except FileNotFoundError:
        content = []
    except IsADirectoryError:
        print('The given filepath is a directory')
        sys.exit(2)
    except PermissionError:
        print('You do not have permission to read {}'.format(path))
        sys.exit(2)


# Yes No queries the user with a yes no question and returns
# True on yes and False on no
def yes_no(question):
    confirmation = ''
    while confirmation not in ['y','yes','n','no']:
        confirmation = input(question)
        confirmation = confirmation.lower()
    return True if confirmation in ['y', 'yes'] else False


####                            ###########################
##### Input and Command Routers ###########################

# Chalk is the entry point into the editor, contains the
# input loop and does some routing
def chalk(path):
    global file_changed

    build_contents_from_file(path)

    print_banner()
    print_ruler()

    while True:
        ln = input('{:6} \001{}\002>\001{}\002 '.format(len(content), c.yellow, c.end))
        if ln == '.':
            # End the editing session (quit)
            # Will query for save if the file has been changed
            quit()
        elif re.match(r'^\.\d+$',ln):
            # Edit a previous line
            edit_line(ln)
        elif len(ln) == 2 and ln[0] == '.':
            # Route a command
            command_router(ln)
        else:
            # Add new content
            content.append(ln)
            file_changed = True

# Command router takes a command line and routes it to its
# command function
def command_router(ln):
    if ln == '.?':
        print_help()
    elif ln == '.a':
        save_as()
    elif ln == '.b':
        view_paste_buffer()
    elif ln == '.c':
        copy_rows()
    elif ln == '.d':
        display_file()
    elif ln == '.f':
        print_file_info()
    elif ln == '.g':
        print_ruler()
    elif ln == '.i':
        insert_lines()
    elif ln == '.m':
        view_continue()
    elif ln == '.p':
        paste_from_buffer()
    elif ln == '.v':
        view_rows()
    elif ln == '.x':
        cut_lines()
    elif ln == '.s':
        save_changes()
    elif ln == '.r':
        print_document()
    else:
        print('{:9}{}Unknown command: {}{}'.format(' ', c.red, ln, c.end))


#####                   ###################################
##### Command Functions ###################################

# Edit line edits an existing line or prints an error
# if the line was unable to be edited
def edit_line(ln):
    global content
    global file_changed
    try:
        row = int(ln[1:])
        text = content[row]
        newln = input_editable('{:6} \001{}\002>\001{}\002 '.format(row, c.b_blue, c.end), content[row])
        if newln != text:
            content[row] = newln
            file_changed = True
    except:
        print('{}{:8} Invalid entry!{}'.format(c.b_red, ' ', c.end))


# Save changes saves changes to a file
def save_changes():
    global file_changed

    if not file_changed:
        return True

    text = '\n'.join(content)
    text += '\n'
    try:
        with open(filepath, 'w') as f:
            f.write(text)
        print('         Saved \033[1m{}\033[0m'.format(filename))
        file_changed = False
        return True
    except PermissionError:
        print('{}         You do not have permission to write to this file.{}'.format(c.red, c.end))
        return False
    except:
        print('{}         Error while writing to file: {}{}'.format(c.red, e, c.end))
        return False


# Save as will switch the save location to
# a new file path and save the content buffer
# to that new path. It will validate the path
# beforehand
def save_as():
    global filepath
    global filename
    global file_changed

    print('{:9}{}Enter the new save path (can be relative):{}'.format(' ', c.cyan, c.end))
    path = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.green, c.end))

    continue_save_as = yes_no('{:9}{}Are you sure you want to save as {}? (y/n){} '.format(' ', c.cyan, path, c.end))
    if not continue_save_as:
        print('{:9}Save canceled.'.format(' '))
        return False

    path = os.path.abspath(path)
    fp = os.path.expanduser(path)
    fn = path.split('/')[-1]
    valid = check_file_writable(fp)
    if not valid:
        print('{:9}{}The path is invalid, save cancelled{}'.format(' ', c.red, c.end))
        return False

    filepath = fp
    filename = fn
    file_changed = True
    return save_changes()


# Quit will quit the program, but first will ask to save if there
# are any unsaved changes
def quit():
    if not file_changed:
        sys.exit(0)
    save = yes_no('         {}Save changes to {}?{} (Y/n) '.format(c.b_green, filename, c.end))
    if save:
        saved = save_changes() if filepath else save_as()
        if saved:
            print('         File "{}" has been saved.'.format(filename))
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(0)


# Display file prints the whole file, line by line, to
# stdout
def display_file():
    print('\n        - - -')
    for i, x in enumerate(content):
        print('{:6} - {}{}{}'.format(i, c.green, x, c.end))
    print('        - - -\n')


def cut_lines():
    global content
    global file_changed
    global paste_buffer

    print('{:9}{}Enter the line number you want to start deleting at:{}'.format(' ', c.cyan, c.end))
    beg = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.b_red, c.end))

    print('{:9}{}Enter the last line number you want to delete (or $ for end of file){}:'.format(' ', c.cyan, c.end))
    end = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.b_red, c.end))

    continue_delete = yes_no('{:9}{}Are you sure you want to delete lines {} - {}? (y/n){} '.format(' ', c.cyan, beg, end, c.end))
    if not continue_delete:
        print('{:9}Deletion canceled.'.format(' '))

    if end == '$':
        end = len(content) - 1
    try:
        beg = int(beg)
        end = int(end) + 1
        if beg < 0 or beg > end:
            print('{}{:9}Invalid entry{}'.format(c.red, ' ', c.end))
            return

        paste_buffer = content[beg:end]

        if end == len(content):
            content = content[:beg]
        else:
            content = content[:beg] + content[end:]
        file_changed = True
    except:
        print('{}{:9}Invalid entry{}\n'.format(c.red, ' ', c.end))


def insert_lines():
    global content
    global file_changed

    print('{:9}{}Enter the line number you want to insert lines before:{}'.format(' ', c.cyan, c.end))
    beg = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.b_green, c.end))

    print('{:9}{}Enter the number of rows you want to insert{}:'.format(' ', c.cyan, c.end))
    count = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.b_green, c.end))

    continue_insert = yes_no('{:9}{}Are you sure you want to insert {} rows before line {}? (y/n){} '.format(' ', c.cyan, count, beg, c.end))
    if not continue_insert:
        print('{:9}Insertion canceled.'.format(' '))

    try:
        beg = int(beg)
        count = int(count)

        if beg < 0 or beg > len(content) or count < 1:
            print('{}{:8} Invalid entry{}'.format(c.red, ' ', c.end))
            return

        while count > 0:
            content.insert(beg,'')
            count -= 1
        file_changed = True
    except:
        print('{}{:8} Invalid entry{}'.format(c.red, ' ', c.end))


def view_rows():
    global view_loc
    print('{:9}{}Enter the line number you want to start viewing from:{}'.format(' ', c.cyan, c.end))
    start = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.yellow, c.end))

    print('{:9}{}Enter the number of rows you want to view{}:'.format(' ', c.cyan, c.end))
    count = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.yellow, c.end))

    try:
        beg = int(start)
        counter = int(count)

        if beg > len(content) - 1:
            print('{}{:9}Cannot start viewing past the end of the file{}')


        if beg < 0 or beg > len(content) - 1:
            print('{}{:9}Invalid view location{}'.format(c.red, ' ', c.end))
            return
        else:
            view_loc['count'] = counter
            print('')
            while counter > 0 and beg < len(content):
                print('{:6} - {}{}{}'.format(beg, c.green, content[beg], c.end))
                counter -= 1
                beg += 1
            print('')
            view_loc['last'] = beg if beg < len(content) - 1 else None

    except:
        print('{}{:8} Invalid entry{}'.format(c.red, ' ', c.end))


def view_continue():
    global view_loc
    if not view_loc['count'] or view_loc['last'] is None:
        print('{}{:9}There is not a current view opperation to continue{}'.format(c.red, ' ', c.end))
        return
    beg = view_loc['last']
    counter = view_loc['count']
    print('')
    while counter > 0 and beg < len(content):
        print('{:6} - {}{}{}'.format(beg, c.green, content[beg], c.end))
        counter -= 1
        beg += 1
    print('')
    view_loc['last'] = beg if beg < len(content) - 1 else None




def copy_rows():
    global paste_buffer

    print('{:9}{}Enter the line number you want to start copying from:{}'.format(' ', c.cyan, c.end))
    start = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.yellow, c.end))

    print('{:9}{}Enter the last line you want to copy ($ for end of file):{}'.format(' ', c.cyan, c.end))
    finish = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.yellow, c.end))
    if finish == '$':
        finish = len(content) - 1

    try:
        beg = int(start)
        end = int(finish)

        if beg > end or beg < 0 or end > len(content) - 1:
            print('{}{:9}Invalid entry x{}'.format(c.red, ' ', c.end))
            return
        else:
            paste_buffer = content[beg:end + 1]

    except:
        print('{}{:8} Invalid entry{}'.format(c.red, ' ', c.end))


def paste_from_buffer():
    global content
    global file_changed

    print('{:9}{}Enter a line number. The pasted data will be inserted {}before{} the given line:{}'.format(' ', c.cyan, '\033[4m', '\033[24m', c.end))
    beg = input('{:6} \001{}\002>\001{}\002 '.format(' ', c.b_green, c.end))

    continue_paste = yes_no('{:9}{}Are you sure you want to paste from the paste buffer before line {}? (y/n){} '.format(' ', c.cyan, beg, c.end))
    if not continue_paste:
        print('{:9}Paste canceled.'.format(' '))

    try:
        beg = int(beg)

        if beg < 0 or beg > len(content):
            print('{}{:8} Invalid entry{}'.format(c.red, ' ', c.end))
            return

        for row in paste_buffer[::-1]:
            content.insert(beg,row)
        file_changed = True
    except:
        print('{}{:8} Invalid entry{}'.format(c.red, ' ', c.end))


def view_paste_buffer():
    print('')
    if len(paste_buffer):
        for num, ln in enumerate(paste_buffer):
            print('{:6} - {}{}{}'.format('pb', c.blue, ln, c.end))
    else:
        print('{:6} - {}{}{}'.format('pb', c.blue, 'The paste buffer is currently empty', c.end))
    print('')


def print_document():
    with tempfile.NamedTemporaryFile(mode = 'w+') as f:
        if sys.platform == 'win32':
            f.write('\r\n'.join(content))
            os.startfile(f.name, 'print')
        else:
            f.write('\n'.join(content))
            os.system('lpr {}'.format(f.name))


def main():
    global filepath
    args = sys.argv
    if len(args) > 2:
        print('Incorrect number of arguments:')
        print('chalk [\033[3mfile path\033[0m]')
        sys.exit(1)
    elif len(args) == 2:
        if len(args[1]) and args[1][0] == "-":
            print('Unknown flag {}'.format(args[1]))
            print('chalk [\033[3mfile path\033[0m]')
            sys.exit(1)
        filepath = args[1]

    # Set readline settings
    readline.parse_and_bind('set editing-mode emacs')
    readline.parse_and_bind('set show-mode-in-prompt off')

    # Run the editor
    chalk(filepath)



###########################################################
# Init
###########################################################

if __name__ == '__main__':
    main()
