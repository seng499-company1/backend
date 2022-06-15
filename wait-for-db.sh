while ! docker exec backend_db touch /tmp/execWorks >/dev/null 2>&1; 
do
    sleep 1
done
