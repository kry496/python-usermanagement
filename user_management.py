#!/usr/bin/python

import argparse, re, sys, subprocess, getpass, os.path, shutil

parser = argparse.ArgumentParser(description='ADD/DELETE Users')
parser.add_argument('-a', '--add',metavar='ADD-USER',help='ADD USER TO THE SERVER',dest='adduser')
parser.add_argument('-d', '--delete',metavar='DELETE-USER',help='DELETE USER FROM THE THE SERVER',dest='deluser')
parser.add_argument('-g', '--group',metavar='group',help='Manually specific USER GROUP',dest='group')
parser.add_argument('-x', '--gid',metavar='gid',help='Manually specific GROUP ID',dest='gid')
parser.add_argument('-y', '--uid',metavar='uid',help='Manually specific USER ID',dest='uid')
parser.add_argument('-s', '--shell',metavar='shell',help='USE NO to avoid login shell creation',dest='shell')
parser.add_argument('-f', '--directory',metavar='directory',help='USE NO to avoid USER directory creation',dest='folder')
parser.add_argument('-p', '--passwd',metavar='passwd',help='USE YES to overide default password created',dest='passwd')

args = parser.parse_args()
user_name = args.adduser
user_id = args.uid


def input_validation():
	if not re.match('[_a-z][-0-9_a-z]*', args.adduser):
		#sys.stderr.write("USER NAME FORMAT NOT VALID")
		raise SystemExit("User Name Format is not Valid")
	if args.group:
		if not re.match('[_a-z][-0-9_a-z]*', args.group):
		#sys.stderr.write("GROUP NAME FORMAT NOT VALID")
			raise SystemExit("Group Name Format is not Valid")
	if not re.match('[0-9]+', args.uid):
		#sys.stderr.write("GROUPD ID FORMAT NOT VALID]")
		raise SystemExit("User ID Format is not Valid")
	if not re.match('[0-9]+', args.gid):
		#sys.stderr.write("GROUPD ID FORMAT NOT VALID]")
		raise SystemExit("Group ID Format is not Valid")


def password_encoder(psswd):
	print(psswd)
	x = subprocess.check_output(['openssl', 'passwd', '-1','-salt','xyz', psswd])
	return(x.decode('utf-8'))


def set_password():
	if args.passwd == 'YES':
		psswd = getpass.getpass('Set Password:')
		update_etc_shadow(psswd)
	else:
		update_etc_shadow("passw0rd")
		# user created with default password -> "passw0rd"

def check_group():
	with open('/etc/group', 'rt') as fd:
		for lines in fd:
			line = lines.split(':')
			if line[0] == args.group:
				sys.stdout.write("GROUP ALREADY EXISTS")
			if args.gid in line[2].split(','):
					raise SystemExit("GID already in USE")

def check_user():
	with open('/etc/passwd', 'rt') as fd:
		for lines in fd:
			line = lines.split(':')
			if line[0] == args.adduser:
				raise SystemExit("User Already present")
				#sys.stderr.write("User Already present")
			if line[2] == args.uid:
				raise SystemExit("UID Already present")
				#sys.stderr.write("UID Already present")

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def mk_home_dir(user_name):
	home_dir = '/home/' + user_name
	subprocess.call(['mkdir', home_dir])
	if os.path.exists('/etc/skel/'):
		copytree('/etc/skel',home_dir)
	return home_dir

def update_etc_passwd(home_dir,shell_value='/bin/bash'):
	with open('/etc/passwd', 'at') as fd:
		line_added = args.adduser + ":x:" + args.uid + ":" + args.gid + ":" + "" + ":" + home_dir + ":" + shell_value + "\n"
		fd.write(line_added)


def update_etc_group():
	with open('/etc/group', 'at') as fd:
		if args.group: 
			group_name = args.group
		else:
			group_name = args.adduser
		if args.gid:
			group_id = args.gid
		else:
			raise SystemExit("default GID is required")
		line_added = group_name + ":x:" + group_id + ":" + args.adduser + "\n"
		fd.write(line_added)


def update_etc_shadow(psswd):
	with open('/etc/shadow', 'at') as fd:
		line_added = user_name + ":" + password_encoder(psswd).strip() + ":17377:0:90:30:::" + "\n"
		#Account Expiry 90 days, warning for change password 30 days.
		fd.write(line_added)


def delete_user():
	home_dir = '/home/' + args.deluser
	if os.path.exists(home_dir):
		subprocess.call(['rm','-r',home_dir])
	with open('/etc/shadow', 'rt') as fd1:
		with open('/root/shadow_tmp', 'wt') as fd2:
			for lines in fd1:
				line = lines.split(':')
				if line[0] == args.deluser:
					pass
				else:
					fd2.write(lines)
	with open('/etc/passwd', 'rt') as fd1:
		with open('/root/passwd_tmp', 'wt') as fd2:
			for lines in fd1:
				line = lines.split(':')
				if line[0] == args.deluser:
					pass
				else:
					fd2.write(lines)
	with open('/etc/group', 'rt') as fd1:
		with open('/root/group_tmp', 'wt') as fd2:
			for lines in fd1:
				line = lines.split(':')
				if line[0] == args.deluser:
					pass
				else:
					fd2.write(lines)
	shutil.move('/root/shadow_tmp','/etc/shadow')
	shutil.move('/root/passwd_tmp','/etc/passwd')
	shutil.move('/root/group_tmp','/etc/group')


def main():
	if args.deluser == None:	
		input_validation()
		check_user()
		check_group()
		set_password()
		if args.shell == 'NO':
			if args.folder == 'NO':
				home_dir = '/'
				update_etc_passwd(home_dir,shell_value='/usr/sbin/nologin')
			else:
				home_dir = mk_home_dir(user_name)
				update_etc_passwd(home_dir,shell_value='/usr/sbin/nologin')
		else:
			if args.folder == 'NO':
				home_dir = '/'
				update_etc_passwd(home_dir,shell_value='/bin/bash')
			else:
				home_dir = mk_home_dir(user_name)
				update_etc_passwd(home_dir,shell_value='/bin/bash')
		update_etc_group()
	else:
		delete_user()

if  __name__ =='__main__':main()