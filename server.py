import socket
import os

cards = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13
}

# UNIXソケットをストリームモードで作成します
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# このサーバが接続を待つUNIXソケットのパスを設定します
server_address = '/tmp/socket_file'

# 以前の接続が残っていた場合に備えて、サーバアドレスをアンリンク（削除）します
try:
    os.unlink(server_address)
# サーバアドレスが存在しない場合、例外を無視します
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

# サーバアドレスにソケットをバインド（接続）します
sock.bind(server_address)

# ソケットが接続要求を待機するようにします
sock.listen(1)

# 無限ループでクライアントからの接続を待ち続けます
while True:
    # クライアントからの接続を受け入れます
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # ループが始まります。これは、サーバが新しいデータを待ち続けるためのものです。
        while True:
            # ここでサーバは接続からデータを読み込みます。
            # 16という数字は、一度に読み込むデータの最大バイト数です。
            data = connection.recv(16)

            # 受け取ったデータはバイナリ形式なので、それを文字列に変換します。
            # 'utf-8'は文字列のエンコーディング方式です。
            data_str = data.decode('utf-8')

            # 受け取ったデータを表示します。
            print('Received ' + data_str)

            # もしデータがあれば（つまりクライアントから何かメッセージが送られてきたら）以下の処理をします。
            if data:
                # Correction: Lookup the card rank and store it in a separate variable
                card_number = cards.get(data_str, 'Invalid card')  # Corrected to use a separate variable

                # Correction: Construct the response based on whether the card is valid or not
                if card_number != 'Invalid card':
                    response = f'Your card: {data_str} Your card rank: {card_number}'  # Corrected to use both data_str and card_number
                else:
                    response = 'Invalid card'  # Corrected to handle invalid card case

                # 処理したメッセージをクライアントに送り返します。
                # ここでメッセージをバイナリ形式（エンコード）に戻してから送信します。
                connection.sendall(response.encode())

            # クライアントからデータが送られてこなければ、ループを終了します。
            else:
                print('no data from', client_address)
                break

    # 最終的に接続を閉じます
    finally:
        print("Closing current connection")
        connection.close()
