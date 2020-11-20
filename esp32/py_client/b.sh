#IP=$(/sbin/ip route | awk '/default/ { print $3 }')
IP="192.168.49.182"
mosquitto_pub -h $IP -i "client/b" -t "password" -m "hi"
