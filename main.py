import random

# Local
from sample_ample import SampleAmple
from tug_of_rebase import TugOfRebase

# General Classes
class AddressRegistry():
    def __init__(self):
        self.registry = {} # address : object

    def register(self, object, address = None):
        if not address:
            address = self.new()
        self.registry[address] = object
        return address

    def new(self):
        return Address(self)
#
class Address():
    def __init__(self, address_registry, ens = None, zero=False):
        self.AR = address_registry
        self.ens = ens
        if zero:
            self.address = "0x0"+"0"*16
        else:
            self.address = "0x"+str(int(random.random()*10**16))

    def isZero(address):
        if address == "0x0"+"0"*16:
            return True
        return False

    def register(self, object):
        self.AR.register(object)
        return True
#
class Context():
    def __init__(self, address, address_registry, chain = []):
        self.sender = address
        self.chain = chain
        self.AR = address_registry
        if bool(chain):
            self.block_number = chain[-1].block_number + 1
        else:
            self.block_number = 1
        self.result = None
    #
    def setResult(self, result):
        self.result = set_result
    #
    def output(self):
        if self.result == True:
            self.chain.append(self)
        return self.chain
#
class Main():
    def __init__(self, address_registry):
        # Init Context
        self.ctx = None
        # Populate Base Address
        self.users = [] # 0 is admin
        for i in range(100):
            self.users.append(Address(address_registry))
        # Init Contracts
        self.newContext(self.users[0], address_registry)
        self.SA = SampleAmple(self.ctx, 'Ampleforth','AMPL')
        self.updateContext(self.users[0])
        self.TOR = TugOfRebase(self.ctx, self.SA.address)
    #
    # New context called before each "block"
    def newContext(self, address, addrss_registry, chain = []):
        self.ctx = Context(address, addrss_registry, chain)
    #
    def updateContext(self, address):
        self.ctx = Context(address, self.ctx.AR, self.ctx.chain)
    #
    # Mints equally to all addresses
    def seedAmple(self, amount):
        self.updateContext(self.users[0])
        self.SA.mint(self.ctx, amount, self.users)
    #
    def rebase(self, amount):
        self.updateContext(self.users[0])
        return self.SA.rebase(self.ctx, amount)

def start():
    AR = AddressRegistry()
    m = Main(AR)
    m.seedAmple(300)
    print("Balance User 4: {}".format(m.SA.getBalance(m.users[4])))
    m.rebase(30000)
    print("Balance User 4: {}".format(m.SA.getBalance(m.users[4])))
    return m

if __name__ =="__main__":
    m = start()
