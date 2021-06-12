from client import Client

client = Client('127.0.0.1', 12001)
client.put("palm.cpu", 0.5, timestamp=1150864247)

client.put("palm.cpu", 2.0, timestamp=1150864248)

client.put("palm.cpu", 0.5, timestamp=1150864248)

client.put("eardrum.cpu", 3, timestamp=1150864250)

client.put("eardrum.cpu", 4, timestamp=1150864251)

client.put("eardrum.memory", 4200000)

print(client.get("*"))
print(client.get("palm.cpu"))
print(client.get("eardrum.memory"))
print(client.get("fake"))
# print(client.get('cpu'))
# print('1'.join(['ok', 'bruh', 'damn', 'lel', '1']))