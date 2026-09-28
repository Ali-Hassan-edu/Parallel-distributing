import socket

SERVER_IP = "127.0.0.1"   # same computer; alag PC ho to server ka IP likhein
PORT = 5000


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
    except ConnectionRefusedError:
        print("Server chal nahi raha. Pehle server.py run karein.")
        return

    print("Connected to server. Message likhein ('exit' likh kar bahar niklein).")

    try:
        while True:
            message = input("You: ")
            if not message.strip():
                continue

            client.sendall(message.encode())
            reply = client.recv(1024)
            if not reply:
                print("Server ne connection band kar diya.")
                break

            print("Server:", reply.decode())

            if message.strip().lower() == "exit":
                break
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        client.close()
        print("Disconnected.")


if __name__ == "__main__":
    main()
