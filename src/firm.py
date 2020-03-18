

# NOTE: Imports are at end of file
# hh is short for household or households

class Firm(object):
    
    sim: object = None              # simulation a 
    money: int = 0                  # current balance of firm
    reserve: int = None             # savings beyond money balance
    num_items: int = None           # number of items in stock for selling
    item_price: int = None          # price a single item is sold for
    demand: int = None              # number of items sold last month
    num_employees: int = None       # firm can employ unlimited number of households
    list_employees: list = []       # list of currently employed hh
    wage: int = None                # money paid to each employed hh per month
    open_pos: bool = None           # whether a position for employment is open
    month_open_pos: int = None      # month the firm started looking to employ
    

    def __init__(self, sim: object):
        self.sim = sim

    def testmethod(self):
        print("Simparam: " + str(self.sim.f_param.get("price_adj_rate")))

    ######## ######## ######## MONTH ######## ######## ########

    # Adjust wage by number of employees and employment target
    # Can't find employees? -> increase wage
    def update_wage(self, month: int):
        if self.month_open_pos < month:
            self.wage *= (1 + random.uniform(0, self.sim.f_param.get("price_adj_rate")))


    def update_employees(self, month: int):
        up_num_items = self.sim.f_param.get("inv_up") * self.demand
        lo_num_items = self.sim.f_param.get("inv_lo") * self.demand

        #marg_cost = (self.wage / self.sim.

    def plan_month():
        pass

    ######## ######## ######## DAY ######## ######## ########

    def daily_production():
        pass

    ######## ######## ######## PAYDAY ######## ######## ########

    def pay_wage():
        pass

    def pay_profit():
        pass
    
######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation