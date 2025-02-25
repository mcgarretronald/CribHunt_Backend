import http.client

conn = http.client.HTTPSConnection("dev-om5mrak03nvhp3qu.us.auth0.com")

payload = "{\"client_id\":\"ocEwGgD4QGBuv9ibOMdab7WqdhUv2wIZ\",\"client_secret\":\"7j9MOH9FUjzzHGtk2o1lhgCj67BEUlZvsB2NZe5ZLif0_LQeC4P1nOTBtPuofKjI\",\"audience\":\"https://127.0.0.1:8000/auth/auth0/\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))