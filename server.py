import socket
import threading

HOST = "0.0.0.0"   # sab network interfaces par sunega
PORT = 5000

# Lock: shared cheezon (print aur counter) ko safe rakhta hai
lock = threading.Lock()
total_clients = 0   # shared variable


def safe_print(message):
    """Ek time par sirf ek thread print kare, taake output mix na ho."""
    lock.acquire()
    try:
        print(message)
    finally:
        lock.release()


def handle_client(conn, addr):
    global total_clients
    thread_name = threading.current_thread().name
    client_ip, client_port = addr

    # Shared counter update karte waqt lock zaroori hai
    lock.acquire()
    try:
        total_clients += 1
        current = total_clients
    finally:
        lock.release()

    safe_print(f"[CONNECTED] Thread: {thread_name} | IP: {client_ip} | "
               f"Port: {client_port} | Active clients: {current}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:                 # client ne connection band kar diya
                break

            message = data.decode().strip()
            if message.lower() == "exit":
                conn.sendall(b"Goodbye!")
                break

            safe_print(f"[{thread_name}] {client_ip}:{client_port} -> {message}")
            conn.sendall(f"Server received: {message}".encode())
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        lock.acquire()
        try:
            total_clients -= 1
            current = total_clients
        finally:
            lock.release()
        safe_print(f"[DISCONNECTED] Thread: {thread_name} | IP: {client_ip} | "
                   f"Port: {client_port} | Active clients: {current}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    safe_print(f"[STARTED] Server listening on port {PORT}...")

    client_number = 0
    try:
        while True:
            conn, addr = server.accept()          # blocking call
            client_number += 1
            t = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                name=f"Client-Thread-{client_number}",
            )
            t.start()                              # har client ka apna thread
    except KeyboardInterrupt:
        safe_print("\n[STOPPED] Server band ho raha hai.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
