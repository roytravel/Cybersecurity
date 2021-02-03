import paramiko as paramiko
from paramiko import AutoAddPolicy

server=""
username="Administrator"
password = ""
cmd_to_execute = "cd C:\\Users\Administrator\\Desktop\\test\\ & python test.py & dir"

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(AutoAddPolicy())

ssh.connect(server, username=username, password=password, sock=None, port=22)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)

err = ''.join(ssh_stderr.readlines())
out = ''.join(ssh_stdout.readlines())
final_output = str(out)+str(err)
print(final_output)