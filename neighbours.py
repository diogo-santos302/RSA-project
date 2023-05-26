import threading

# Create a lock object
lock = threading.Lock()

# Shared region
neighbours = []

def add_neighbour(ip):
    # Acquire the lock before accessing/modifying the shared data
    lock.acquire()
    
    try:
        # Perform operations on the shared data
        neighbours.append(ip)
    finally:
        # Release the lock to allow other threads to access the shared data
        lock.release()
        
def remove_neighbour(ip):
	# Acquire the lock before accessing/modifying the shared data
    lock.acquire()
    try:
        # Perform operations on the shared data
        neighbours.remove(ip)
    finally:
        # Release the lock to allow other threads to access the shared data
        lock.release()
