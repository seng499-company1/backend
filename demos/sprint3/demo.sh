# succesfully pings the login endpoint for a professor
curl -H "Content-Type: application/json" \
    -d '{"username":"mdadams", "password":"password"}' \
    http://localhost:5000/login/
