IP=$(/sbin/ip route | awk '/default/ { print $3 }')
mosquitto_pub -h $IP -i "client/b" -t "password" -m "hi"
