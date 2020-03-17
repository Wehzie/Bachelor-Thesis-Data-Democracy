

import random
from simulation import simulation

# NOTE: hh is short for household or households

class firm(object):
    
    sim: object = None              # simulation a 
    money: int = None               # current balance of firm
    reserve: int = None             # savings beyond money balance
    num_items: int = None           # number of items in stock for selling
    item_price: int = None          # price a single item is sold for
    demand: int = None              # number of items sold last month
    num_employees: int = None       # firm can employ unlimited number of households
    list_employees: list = []       # list of currently employed hh
    wage: int = None                # money paid to each employed hh per month
    open_pos: bool = None           # whether a position for employment is open
    month_open_pos: int = None      # month the firm started looking to employ
    

    def __init__(self):
        pass

    ######## ######## ######## MONTH ######## ######## ########

    # Adjust wage by number of employees and employment target
    # employment target met -> decrease wage
    # insufficient employees -> increase wage

    # NOTE: Doesn't implement filledPosition
    def update_wage(self: firm, month: int):
        if self.month_open_pos == month - 1:             
            self.wage *= (1 + random.uniform(0, self.sim.f_param.get("price_adj_rate")))
        elif (month - self.month_open_pos) > self.sim.f_param.get("price_adj_prob"):
            self.wage *= (1 - random.uniform(0, self.sim.f_param.get("price_adj_rate")))

    def update_employees():
        pass

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
    