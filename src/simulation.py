

from household import household
from firm import firm

def get_firm_param():
    firm_param = {
        'num_firms': 100,
        'fi_price_prob': 0.78,
        'fi_price_speed': 0.019,
        'fi_wage_prob': 0.07,
        'fi_wage_speed': 0.02,
        'fi_min_inv': 0.25,
        'fi_max_inv': 1,
        'fi_min_profit': 1.025,
        'fi_max_profit': 1.15,
    }

    return firm_param

def get_hh_param():
    hh_param = {
        'num_households': 1000,
        'hh_savings': 0.885,
        'hh_res_wage_employed': 1,
        'hh_res_wage_fired': 1,
        'hh_res_wage_unemployed': 0.9,
    }

    return hh_param

def init_households():
    hh_param = get_hh_param()
    hh_list = []
    for hh in range(hh_param.get("num_households")):
        hh_list.append(household())
    
    return hh_list

def init_firms():
    pass

def start_sim(num_months):
    
    hh_list = init_households()
    print("test")

    for month in range(num_months):
        # plan month
        # perform day
        # end of months

        pass