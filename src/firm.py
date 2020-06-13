

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: Imports are at end of file
# hh is short for household or households

class Firm(object):
    
    def __init__(self, sim: object):
        self.sim: object = sim                                  # firm belongs to a simulation
        self.money: float = sim.f_param.get("init_money")       # current balance of firm
        self.reserve: float = sim.f_param.get("init_reserve")   # how much money to not pay out as profits
        self.num_items: int = sim.f_param.get("init_items")     # number of items in stock for selling
        self.lo_num_items: int = None                           # at least have this many items in stock
        self.up_num_items: int = None                           # don't have more than this items in stock
        rnd = random.uniform(-0.5, 0.5) / 50                    # generate small float around +-0
        self.item_price: float = sim.f_param.get("init_avg_price") + rnd    # price a single item is sold for
        self.marginal_cost: float = None                        # the price of producing one item
        self.lo_item_price: float = None                        # don't let item cost fall lower than this
        self.up_item_price: float = None                        # don't let item cost rise higher than this
        self.demand: int = 0                                    # number of items sold this month so far
        self.list_employees: list = []                          # list of currently employed hh by index as found in simulation
        rnd = random.uniform(-0.5, 0.5) / 50                    # generate small float around +-0
        self.wage: float = sim.f_param.get("init_avg_wage") + rnd   # money paid to each employed hh per month
        self.hiring_status: int = 0                             # ternary, where 1: hire, 0: no changes, -1: fire
        # TODO: Maybe I actually need two variables here for hiring and firing
        self.month_hiring: int = 0                              # month the firm started looking to employ
        # TODO: What's up with month to start planning in JS impl?

        # TODO: make negative balance impossible, in a non-hacky way
    ######## ######## ######## METHODS ######## ######## ########

    # increase wage when no employees are found
    # decrease wage after n months of full employment
    def update_wage(self, month: int):
        if self.hiring_status == 1 and self.month_hiring < month:
            self.wage *= (1 + random.uniform(0, self.sim.f_param["wage_adj_rate"]))
        if self.hiring_status <= 0 and month - self.month_hiring > self.sim.f_param["lo_wage_months"]:
            self.wage *= (1 - random.uniform(0, self.sim.f_param["wage_adj_rate"]))

    # demand determines how many items should be kept in stock
    def update_item_bounds(self):
        self.lo_num_items = self.sim.f_param["inv_up"] * self.demand        # upper item limit
        self.up_num_items = self.sim.f_param["inv_lo"] * self.demand        # lower item limit

    # employ more people when not enough items are produced
    def update_hiring_status(self, month: int):
        self.update_item_bounds()

        if self.num_items < self.lo_num_items:
            self.hiring_status = 1
            self.month_hiring = month
        elif self.num_items > self.up_num_items:
            self.hiring_status = -1
        else: self.hiring_status = 0

    # wage determines item price
    def update_price_bounds(self):
        # marginal cost is the cost of producing one more item
        # one worker produce one item each day
        # so marginal cost ist the cost of paying another worker for a day
        self.marginal_cost = (self.wage / self.sim.days_in_month) / self.sim.f_param["tech_lvl"]
        self.lo_item_price = self.sim.f_param["price_lo"] * self.marginal_cost
        self.up_item_price = self.sim.f_param["price_up"] * self.marginal_cost
    
    # increase price when few items in stock and sold cheaply
    # lower price when many items in stock and sold expensively
    def update_price(self, month: int):
        self.update_item_bounds()
        self.update_price_bounds()

        chance = random.uniform(0, 1) < self.sim.f_param["price_adj_prob"]
        few_items = self.num_items < self.lo_num_items
        many_items = self.num_items > self.up_num_items
        lo_price = self.item_price < self.up_item_price
        hi_price = self.item_price > self.up_item_price
        
        if few_items and lo_price and chance:
            self.item_price *= (1 + self.sim.f_param["price_adj_rate"] * random.uniform(0, 1))
        elif many_items and hi_price and chance:
            self.item_price *= (1 - self.sim.f_param["price_adj_rate"] * random.uniform(0, 1))

    # TODO: evaluate open_position, filled_position, close_position?
    # add household to list of employees
    def hire(self, employee: object):
        self.list_employees.append(employee)
        self.hiring_status = 0

    # remove employee from list of employees
    def grant_leave(self, employee: object):
        if employee in self.list_employees: 
            self.list_employees.remove(employee) # BUG: list.remove(x): x not in list
            self.hiring_status = 0

    # remove random employee from list of employees
    # inform employee of unemployment
    def fire_random_employee(self):
        if len(self.list_employees) < 1: return # TODO: The need of doing this shows a bug probably
        
        employee = random.choice(self.list_employees)
        self.list_employees.remove(employee)
        employee.fired()
    
    # choose whether to fire an employee based on hiring status
    # after considering firing, reset hiring status
    def make_layoff_decision(self):
        if self.hiring_status == -1: self.fire_random_employee()
        self.hiring_status = 0

    # produce new items for firm's inventory
    def produce_items(self):
        self.num_items += self.sim.f_param["tech_lvl"] * len(self.list_employees)

    # return number of items sold, reduce inventory, increase money and demand
    def sell_items(self, item_ask: int) -> int:
        num_items_sold: int = min(item_ask, self.num_items)
        self.num_items -= num_items_sold
        self.money += num_items_sold * self.item_price
        self.demand += item_ask
        return num_items_sold

    # return total money to pay employees each month
    def sum_wages(self) -> int:
        return self.wage * len(self.list_employees)

    # pay employees the full wage
    # if insufficient money available then reduce wage
    def pay_wages(self):
        if self.money < self.sum_wages() and len(self.list_employees) > 0:
            self.wage = self.money / len(self.list_employees)

        for employee in self.list_employees:
            employee.receive_wage(self.wage)

        self.money -= self.sum_wages()

    # determine how much money is not paid out as profits
    def set_reserve(self):
        frac_monthly_wages = self.sim.f_param["buffer_rate"] * self.sum_wages()
        self.reserve = max(0, min(frac_monthly_wages, self.money))

    # return the sum of money owned by all households in the simulation
    def sum_hh_money(self) -> int:
        sum = 0
        for hh in self.sim.hh_list:
            sum += hh.money if hh.money > 0 else 0
        return sum

    # if profits have been made then pay profits to all households in the simulation
    # richer households receive higher profits
    def pay_profits(self):
        profit = max(0, self.money - self.sum_wages() - self.reserve)
        sum_hh_money = self.sum_hh_money()
        if profit > 0:
            for hh in self.sim.hh_list:
                hh.receive_profit(profit * (hh.money / sum_hh_money))

        self.money -= profit

    # reset monthly item demand to zero
    def reset_demand(self):
        self.demand = 0
    
######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation
from household import Household