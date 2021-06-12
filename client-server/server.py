import asyncio

storage = {}


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        pass
        # self.storage = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = self.process_data(data.decode('utf-8'))
        self.transport.write(response.encode('utf-8'))

    def process_data(self, data):
        data = data.split('\n')[0]
        data = data.split(' ')

        request, data = data[0], data[1:]
        if request == 'put':

            if len(data) != 3:
                return 'error\nwrong command\n\n'
            metric_name, metric_value, timestamp = data

            try:
                metric_value = float(metric_value)
                timestamp = int(timestamp)
            except ValueError:
                return 'error\nwrong command\n\n'

            metric_value = float(metric_value)
            timestamp = int(timestamp)
            if metric_name not in storage.keys():
                storage[metric_name] = []

            for idx, content in enumerate(storage[metric_name]):
                if content[0] == timestamp:
                    del storage[metric_name][idx]

            storage[metric_name].append((timestamp, metric_value))
            return 'ok\n\n'

        elif request == 'get':
            if len(data) != 1:
                return 'error\nwrong command\n\n'
            metric_name = data[0]

            if metric_name == '*':
                if not storage:
                    return 'ok\n\n'
                response = ['ok']
                for key in storage:
                    content = storage[key]
                    for timestamp, metric_value in content:
                        response.append(f'{key} {metric_value} {timestamp}')
                response.append('\n')
                response = '\n'.join(response)
                return response

            else:
                response = ['ok']
                if metric_name not in storage:
                    return 'ok\n\n'
                content = storage[metric_name]
                for timestamp, metric_value in content:
                    response.append(f'{metric_name} {metric_value} {timestamp}')
                response.append('\n')
                response = '\n'.join(response)
                return response

        else:
            return 'error\nwrong command\n\n'


if __name__ == '__main__':
    run_server('127.0.0.1', 12001)
