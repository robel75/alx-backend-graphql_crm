import datetime
import requests

def log_crm_heartbeat():
    """Logs a heartbeat message to /tmp/crm_heartbeat_log.txt"""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"
    
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)
    
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            f.write(f"{timestamp} GraphQL endpoint responded\n")
        else:
            f.write(f"{timestamp} GraphQL endpoint returned status {response.status_code}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL endpoint check failed: {e}\n")
