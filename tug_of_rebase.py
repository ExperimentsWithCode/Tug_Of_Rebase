

class TugOfRebase():
    def __init__(self, ctx, token_contract):
        # General
        self.admin = ctx.sender
        self.token_contract = token_contract
        # Address
        self.address = ctx.AR.register(self)
        # Local
        self.total_supply = 0
        self.long_total = 0
        self.short_total = 0
        self.long_balance = {}  # address : balance
        self.short_balance = {}
        self.rebase_count = 0
        self.lock_number = 0
        self.last_token_supply = 0
        self.last_rebase_size = 0
    #
    def processRebase(self):
        pass

    #
    def lock(self, ctx):
        # if self._isLocked(ctx):
        #     return False  #?
        # self.lock_number = ctx.block_number
        # self.last_token_supply = ctx.AR[self.token_contract].total_supply
        # return True
        pass
    #
    def _isLocked(self, ctx):
        pass
        # last_rebase_block = ctx.AR[self.token_contract].last_rebase
        # return self.lock_number - last_rebase_block < 0
    #
    def unlock(self, ctx):
        # set rebase numbers
        pass
    #
    def depositShort(self, ctx):
        pass
    #
    def depositLong(self, ctx):
        pass
    #
    def claimShort(self, ctx):
        pass
    #
    def claimLong(self, ctx):
        pass
    #
    def _calcRebaseDiff(self, ctx):
        return self._calcRebaseSize(ctx) - (0.9 * self.last_rebase_size)
    #
    def _calcSupplyDelta(self, ctx):
        return ctx.AR[self.token_contract].total_supply - self.last_token_supply
    #
    def _calcRebaseSize(self, ctx):
        return self._calcSupplyDelta(ctx) / self.last_token_supply
    #
    def _calcAdjust(self, ctx):
        # Get Post Rebase Balance
        new_balance = ctx.AR[self.token_contract].getBalance()
        # Calc offsets from unequal provisions
        offset_long = self.long_balance /(self.long_balance + self.short_balance)
        offset_short = self.short_balance /(self.long_balance + self.short_balance)
        # Apply offsets
        new_long_bal = (new_balance - self.total_supply()) * offset_long + self.long_balance
        new_short_bal = (new_balance - self.total_supply()) * offset_short + self.short_balance
        # Confirm Balances Match up
        if not self._validateAdjust(new_long_bal, new_short_bal, new_balance):
            return False
        # Apply Rebase
        rebase_diff = self._calcRebaseDiff(ctx)
        if rebase_diff > 0: # Longs win
            new_short_shift = self.short_balance * rebase_diff
            new_short_bal -= new_short_shift
            new_long_bal += new_short_shift
        else:               # Shorts Win
            new_long_shift = self.long_balance * rebase_diff
            new_long_bal -= new_long_shift
            new_short_bal += new_long_shift
        if not self._validateAdjust(new_long_bal, new_short_bal, new_balance):
            return False
        self.long_balance = new_long_bal
        self.short_balance = new_short_bal
    #
    def _validateAdjust(self, long, short, new):
        if new == long + short:
            return True
        else:
            print("Could not calc adjust. Balances did not sync")
            print(new - (long + short))
            return False
    #
    # def _calcLongAdjust(self):
    #     new_total = self.long_total
    #     new_total *= (1 + self._rebase_size())
    #     if self._didLongWin():
    #         return {'new_total': new_total, 'tribute': 0}
    #     else:
    #         adj_rebase = self.last_rebase_size / self._calcRebaseSize()
    #         adj_new_total = new_total *
    #         return {'new_total': new_total, 'tribute': 0}
