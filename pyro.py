import Pyro4
# use the URI that the server printed:
thing = Pyro4.Proxy("PYRONAME:myrtk")
print(thing.getPosition())   # prints 84
