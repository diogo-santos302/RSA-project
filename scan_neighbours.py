import socket
import neighbours

def get_current_neighbours() -> list:
    with neighbours.lock:
        return neighbours.neighbours
        
def try_to_connect(ip, port) -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result

def scan_neighbours(max_number_of_neighbours: int):
    if max_number_of_neighbours > 255:
        raise ValueError("Maximum number of neighbours should not be higher than 255!")
    network_range = "10.1.1.0/24"
    broker_port = 1883
    available_pis = get_current_neighbours()
    for host in range(1, max_number_of_neighbours):
        ip_address = f"10.1.1.{host}"
        # ip_address = "localhost"
        print(ip_address)
        result = try_to_connect(ip_address, broker_port)
        if result == 0:
            if ip_address not in available_pis:
                print(f"Added {ip_address}")
                available_pis.append(ip_address)
                neighbours.add_neighbour(ip_address)
        else:
            if ip_address in available_pis:
                print(f"Removed {ip_address}")
                available_pis.remove(ip_address)
                neighbours.remove_neighbour(ip_address)
