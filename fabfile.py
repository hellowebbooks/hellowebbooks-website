import os
from fabric import task, Connection

@task
def deploy(c):
    c = Connection(host='165.227.33.196', user=os.environ['POSTGRES_US'])
    with c.cd('hellowebbooks/hellowebbooks'):
        c.run('git pull origin master')
        c.sudo('systemctl restart gunicorn')
