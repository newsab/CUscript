
# saved as greeting-client.py
import Pyro4


# use name server object lookup uri shortcut
greeting_maker = Pyro4.Proxy("PYRONAME:CF_BÖSE")
print(greeting_maker.get_fortune())
