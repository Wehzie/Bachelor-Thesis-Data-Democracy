

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: hh is short for household or households

class Household(object):
    
    money = None                    # current balance of hh
    daily_cost = None               # money spent daily by hh
    saving_param = None             # controls portion of monthly earings saved; 0 < saving_param < 1

    employer = None                 # hh has one employer firm (type B connection)
    firm_list = []                  # hh buys at up to 7 firms (type A connection)
                                    #   contains indices pointing to firms in simulation
    firms_lo_stock = []             # hh remembers firms with not enough goods in the last month
    
    res_wage = None                 # reservation wage, minimum wage hh works for
    rw_change_employed = None       # reservation wage change during month of employment
    rw_change_unemployed = None     # reservation wage change during month of unemployment
    rw_change_fired = None          # reservation wage change at moment of being fired

    ask_num_firms = None            # number of firms a hh asks for a job during a month of unemployment

    def __init__(self):
        pass

    ######## ######## ######## METHODS ######## ######## ########

    def fired():
        pass

    def receive_wage():
        pass

    def receive_profit():
        pass

    ######## ######## ######## MONTH ######## ######## ########

    # return list of vendors the hh doesn't buy from by index
    def non_vendor_firms(self, sim) -> [int]:
        pot_firm_list = list(range(0, sim.f_param.get("num_firms")))
        for firm in self.firm_list:
            del potential_firm_list[firm]
        return pot_firm_list

    # household tries to replace a vendor (firm it buys from) with a cheaper one
    def find_cheaper_firm(self, sim):
        # abort this method by chance
        if random.uniform(0, 1) > sim.hh_param.get("repl_vend_price_prob"):
            return

        # randomly select old firm by index in simulation
        old_firm = random.randrange(0, len(self.firm_list))

        # list of vendors the hh doesn't buy from by index
        pot_firm_list = self.non_vendor_firms(sim)

        # probability of choosing a new vendor is proportional to a firm’s number of employees
        #   weight of a firm is: firm's number of employees / total number of households 
        weight_list = []
        for firm in pot_firm_list:
            weight_list.append(sim.firm_list[firm].num_employees / sim.hh_param.get("num_hh"))

        # replace old firm if the new one's price is lower
        new_firm = random.choices(potential_firm_list, weight_list)[0]
        if sim.firm_list[new_firm].item_price < sim.firm_list[old_firm].item_price * (1 - sim.hh_param.get("lower_vendor_price")):
            self.firm_list[old_firm] = new_firm

    # household tries to replace a vendor when it previously had insufficient stock
    def find_stocked_firm(self, sim):
        # abort method when no vendor had low stock or by chance
        if not self.firms_lo_stock or random.uniform(0, 1) > sim.hh_param.get("repl_vend_inv_prob"):
            return
        
        # TODO: Probability should be proportional to the extend of the restriction
        # randomly select a firm from those that weren't able to satisfy demands
        lo_stock_firm = self.firms_lo_stock[random.randrange(0, len(self.firms_lo_stock))]

        # randomly choose among vendors the hh doesn't buy from
        new_firm = random.choice(self.non_vendor_firms(sim))

        self.firm_list[lo_stock_firm]


    def search_any_employer():
        pass

    def search_better_employer():
        pass

    def plan_month():
        pass

    ######## ######## ######## DAY ######## ######## ########

    def daily_buying():
        pass

######## ######## ######## IMPORTS ######## ######## ########

import random
from simulation import Simulation
from firm import Firm