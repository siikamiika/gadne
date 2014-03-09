from subprocess import getoutput, Popen

triggers = ['!update']

def run(msg):
    status = getoutput('git pull')
    if status == 'Already up-to-date.':
         return 'ei uusia committeja KUULIKKO :ghammer:'
    else:
        Popen('./update &', shell=True)
