from collections import defaultdict


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
        self.long_balance = defaultdict(float)  # address : balance
        self.short_balance = defaultdict(float)
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
    def depositShort(self, ctx, amount):
        self._deposit(ctx, amount, False)
    #
    def depositLong(self, ctx, amount):
        self._deposit(ctx, amount, True)
    #
    def _deposit(self, ctx, amount, isLong = True):
        # Transfer to contract
        result = ctx.AR[self.token_contract].transfer(ctx, amount, self.address)
        if result:
            # Validate supply matches expectation
            local_supply =ctx.AR[self.token_contract].getBalance(self.address)
            if local_supply - amount = self.total_supply:
                # Update local balance
                if isLong:
                    self.long_balance[ctx.sender] += amount
                else:
                    self.short_balance[ctx.sender] += amount
            else:
                return False
        else:
            return False
    #
    def claimShort(self, ctx, amount):

        pass
    #
    def claimLong(self, ctx):
        pass
    #
    def _claim(self, ctx, amount, isLong = True):
        pass
    #
    def _getNewLongBalance(self, address):
        old_bal = self.long_balance[address]
        old_bal / self.

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
