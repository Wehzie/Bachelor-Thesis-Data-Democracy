

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: hh is short for household or households

class Simulation(object):
    
    ######## ######## ######## INSTANCE VARIABLES ######## ######## ########

    num_months = None                   # number of months simulated
    days_in_month = 21                  # number of working days in a month

    f_param = {
        'num_firms': 100,               # total number of firms
        'months_lo_wage': 24,           # gamma: in number of months. duration after which wage is increased when all job positions filled
        'wage_adj_rate': 0.019,         # delta: rate at which wages are adjusted
        'inv_up': 1,                    # phi_up: rate at which number of items in stock are considered too many
        'inv_lo': 0.25,                 # phi_lo: rate at which number of items in stock are considerd too few    
        'price_up': 1.15,               # varphi_up: rate at which prices are considered too high
        'price_lo': 1.025,              # varphi_lo: rate at which prices are considered too low
        'price_adj_rate': 0.02,         # vartheta: rate at which prices are updated
        'price_adj_prob': 0.75,         # theta: probability at which prices are updated
        'tech_lvl': 3,                  # lambda: technology parameter applied to an employee's natural work force in item production
        'buffer_rate': 0.1,             # chi: rate at which a firm builds a money buffer
    }

    hh_param = {
        'num_hh': 1000,                     # total number of households
        'lower_vendor_price': 0.01,         # xi: percent by which a new vendor's prices must be cheaper, normalized to 1
        'unemployed_ask_num': 5,            # beta: number of firms an unemployed household asks for a job each month
        'pi': 0.1,                          # pi: probability that a hh satisfied with its wage asks another firm for a job
        'cost_decay': 0.9,                  # alpha: rate at which monthly expenses decay relative to wealth
        'repl_vend_price_prob': 0.25,       # psi_price: probability of replacing a firm a hh buys from due to high prices 
        'repl_vend_inv_prob': 0.25,         # psi_quant: probability or replacing a firm a hh buys from due to little inventory
                                            # reservation wage: minimum a hh is willing to work for
        'lo_res_wage_unemployed': 0.1,      # hh's reservation wage decrease rate during month of unemployment
    }

    firm_list = []                      # list of all firms in the model
    hh_list = []                        # list of all hh in the model

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, num_months: int):
        self.num_months = num_months

    ######## ######## ######## METHODS ######## ######## ########

    def init_households(self):
        hh_list = []
        for hh in range(hh_param.get("num_households")):
            hh_list.append(household())
        
        return hh_list

    def init_firms(self):
        pass

    def start_sim(self):
        print("######## ######## ######## START SIMULATION ######## ######## ########")

        testfirm = Firm(self)
        testfirm.testmethod()

        print("######## ######## ######## STOP SIMULATION ######## ######## ########")

from household import Household
from firm import Firm