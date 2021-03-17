import Pyro4
# use the URI that the server printed:
uri = "PYRO:Pyro.NameServer@172.16.0.3:34291"
thing = Pyro4.Proxy(uri)
print(thing.method(42)) 