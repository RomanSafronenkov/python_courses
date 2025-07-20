class Server:
    NUM_SERVERS = 0

    def __init__(self):
        self.buffer = []
        self.ip = self.set_ip()
        self.router = None

    @classmethod
    def set_ip(cls):
        ip = cls.NUM_SERVERS + 1
        cls.NUM_SERVERS += 1
        return ip

    def send_data(self, data):
        self.router.buffer.append(data)

    def get_data(self):
        received_data = self.buffer
        self.buffer = []
        return received_data

    def get_ip(self):
        return self.ip

class Router:
    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, server):
        self.servers[server.ip] = server
        server.router = self

    def unlink(self, server):
        server.router = None
        del self.servers[server.ip]

    def send_data(self):
        for data in self.buffer:
            server = self.servers.get(data.ip)
            if server is not None:
                server.buffer.append(data)
        self.buffer = []


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip

router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
router.link(Server())
sv_to = Server()
router.link(sv_to)
print(router.servers)

sv_from.send_data(Data("Hello", sv_to.get_ip()))
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
sv_to.send_data(Data("No way", sv_from2.get_ip()))
print(router.buffer)
router.send_data()
print(router.buffer)

msg_lst_from = sv_from.get_data()
msg_lst_from2 = sv_from2.get_data()
msg_lst_to = sv_to.get_data()
print(*[data.data for data in msg_lst_from])
print(*[data.data for data in msg_lst_from2])
print(*[data.data for data in msg_lst_to])

