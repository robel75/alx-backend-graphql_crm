#!/usr/bin/env python3

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(
    url='http://localhost:8000/graphql',
    verify=True,
    retries=3,
)
client = Client(transport=transport, fetch_schema_from_transport=True)
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
query = gql("""
query getRecentOrders($since: DateTime!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
""")

params = {"since": seven_days_ago}

try:
    result = client.execute(query, variable_values=params)
    orders = result.get("orders", [])
except Exception as e:
    print(f"GraphQL query failed: {e}")
    orders = []

log_file = "/tmp/order_reminders_log.txt"
with open(log_file, "a") as f:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for order in orders:
        f.write(f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n")

print("Order reminders processed!")
