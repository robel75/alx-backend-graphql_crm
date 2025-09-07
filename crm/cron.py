import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """Logs a heartbeat message and optionally checks GraphQL endpoint."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(f"{timestamp} CRM is alive\n")

    # Optional GraphQL check
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=True, retries=3)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        result = client.execute(query)
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL endpoint responded: {result}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL check failed: {e}\n")

def update_low_stock():
    """Updates low-stock products via GraphQL and logs updates."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/low_stock_updates_log.txt"

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
        """)
        result = client.execute(mutation)
        with open(log_file, "a") as f:
            for product in result["updateLowStockProducts"]["updatedProducts"]:
                f.write(f"{timestamp} - {product['name']} stock updated to {product['stock']}\n")
            f.write(f"{timestamp} - {result['updateLowStockProducts']['message']}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Low stock update failed: {e}\n")
