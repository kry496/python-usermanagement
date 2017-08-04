# python-usermanagement
    Python Script to replace useradd and userdel command. 
  
 # HELP
      For Help type -> python3 user_management.py -h 
            usage: user_management.py [-h] [-a ADD-USER] [-d DELETE-USER] [-g group]
                          [-x gid] [-y uid] [-s shell] [-f directory]
                          [-p passwd]

            ADD/DELETE Users

            optional arguments:
            -h, --help                                  show this help message and exit
            -a ADD-USER, --add ADD-USER                 ADD USER TO THE SERVER
            -d DELETE-USER, --delete DELETE-USER        DELETE USER FROM THE THE SERVER
            -g group, --group group                     Manually specific USER GROUP
            -x gid, --gid gid                           Manually specific GROUP ID
            -y uid, --uid uid                           Manually specific USER ID
            -s shell, --shell shell                     USE NO to avoid login shell creation
            -f directory, --directory directory         USE NO to avoid USER directory creation
            -p passwd, --passwd passwd                  USE YES to overide default password created

    
 # SAMPLE - ADD_USER
 
      run -> python3 user_management.py -a test.user1 --gid 1003 --uid 1003 -p YES
      
      - To add user 'test.user1' use the above command
      - UID and GID are required and need to be unique;
      - if GID is not mentioned it defaults to UID value for creating group
      - GROUP NAME defaults user name; can be overridden using --group flag
      - -p flag can be used set unique password for user; script encodes the password and writes it to the shadow file
      - if -p flag is not set; the default password for the user created is 'passw0rd'
      - The default shell is bash; if shel  is not requrired use flag and value as -->>>  --shell NO
      - THe default home directory created is /home/<user_name> ; if default home directory is not required use flag --> --directory NO
      - Note: Script doesn't support user addition to existing GROUPS.
 
 # SAMPLE - DELETE_USER
       run -> python3 user_management.py -d "test.user1"
      
      - run the above command to delete user --> test.user1
       - Script will clean up home directory only if its created.

    
      
