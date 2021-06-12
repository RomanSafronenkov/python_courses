import socket
import time


class ClientError(OSError):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.sock = socket.socket()
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))

    def get(self, metric_name):
        try:
            request = f'get {metric_name}\n'
            self.sock.sendall(request.encode('utf-8'))

            response = self.sock.recv(4096).decode('utf-8')
            if not response.endswith('\n\n'):
                raise ClientError(r'Invalid response format, no \n\n symbol at the end')

            response = response.split('\n\n')[0]
            response = response.split('\n')

            status, response = response[0], response[1:]
            if not response:
                return {}
            if set(map(lambda x: len(x.split(' ')), response)) != {3}:
                raise ClientError('Invalid response format, len is not 3')

            if status != 'ok':
                raise ClientError('Invalid format or "error" in response occurred')

            result = {}
            for metric in response:
                name, metric_value, timestamp = metric.split(' ')
                if name not in result:
                    result[name] = []

                try:
                    metric_value = float(metric_value)
                    timestamp = int(timestamp)
                except ValueError as err:
                    raise ClientError(err) from None

                result[name].append(tuple((timestamp, metric_value)))

            for key in result.keys():
                result[key].sort(key=lambda x: x[0])
            return result
        except socket.timeout as err:
            raise ClientError('Timeout Error', err) from None

    def put(self, metric_name, metric_value, timestamp=None):
        try:
            if timestamp is None:
                timestamp = int(time.time())

            data_to_send = f'put {metric_name} {metric_value} {timestamp}\n'
            self.sock.sendall(data_to_send.encode('utf-8'))
            response = self.sock.recv(1024).decode('utf-8')
            if response != 'ok\n\n':
                raise ClientError
        except socket.timeout as err:
            raise ClientError('Error putting the data to the server', err) from None

    def close(self):
        try:
            self.sock.close()
        except socket.error as err:
            raise ClientError('Error closing the socket', err)
