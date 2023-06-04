from datetime import datetime


def audit_log_transaction(tourisId: str, message=''):
    with open('audit_log.txt', mode='a') as logfile:
        content = f'tourist {tourisId} executed {message} at {datetime.now()}'
        logfile.write(content)
