# Simple Python Client-Server Application

This repository contains a simple client-server application implemented in Python using Unix domain sockets. The server randomly picks a card rank from a predefined set of cards (A to K) and sends the corresponding number to the client. The server also handles a 'SHUTDOWN' command to gracefully stop.

## Files

- `client.py`: The client script that connects to the server and requests a card rank.
- `server.py`: The server script that listens for client connections, processes requests, and responds with the corresponding card number.

## Usage

### Running the Server

1. Navigate to the directory containing the `server.py` script.
2. Run the server script using Python:
   ```sh
   python3 server.py
