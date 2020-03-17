

from household import household
from firm import firm

# NOTE: hh is short for household or households

class simulation(object):
    
    ######## ######## ######## INSTANCE VARIABLES ######## ######## ########

    num_months = None                   # number of months simulated

    f_param = {
        'num_firms': 100,               # total number of firms
        'price_adj_prob': 0.78,         # probability that a firm adjusts item prices
        'price_adj_rate': 0.019,        # rate at which prices are adjusted
        'wage_adj_prob': 0.07,          # probability that a firm adjusts wages
        'wage_adj_rate': 0.02,          # rate at which wages are updated
        'inv_lo': 0.25,                 # rate at which number of items in stock are considerd too few    
        'inv_up': 1,                    # rate at which number of items in stock are considered too many
        'price_lo': 1.025,              # rate at which prices are considered too low
        'price_up': 1.15,               # rate at which prices are considered too high
    }

    hh_param = {
        'num_hh': 1000,                     # total number of households
        'cr_decay': 0.885,                  # rate at which monthly expenses decay relative to wealth

        # reservation wage: minimum a hh is willing to work for
        'res_wage_employed': 1,             # reservation wage during month of employment
        'res_wage_fired': 1,                # reservation wage in month of being fired
        'res_wage_unemployed': 0.9,         # reservation wage during month of unemployment
    }

    firm_list = []          # list of all firms in the model
    hh_list = []            # list of all hh in the model

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, num_months: int):
        

    ######## ######## ######## METHODS ######## ######## ########

    def init_households(self: simulation):
        hh_list = []
        for hh in range(hh_param.get("num_households")):
            hh_list.append(household())
        
        return hh_list

    def init_firms(self: simulation):
        self.firm_list = 

    def start_sim(num_months):
        
        hh_list = init_households()
        print("test")

        for month in range(num_months):
            # plan month
            # perform day
            # end of month

            pass