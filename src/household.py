

class Household(object):
    '''
    A household has two kinds of relationships with firms.
    Firstly, a household can have one firm as an employer.
    Secondly, a household can have multiple firms as preferred vendors.
    Based on the wage of a firm a household may search for other employers.
    Based on the ability to satisfy item demand a household may change its preferred vendors.
    '''

    def __init__(self, sim: object, employer: object):
        self.sim: object = sim                                  # hh belongs to a simulation
        self.money: float = sim.hh_param.get("init_money")      # current balance of hh
        self.employer: object = employer                        # hh has one employer firm (type B connection)
        self.vendor_list: list = []                             # hh buys at up to 7 firms (type A connection)
        for vendor in range(sim.hh_param.get("num_vendors")):
            self.vendor_list.append(random.choice(self.get_non_vendor_firms()))
        self.blocked_vendors: list = []                         # hh remembers firms with not enough goods in the last month
        self.blocked_v_amount: list = []
        self.res_wage: float = 0                                # reservation wage, minimum wage hh works for
        self.daily_demand: int = 0                              # number of items a hh aims to buy each day
        self.income: float = 0                                  # sum of wage and profit within a given month 

    ######## ######## ######## METHODS ######## ######## ########

    # set hh to have no employer
    def fired(self):
        self.employer = None
        self.res_wage *= self.sim.hh_param.get("rw_change_fired")

    # increase hh balance by received wage
    def receive_wage(self, employer_money):
        self.money += employer_money
        self.income += employer_money

    # increase hh balance by received profits
    def receive_profit(self, profit_money):
        self.money += profit_money
        self.income += profit_money

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
            weight_list.append(len(vendor.list_employees) / self.sim.hh_param.get("num_hh"))

        # replace old firm if the new one's price is lower
        # if the new firm was initially blacklisted then unlist it
        new_firm = random.choices(pot_vendor_list, weight_list)[0]
        if new_firm.item_price < old_firm.item_price * (1 - self.sim.hh_param.get("lower_vendor_price")):
            if old_firm in self.blocked_vendors: self.blocked_vendors.remove(old_firm)
            if new_firm in self.blocked_vendors: self.blocked_vendors.remove(new_firm)
            self.vendor_list.remove(old_firm)
            self.vendor_list.append(new_firm)

    # household tries to replace a vendor when it had insufficient stock last month
    def find_stocked_vendor(self):
        # abort method when no vendor had low stock or by chance
        if not self.blocked_vendors or random.uniform(0, 1) > self.sim.hh_param.get("repl_vend_inv_prob"):
            return
        
        # randomly select a firm from those that weren't able to satisfy demands
        # probability should be proportional to the extent of the restriction in the original model
        # as a implemented simplification
        # probability is proportional to the least number of items in stock
        weight_list = []
        max_items = max([v.num_items for v in self.blocked_vendors])
        for vendor in self.blocked_vendors:
            weight_list.append(abs(vendor.num_items - max_items))
        lo_stock_firm = random.choices(self.blocked_vendors, weight_list)[0]

        # randomly choose among vendors the hh doesn't buy from
        new_firm = random.choice(self.get_non_vendor_firms())

        # replace low stock vendor and reset the low stock vendors        
        self.vendor_list.remove(lo_stock_firm)
        self.vendor_list.append(new_firm)
        self.blocked_vendors = []

    # unemployed hhs are eager to find a job
    # employed hhs are less eager to find a job
    # since employed hhs have a job their wage expectations grow
    def do_jobsearch(self):
        if self.employer == None:
            self.search_any_employer()
        else:
            self.res_wage *= self.sim.hh_param.get("rw_change_employed")
            self.search_better_employer()

    # unemployed hh searches for an employer paying at least the hh's reservation wage
    def search_any_employer(self):
        # unemployed hh randomly approaches a number of firms
        for attempt in range(0, self.sim.hh_param.get("unemployed_ask_num")):
            pot_firm = random.choice(self.sim.firm_list)
            if pot_firm.hiring_status == 1 and pot_firm.wage >= self.res_wage:
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
            if pot_firm.hiring_status == 1 and pays_enough and pays_better:
                self.employer.grant_leave(self)
                pot_firm.hire(self)
                self.employer = pot_firm
        
    # determine quantity of items a hh consumes each day of the beginning month
    def plan_demand(self):
        def get_mean_item_price() -> float:
            sum = 0
            for vendor in self.vendor_list:
                sum += vendor.item_price
            return sum / len(self.vendor_list)
        
        mean_price = get_mean_item_price()

        # no_decay_demand example: 100€ money / 1€ banana_price = buy 100 bananas this month
        no_decay_demand = self.money // mean_price

        # if no_decay_demand is > 1 then, since 0 < cost_decay < 1, the power function returns a value smaller than no_decay_demand
        # if no_decay_demand is < 1 then the power function returns a value larger than no_decay_demand
        #   in this case, money < monthly_demand * mean_price, this scenario is solved by taking monthly_demand = no_decay_demand
        #   so that money == no_decay_demand * mean_price
        monthly_demand = min(pow(no_decay_demand, self.sim.hh_param.get("cost_decay")), no_decay_demand)
        self.daily_demand = monthly_demand // self.sim.days_in_month

    # hhs buy items from their preferred vendors to satisfy their daily demand
    def buy_items(self):
        remaining_demand: int = self.daily_demand
        
        unvisited_vendors = self.vendor_list.copy()
        for vendor_count in self.vendor_list:
            vendor = random.choice(unvisited_vendors)
            unvisited_vendors.remove(vendor)

            item_ask: int = min(remaining_demand, self.money // vendor.item_price)    # when hh has more demand than money, don't overspend
            items_sold: int = vendor.sell_items(item_ask)
            remaining_demand -= items_sold
            self.money -= items_sold * vendor.item_price

            # when there is need to buy from another firm
            # then the initial firm didn't satisfy demand
            # due to high price or little inventory
            # so the firm is blacklisted as vendor
            if remaining_demand > 0 and vendor not in self.blocked_vendors:
                self.blocked_vendors.append(vendor)

            # stop method if hh has no money, demand is satisfied or all vendors have been visited
            demand_satisfied: bool = remaining_demand <= self.sim.hh_param.get("demand_sat") * self.daily_demand
            if self.money <= 0 or demand_satisfied: return

    # hhs get used to their wage and expect this as their new reservation wage
    def update_res_wage(self):
        if self.employer is not None and self.employer.wage > self.res_wage:
            self.res_wage = self.employer.wage

    # hhs pay a portion of their monthly income to the government but not more than they have
    def pay_tax(self, tax_rate: float) -> float:
        tax = self.income * tax_rate
        if self.money - tax < 0: tax = self.money
        self.money -= tax
        return tax

    # hhs receive a universal basic income each month
    def receive_ubi(self, ubi: float):
        self.money += ubi

    # reset how much wage and profit was received this month
    def reset_income(self):
        self.income = 0

######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation
from firm import Firm