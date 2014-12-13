bind = "0.0.0.0:5001"
workers = 8
worker_class = "egg:gunicorn#gevent"
daemon = True
#pidfile = '/tmp/file-server.pid'
#errorlog = accesslog = '/home/log/file-server/gunicorn.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(T)s %(D)s "%(f)s" "%(a)s"'
