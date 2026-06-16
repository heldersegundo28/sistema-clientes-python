from datetime import datetime
def log(msg):
    with open('sistema.log','a',encoding='utf-8') as f:
        f.write(f'{datetime.now()} - {msg}\n')