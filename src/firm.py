

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: Imports are at end of file
# hh is short for household or households

class Firm(object):
    
    sim: object = None              # firm belongs to a simulation
    money: float = 0                # current balance of firm
    reserve: float = None           # savings beyond money balance

    num_items: int = None           # number of items in stock for selling
    lo_num_items: int = None        # at least have this many items in stock
    up_num_items: int = None        # don't have more than this items in stock
    item_price: float = None        # price a single item is sold for
    marginal_cost: float = None     # the price of producing one item
    lo_item_price: float = None     # don't let item cost fall lower than this
    up_item_price: float = None     # don't let item cost rise higher than this
    demand: int = None              # number of items sold last month
                                    # TODO: Verify this is how demand works. Consider renaming to demand_month

    list_employees: list = []       # list of currently employed hh by index as found in simulation
    wage: float = None              # money paid to each employed hh per month
    hiring_status: int = None       # ternary, where 1: hire, 0: no changes, -1: fire
    # TODO: Maybe I actually need two variables here for hiring and firing
    month_hiring: int = None        # month the firm started looking to employ
    
    def __init__(self, sim: object):
        self.sim = sim
        self.money = sim.f_param.get("init_money")
        self.reserve = sim.f_param.get("init_reserve")
        self.num_items = sim.f_param.get("init_items")
        self.item_price = sim.f_param.get("init_avg_price") + random.uniform(-0.5, 0.5) / 50
        self.demand = 0
        self.list_employees = []
        self.wage = sim.f_param.get("init_avg_wage") + random.uniform(-0.5, 0.5) / 50
        self.hiring_status = 0
        self.month_hiring = 0
        # TODO: What's up with month to start planning in JS impl?

    ######## ######## ######## METHODS ######## ######## ########

    # increase wage when no employees are found
    def update_wage(self, month: int):
        if self.month_hiring < month:
            self.wage *= (1 + random.uniform(0, self.sim.f_param.get("price_adj_rate")))
        # TODO: impl decreasing wages when all positions filled?

    # demand determines how many items should be kept in stock
    def update_item_bounds(self):
        lo_num_items = self.sim.f_param.get("inv_up") * self.demand
        up_num_items = self.sim.f_param.get("inv_lo") * self.demand

    # employ more people when not enough items are produced
    def update_hiring_status(self, month: int):
        update_item_bounds(self)

        if self.num_items < self.lo_num_items:
            self.hiring_status = 1
            self.month_hiring = month
        elif self.num_items > self.up_num_items:
            self.hiring_status = -1

    # wage determines item price
    def update_price_bounds(self):
        self.marginal_cost = (self.wage / self.sim.days_in_month) / self.sim.f_param.get("tech_lvl")
        self.lo_item_price = self.sim.f_param.get("price_lo") * self.marginal_cost
        self.up_item_price = self.sim.f_param.get("price_up") * self.marginal_cost
    
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
        elif many_items and hi_price and chance:
            self.item_price *= (1 - self.sim.f_param.get("price_adj_rate") * random.uniform(0, 1))

    # TODO: evaluate open_position, filled_position, close_position?
    # add household to list of employees
    def hire(self, employee: object):
        self.list_employees.append(employee)
        self.hiring_status = 0

    # remove employee from list of employees
    def grant_leave(self, employee: object):
        self.list_employees.remove(employee)

    # remove random employee from list of employees
    # inform employee of unemployment
    def fire_random_employee(self):
        employee = random.choice(self.list_employees)
        self.list_employees.remove(employee)
        employee.fired()
        self.hiring_status = 0
    
    # choose whether to fire an employee based on hiring status
    def make_layoff_decision(self):
        if self.hiring_status == -1: self.fire_random_employee()

    # produce new items for firm's inventory
    def produce_items(self):
        self.num_items += self.sim.f_param.get("tech_lvl") * len(self.list_employees)


    # return number of items sold, reduce inventory, increase money and demand
    def sell_items(self, demand_deal: int) -> int:
        num_items_sold = min(self.num_items, demand)
        self.num_items -= num_items_sold
        self.money += num_items_sold * self.item_price
        self.demand += demand_deal
        return num_items_sold

    # return total money to pay employees each month
    def sum_wages(self) -> int:
        return self.wage * len(self.list_employees)

    # pay employees the full wage
    # if insufficient money available then reduce wage
    def pay_wages(self):
        if self.money < self.sum_wages():
            self.wage = self.money / len(self.list_employees)

        for employee in self.list_employees:
            employee.receive_wage(self.wage)

        self.money -= self.sum_wages()

    # determine how much money is set back as buffer
    def set_reserve(self):
        frac_monthly_wages = self.sim.get("buffer_rate") * self.sum_wages()
        self.reserve = max(0, min(frac_monthly_wages, self.money))
        # TODO: is max(0, ) necessary? Can wages or money be < 0 ?

    # return the sum of money owned by all employed households
    def sum_hh_money(self) -> int:
        sum = 0
        for employee in self.list_employees:
            # TODO: Is this necessary? Can hh.money be negative?
            sum += employee.money if employee.money != 0 else 0
        return sum

    # if profits have been made and employees have any money then pay profits
    # richer employees receive higher profits
    def pay_profits(self):
        # TODO: Can profit and hh_money be < 0?
        profit = self.money - self.reserve - self.sum_wages()
        if profit > 0 and self.sim.sum_hh_money() > 0:
            for employee in self.list_employees:
                employee.receive_profit()

    # reset monthly item demand to zero
    def reset_demand(self):
        self.demand = 0
    
######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation
from household import Household