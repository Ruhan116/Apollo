import http.client, json, sys

def req(host, port, method, path, data=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=10)
    body = json.dumps(data).encode('utf-8') if data is not None else None
    headers = headers or {}
    if body and 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'
    conn.request(method, path, body=body, headers=headers)
    r = conn.getresponse()
    b = r.read().decode('utf-8')
    return r.status, b, dict(r.getheaders())

# Check health of gateway, auth, goals
services = [("localhost",8000,"/health/live"),("localhost",8001,"/health/live"),("localhost",8002,"/health/live")]
for h,p,path in services:
    try:
        s,b,_ = req(h,p,'GET',path)
        print(f'HEALTH {p}{path} ->', s, b)
    except Exception as e:
        print('HEALTH ERROR', p, e)

# Login via gateway
login_payload = {"email":"ruhan@gmail.com","password":"Pass@123"}
try:
    s,b,_ = req('localhost',8000,'POST','/api/auth/login', login_payload)
    print('LOGIN ->', s, b)
    if s != 200:
        sys.exit(0)
    token = json.loads(b).get('access_token')
    if not token:
        print('NO TOKEN')
        sys.exit(0)
except Exception as e:
    print('LOGIN ERROR', e)
    sys.exit(0)

# Create goal via gateway
try:
    create_payload = {"prompt":"Test goal via gateway (retry)"}
    s2,b2,headers2 = req('localhost',8000,'POST','/api/goals/create', create_payload, {'Authorization': f'Bearer {token}'})
    print('CREATE ->', s2)
    print('BODY:', b2)
    print('HEADERS:', headers2)
except Exception as e:
    print('CREATE ERROR', e)
