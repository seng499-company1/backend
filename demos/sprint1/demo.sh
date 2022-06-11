curl -X POST -H "Content-Type: application/json" \
    -d '{"first_name":"Mr", "last_name":"Engineer", "is_peng":True, "is_teaching":True, "email":"email@uvic.ca", "department":"ECE" }' \
    http://localhost:5000/professors/
