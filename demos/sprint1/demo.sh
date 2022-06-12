curl -H "Content-Type: application/json" \
    -d '{"first_name":"Mr", "last_name":"Engineer", "is_peng":true, "is_teaching":true, "email":"email@uvic.ca", "department":"ECE" }' \
    http://localhost:5000/professors/
