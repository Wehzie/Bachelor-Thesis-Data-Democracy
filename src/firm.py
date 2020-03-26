

# NOTE: Imports are at end of file
# hh is short for household or households

class Firm(object):
    
    sim: object = None              # firm belongs to a simulation
    money: int = 0                  # current balance of firm
    reserve: int = None             # savings beyond money balance

    num_items: int = None           # number of items in stock for selling
    lo_num_items = None             # at least have this many items in stock
    up_num_items = None             # don't have more than this items in stock
    item_price: int = None          # price a single item is sold for
    marginal_cost: int = None       # the price of producing one item
    lo_item_price: int = None       # don't let item cost fall lower than this
    up_item_price: int = None       # don't let item cost rise higher than this
    demand: int = None              # number of items sold last month

    list_employees: list = []       # list of currently employed hh by index as found in simulation
    wage: int = None                # money paid to each employed hh per month
    open_pos: bool = None           # whether a position for employment is open
    month_open_pos: int = None      # month the firm started looking to employ
    

    def __init__(self, sim: object):
        self.sim = sim

    def testmethod(self):
        print("Simparam: " + str(self.sim.f_param.get("price_adj_rate")))

    ######## ######## ######## MONTH ######## ######## ########

    # increase wage when no employees are found
    def update_wage(self, month: int):
        if self.month_open_pos < month:
            self.wage *= (1 + random.uniform(0, self.sim.f_param.get("price_adj_rate")))

    # demand determines how many items should be kept in stock
    def update_item_bounds(self):
        self.sim.f_param.get("inv_up") * self.demand
        self.sim.f_param.get("inv_lo") * self.demand

    # wage determines item price
    def update_price_bounds(self):
        self.marginal_cost = (self.wage / self.sim.days_in_month) / self.sim.f_param.get("tech_lvl")
        self.lo_item_price = self.sim.f_param.get("price_lo") * marginal_cost
        self.up_item_price = self.sim.f_param.get("price_up") * marginal_cost

    # employ more people when not enough items are produced
    def update_employees(self, month: int):
        update_item_bounds(self)

        if self.num_items < lo_num_items:
            self.open_pos = True
            self.month_open_pos = month
    
    # increase price when few items in stock and sold cheaply
    # lower price when many items in stock and sold expensively
    def update_price(self, month: int):
        update_item_bounds(self)
        update_price_bounds(self)

        chance = random.uniform(0, 1) < self.sim.f_param.get("price_adj_prob")
        few_items = self.num_items < self.lo_num_items
        many_items = self.num_items > self.up_num_items
        lo_price = self.item_price < self.up_item_price
        hi_price = self.item_price > self.up_item_price
        
        if few_items and lo_price and chance:
            self.item_price *= (1 + self.sim.f_param.get("price_adj_rate") * random.uniform(0, 1))
        elif: many_items and hi_price and chance:
            self.item_price *= (1 - self.sim.f_param.get("price_adj_rate") * random.uniform(0, 1))

    # add household to list of employees
    def hire(self, employee: object):
        self.list_employees.append(employee)

    # remove employee from list of employees
    # inform employee of unemployment
    def fire(self, employee_idx: int):
        fired_employee = self.list_employees.pop(employee_idx)
        fired_employee.fired()          # NOTE: Is this OOP best practice? Observer pattern

    # remove employee from list of employees
    def quit(self, employee_idx: int):
        fired_employee = self.list_employees.pop(employee_idx)

    

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
from household import Household