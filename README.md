# brutelee
BruteLee is a simple SSH brute forcer using generated passwords and passwords read from a file.

# Usage
```python BruteLee.py -u username -s serverIP [-pwl password_length ] [password character set options | -f passwordfile]```

# Examples                          
```python BruteLee.py -u user02 -s 192.168.81.129 -num -fpw 01 -d ```

Connect to user02 at address 192.168.81.129, use only numbers in the password, use a forced password of 01 for testing, print debug information

```python BruteLee.py -u user03 -s 192.168.81.129 -f 500_worst_passwords.txt```

Connect to user03 at address 192.168.81.129, using the file 500_worst_passwords.txt. Add -fpw dragon -d to print debug info for this example.

short | long | purpose
----- | ---- | -------
-u | --username | Username whose password you are trying to find. Required.
-s | --server | IP address of SSH server. Required.
-pwl | --pwlength | Password length, default = 3
-lc | --lowercase | Use lower case characters in the password (default if no other options are specified)
-uc | --uppercase | Use upper case characters in the password
-sym | --symbols  | Use symbol characters in the password
-num | --numbers  | Use numbers in the password
-p |  --port     | Port to connect on, default = 22
-fpw | --forcepw  | Force this password to be used (testing purposes). Use with -d
-f  | --pwfile   | Text file containing passwords, one per line
-d |  --debug    | Print arguments & test connection with server, use with -fpw
