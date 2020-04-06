

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: hh is short for household or households

class Household(object):

    # TODO: type hinting
    sim: object = None              # hh belongs to a simulation
    money = None                    # current balance of hh
    daily_cost = None               # money spent daily by hh
    saving_param = None             # controls portion of monthly earings saved; 0 < saving_param < 1

    employer = None                 # hh has one employer firm (type B connection)
    firm_list = []                  # hh buys at up to 7 firms (type A connection)
                                    #   contains indices pointing to firms in simulation
    firms_lo_stock = []             # hh remembers firms with not enough goods in the last month
    
    res_wage = None                 # reservation wage, minimum wage hh works for
    # TODO: move rw_change parameters to sim
    rw_change_employed = None       # reservation wage change during month of employment
    rw_change_unemployed = None     # reservation wage change during month of unemployment
    rw_change_fired = None          # reservation wage change at moment of being fired

    ask_num_firms = None            # number of firms a hh asks for a job during a month of unemployment

    def __init__(self):
        pass

    ######## ######## ######## METHODS ######## ######## ########

    # set hh to have no employer
    def fired(self):
        self.employer = None
        # TODO: reservation wage adjustments

    # increase hh balance by received wage
    def receive_wage(self, employer_money):
        self.money += employer_money
        # TODO: reservation wage adjustments

    # increase hh balance by received profits
    def receive_profit(self, profit_money):
        self.money += profit_money

    # return list of vendors the hh doesn't buy from
    def get_non_vendor_firms(self) -> [object]:
        pot_firm_list = self.sim.firm_list.copy()
        for firm in self.firm_list:
            pot_firm_list.remove(firm)
        return pot_firm_list

    # return a list of all firms in the simulation except for the current employer
    def get_non_employer_firms(self) -> [object]:
        pot_firm_list = self.sim.firm_list.copy()
        pot_firm_list.remove(self.employer)
        return pot_firm_list

    # return whether a hh is employed or not
    def is_employed(self) -> bool:
        return self.employer is not None

    # household tries to replace a vendor (firm it buys from) with a cheaper one
    def find_cheaper_firm(self):
        # abort this method by chance
        if random.uniform(0, 1) > self.sim.hh_param.get("repl_vend_price_prob"): return

        # randomly select a firm the household buys from
        old_firm = random.choice(self.firm_list)

        # list of vendors the hh doesn't buy
        pot_firm_list = self.get_non_vendor_firms()

        # probability of choosing a new vendor is proportional to a firm’s number of employees
        #   weight of a firm is: firm's number of employees / total number of households 
        weight_list = []
        for firm in pot_firm_list:
            weight_list.append(firm.num_employees / self.sim.hh_param.get("num_hh"))

        # replace old firm if the new one's price is lower
        new_firm = random.choices(pot_firm_list, weight_list)[0]
        if new_firm.item_price < old_firm.item_price * (1 - self.sim.hh_param.get("lower_vendor_price")):
            self.firm_list.remove(old_firm)
            self.firm_list.append(new_firm)

    # household tries to replace a vendor when it previously had insufficient stock
    def find_stocked_firm(self):
        # abort method when no vendor had low stock or by chance
        if not self.firms_lo_stock or random.uniform(0, 1) > self.sim.hh_param.get("repl_vend_inv_prob"):
            return
        
        # TODO: Probability should be proportional to the extend of the restriction
        # randomly select a firm from those that weren't able to satisfy demands
        lo_stock_firm = random.choice(self.firms_lo_stock)

        # randomly choose among vendors the hh doesn't buy from
        new_firm = random.choice(self.get_non_vendor_firms())

        self.firm_list.remove(lo_stock_firm)
        self.firm_list.append(new_firm)

    # unemployed hh searches for an employer paying at least the hh's reservation wage
    def search_employer(self):
        if self.employer is not None: return # TODO: should only unemployed hhs search?

        # hh randomly approaches a number of firms
        for attempt in range(0, self.sim.hh_param.get("unemployed_ask_num")):
            pot_firm = random.choice(self.sim.firm_list)
            if pot_firm.hiring is True and pot_firm.wage >= self.res_wage:
                self.employer = pot_firm
                pot_firm.hire(self)
                return
        
        # hh lowers it's reservation wage when no employer was found
        if self.employer is None: self.res_wage *= self.rw_change_unemployed

    # hhs paid less than reservation wage search a better employer
    # hhs paid reservation wage also sometimes look for better pay
    def search_better_employer(self):
        only_employee = len(self.employer.list_employees) <= 1
        bad_pay = elf.employer.wage < self.res_wage
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
            self.res_wage *= self.rw_change_employed
        
    # determine quantity of items a hh consumes each day of the beginning month
    def plan_demand(self):
        def get_mean_item_price() -> float:
            sum = 0
            for firm in self.firm_list:
                sum += firm.item_price
            return sum / len(self.firm_list)
        
        mean_price = get_mean_item_price()

        # no_decay_demand example: 100€ money / 1€ banana_price = buy 100 bananas this month
        no_decay_demand = self.money / mean_price
        # if no_decay_demand is > 1 then, since 0 < cost_decay < 1, the power function returns a value smaller than no_decay_demand
        # if no_decay_demand is < 1 then the power function returns a value larger than no_decay_demand
        #   in this case, money < monthly_demand * mean_price, this scenario is solved by taking monthly_demand = no_decay_demand
        #   so that money == no_decay_demand * mean_price
        monthly_demand = min(pow(no_decay_demand, self.sim.hh_param.get("cost_decay")), no_decay_demand)
        self.daily_demand = monthly_demand / self.sim.days_in_month

    def buy_items(self):
        remaining_demand = self.daily_demand

        # TODO: should be while-loop? is it possible that hh has no money to begin with?
        for vendor in self.firm_list:
            vendor = random.choice(self.firm_list)
            item_ask = min(remaining_demand, self.money / vendor.item_price)
            items_sold = vendor.sell_items(item_ask)
            remaining_demand -= items_sold
            self.money -= items_sold * vendor.item_price
            # TODO: implement restricting vendors if they can't satisfy the item_ask

            # stop method if hh has no money, demand is satisfied or all vendors have benn visited
            demand_satisfied: bool = remaining_demand <= 1 - self.sim.hh_param.get("demand_sat") * self.daily_demand
            if self.money <= 0 or demand_satisfied: return

######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation
from firm import Firm
