IP=$(/sbin/ip route | awk '/default/ { print $3 }')
mosquitto_sub -h $IP -i "client/a" -t "password"
