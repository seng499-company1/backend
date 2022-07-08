echo 'admin login'
curl -H "Content-Type: application/json" \
    -d '{"username":"admin", "password":"password"}' \
    http://localhost:5000/login/

echo 'professor login'
curl -H "Content-Type: application/json" \
    -d '{"username":"mdadams", "password":"password"}' \
    http://localhost:5000/login/

echo 'wrong password'
curl -H "Content-Type: application/json" \
    -d '{"username":"mdadams", "password":"pasord"}' \
    http://localhost:5000/login/

echo 'invalid user'
curl -H "Content-Type: application/json" \
    -d '{"username":"mdas", "password":"pasord"}' \
    http://localhost:5000/login/