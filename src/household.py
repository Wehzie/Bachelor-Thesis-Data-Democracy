

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: hh is short for household or households

class Household(object):

    sim: object = None              # hh belongs to a simulation
    money: float = None             # current balance of hh
    employer: object = None         # hh has one employer firm (type B connection)
    vendor_list: list = []          # hh buys at up to 7 firms (type A connection)
    vendors_lo_stock: list = []     # hh remembers firms with not enough goods in the last month
    res_wage: float = None          # reservation wage, minimum wage hh works for

    def __init__(self, sim: object, employer: object):
        self.sim = sim
        self.money = sim.hh_param.get("init_money")
        self.employer = employer
        for vendor in sim.hh_param.get("num_vendors"):
            self.vendor_list.append(random.choice(self.get_non_vendor_firms()))
        self.res_wage = 0           # initially any wage is accepted

    ######## ######## ######## METHODS ######## ######## ########

    # set hh to have no employer
    def fired(self):
        self.employer = None
        self.res_wage *= self.sim.hh_param.get("rw_change_fired")

    # increase hh balance by received wage
    def receive_wage(self, employer_money):
        self.money += employer_money
        if employer_money > self.res_wage: self.res_wage = employer_money

    # increase hh balance by received profits
    def receive_profit(self, profit_money):
        self.money += profit_money

    # return list of vendors the hh doesn't buy from
    def get_non_vendor_firms(self) -> [object]:
        pot_vendor_list = self.sim.firm_list.copy()
        for vendor in self.vendor_list:
            pot_vendor_list.remove(vendor)
        return pot_vendor_list

    # return a list of all firms in the simulation except for the current employer
    def get_non_employer_firms(self) -> [object]:
        pot_employer_list = self.sim.firm_list.copy()
        pot_employer_list.remove(self.employer)
        return pot_employer_list

    # return whether a hh is employed or not
    def is_employed(self) -> bool:
        return self.employer is not None

    # household tries to replace a vendor (firm it buys from) with a cheaper one
    def find_cheaper_vendor(self):
        # abort this method by chance
        if random.uniform(0, 1) > self.sim.hh_param.get("repl_vend_price_prob"): return

        # randomly select a firm the household buys from
        old_firm = random.choice(self.vendor_list)

        # list of vendors the hh doesn't buy
        pot_vendor_list = self.get_non_vendor_firms()

        # probability of choosing a new vendor is proportional to a firm’s number of employees
        #   weight of a firm is: firm's number of employees / total number of households 
        weight_list = []
        for vendor in pot_vendor_list:
            weight_list.append(vendor.num_employees / self.sim.hh_param.get("num_hh"))

        # replace old firm if the new one's price is lower
        new_firm = random.choices(pot_vendor_list, weight_list)[0]
        if new_firm.item_price < old_firm.item_price * (1 - self.sim.hh_param.get("lower_vendor_price")):
            self.vendor_list.remove(old_firm)
            self.vendor_list.append(new_firm)

    # household tries to replace a vendor when it previously had insufficient stock
    def find_stocked_vendor(self):
        # abort method when no vendor had low stock or by chance
        if not self.vendors_lo_stock or random.uniform(0, 1) > self.sim.hh_param.get("repl_vend_inv_prob"):
            return
        
        # TODO: Probability should be proportional to the extend of the restriction
        # randomly select a firm from those that weren't able to satisfy demands
        lo_stock_firm = random.choice(self.vendors_lo_stock)

        # randomly choose among vendors the hh doesn't buy from
        new_firm = random.choice(self.get_non_vendor_firms())

        self.vendor_list.remove(lo_stock_firm)
        self.vendor_list.append(new_firm)

    # TODO: give some explanation here
    def do_jobsearch(self):
        if self.employer == None:
            self.search_any_employer()
        else:
            self.search_better_employer()

    # unemployed hh searches for an employer paying at least the hh's reservation wage
    def search_any_employer(self):
        if self.employer is not None: return # TODO: should only unemployed hhs search?

        # hh randomly approaches a number of firms
        for attempt in range(0, self.sim.hh_param.get("unemployed_ask_num")):
            pot_firm = random.choice(self.sim.firm_list)
            if pot_firm.hiring is True and pot_firm.wage >= self.res_wage:
                self.employer = pot_firm
                pot_firm.hire(self)
                return
        
        # hh lowers it's reservation wage when no employer was found
        if self.employer is None: self.res_wage *= self.sim.hh_param.get("rw_change_unemployed")

    # hhs paid less than reservation wage search a better employer
    # hhs paid reservation wage also sometimes look for better pay
    def search_better_employer(self):
        only_employee = len(self.employer.list_employees) <= 1
        bad_pay = self.employer.wage < self.res_wage
        chance = random.uniform(0, 1) < self.sim.hh_param.get("repl_employer_prob")

        if self.is_employed() and not only_employee and bad_pay or chance:
            pot_firm = random.choice(self.get_non_employer_firms())

            pays_enough = pot_firm.wage > self.res_wage
            pays_better = pot_firm.wage > self.employer.wage
            if pot_firm.hiring and pays_enough and pays_better:
                self.employer.grant_leave(self)
                pot_firm.hire(self)
                self.employer = pot_firm
            
            # TODO: Move this to somewhere else or remove
            self.res_wage *= self.sim.hh_param.get("employed")
        
    # determine quantity of items a hh consumes each day of the beginning month
    def plan_demand(self):
        def get_mean_item_price() -> float:
            sum = 0
            for vendor in self.vendor_list:
                sum += vendor.item_price
            return sum / len(self.vendor_list)
        
        mean_price = get_mean_item_price()

        # no_decay_demand example: 100€ money / 1€ banana_price = buy 100 bananas this month
        no_decay_demand = self.money / mean_price
        # if no_decay_demand is > 1 then, since 0 < cost_decay < 1, the power function returns a value smaller than no_decay_demand
        # if no_decay_demand is < 1 then the power function returns a value larger than no_decay_demand
        #   in this case, money < monthly_demand * mean_price, this scenario is solved by taking monthly_demand = no_decay_demand
        #   so that money == no_decay_demand * mean_price
        monthly_demand = min(pow(no_decay_demand, self.sim.hh_param.get("cost_decay")), no_decay_demand)
        self.daily_demand = monthly_demand / self.sim.days_in_month

    # TODO: comment
    def buy_items(self):
        remaining_demand = self.daily_demand

        # TODO: should be while-loop? is it possible that hh has no money to begin with?
        for vendor in self.vendor_list:
            vendor = random.choice(self.vendor_list)
            item_ask = min(remaining_demand, self.money / vendor.item_price)
            items_sold = vendor.sell_items(item_ask)
            remaining_demand -= items_sold
            self.money -= items_sold * vendor.item_price
            # TODO: implement restricting vendors if they can't satisfy the item_ask

            # stop method if hh has no money, demand is satisfied or all vendors have been visited
            demand_satisfied: bool = remaining_demand <= 1 - self.sim.hh_param.get("demand_sat") * self.daily_demand
            if self.money <= 0 or demand_satisfied: return

    # TODO: comment
    def update_res_wage(self):
        if self.employer is not None and self.employer.wage > self.res_wage:
            self.res_wage = self.employer.wage

######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation
from firm import Firm
