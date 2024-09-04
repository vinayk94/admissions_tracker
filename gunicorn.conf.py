import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5