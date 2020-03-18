

# NOTE: hh is short for household or households

class Household(object):
    
    money = None                    # current balance of hh
    daily_cost = None               # money spent daily by hh
    saving_param = None             # controls portion of monthly earings saved; 0 < saving_param < 1

    employer = None                 # hh has one employer firm (type B connection)
    firm_list = []                  # hh buys at up to 7 firms (type A connectinon)
    firms_restricted = []           # hh remembers firms with not enough goods
    
    res_wage = None                 # reservation wage, minimum wage hh works for
    rw_change_employed = None       # reservation wage change during month of employment
    rw_change_unemployed = None     # reservation wage change during month of unemployment
    rw_change_fired = None          # reservation wage change at moment of being fired

    ask_num_firms = None            # number of firms a hh asks for a job during a month of unemployment

    def __init__(self):
        pass

    ######## ######## ######## MONTH ######## ######## ########

    def find_cheaper_firm():
        pass

    def replace_firm():
        pass

    def search_any_employer():
        pass

    def search_better_employer():
        pass

    def plan_month():
        pass

    ######## ######## ######## DAY ######## ######## ########

    def daily_buying():
        pass
    