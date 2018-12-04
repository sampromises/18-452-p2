sudo ip link add name mesh-bridge type bridge
sudo ip link set dev eth0 master mesh-bridge
sudo ip link set dev bat0 master mesh-bridge
sudo ip link set up dev eth0
sudo ip link set up dev bat0
sudo ip link set up dev mesh-bridge