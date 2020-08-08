from collections import defaultdict
import pdb

class SampleAmple():
    def __init__(self, ctx, name, symbol):
        self.name = name
        self.symbol = symbol
        self.total_supply = 0
        self.balances = defaultdict(float)  # address : balance # Really percent of supply
        self.allowances = defaultdict(float) # main address { allowed address: amount}
        self.admin = ctx.sender
        self.address = ctx.AR.register(self)

        self.last_rebase = None

    #
    def mint(self, ctx, amount, addresses):
        if not (ctx.sender == self.admin):
            return False
        # could probably use work
        # pdb.set_trace()
        self.total_supply = amount * len(addresses)
        print("Total Supply: {}".format(self.total_supply))
        new_bal = self._unitToBalance(300)
        for address in addresses:
            self.balances[address] += new_bal
        return True


    #
    def transfer(self, ctx, amount, address):
        if Address.isZero(ctx.sender):
            return False
        bal = self.getBalance(ctx.address)
        if bal > amount:
            return False
        return self._transfer(ctx, amount, address)
    #
    def _trasfer(self, ctx, amount, address):
        transfer_bal = self._unitToBalance(amount)
        cur_bal_from = self.balances[ctx.sender]
        cur_bal_to = self.balances[address]
        start_total = cur_bal_from + cur_bal_to
        #
        cur_bal_to += transfer_bal
        cur_bal_from -= transfer_bal
        if start_total == cur_bal_to + cur_bal_from:
            self.balances[ctx.sender] = cur_bal_from
            self.balances[address] = cur_bal_to
            return True
        return False
    #
    def getBalance(self, address):
        return self._balanceToUnit(self.balances[address])
    #
    def _balanceToUnit(self, balance):
        return balance * self.total_supply
    #
    def _unitToBalance(self, unit):
        return unit / self.total_supply
    #
    def rebase(self, ctx, supply_delta):
        if not (ctx.sender == self.admin):
            return False
        self.total_supply += supply_delta
        self.last_rebase = ctx.block_number
        print("Rebase: New Supply = {}".format(self.total_supply))
        return True

    #
    # def transferFrom(self, amount, address):
    #     pass
    # #
    # def allow(self, amount, address):
    #     pass
    #
    # def getAllowance(self, address, allow_address ):
    #     pass
    #
