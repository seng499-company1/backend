while ! docker exec "backend_db" mysql --user="root" --password="root" -e "SELECT 1" >/dev/null 2>&1; 
do
    sleep 1
done
