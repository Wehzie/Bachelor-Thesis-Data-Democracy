

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

# NOTE: hh is short for household or households

class Simulation(object):
    
    ######## ######## ######## INSTANCE VARIABLES ######## ######## ########

    num_months = None                   # number of months simulated
    days_in_month = 21                  # number of working days in a month

    f_param = {
        # TODO: consider num_f in line with num_hh
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

        'init_money': 0,                # firm's starting balance
        'init_reserve': 0,              # firm's starting savings
        'init_items': 50,               # firm's starting inventory
        'init_avg_price': 1,            # firm's average starting price
        'init_avg_wage': 52,            # firm's average starting wage
    }

    hh_param = {
        'num_hh': 1000,                     # total number of households
        'lower_vendor_price': 0.01,         # xi: percent by which a new vendor's prices must be cheaper, normalized to 1
        'unemployed_ask_num': 5,            # beta: number of firms an unemployed household asks for a job each month
        'repl_employer_prob': 0.1,          # pi: probability that a hh satisfied with its wage asks another firm for a job
        'cost_decay': 0.9,                  # alpha: rate at which monthly expenses decay relative to wealth
        'repl_vend_price_prob': 0.25,       # psi_price: probability of replacing a firm a hh buys from due to high prices 
        'repl_vend_inv_prob': 0.25,         # psi_quant: probability or replacing a firm a hh buys from due to little inventory
        'lo_res_wage_unemployed': 0.1,      # hh's reservation wage decrease rate during month of unemployment
                                            # reservation wage is the minimum wage a hh is willing to work for
        'demand_sat': 0.95,                 # hh is satisfied with buying a little less percent of items it planned to buy

        'init_money': 100,                  # hh's starting balance
        'num_vendors': 7,                   # number of firms a hh buys from
        'rw_change_employed': 1,            # reservation wage change during month of employment
        'rw_change_unemployed': 0.9,        # reservation wage change during month of unemployment
        'rw_change_fired': 1,               # reservation wage change at moment of being fired
    }

    firm_list = []                      # list of all firms in the model
    hh_list = []                        # list of all hh in the model

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, num_months: int):
        self.num_months = num_months
        self.current_month = 0

    ######## ######## ######## METHODS ######## ######## ########

    def print_sim_step(self, step: str):
        print(f"######## ######## ######## {step} IN SIMULATION ######## ######## ########")

    # initialize a number of firms
    def init_firms(self):
        for firm in range(self.f_param.get("num_firms")):
            self.firm_list.append(Firm(self))

    # initialize a number of hhs
    def init_households(self):
        employer_idx = 0
        for hh in range(self.hh_param.get("num_hh")):
            # first, hhs are distributed such that each firm has one employee
            # afterwards, hhs are randomly assigned to an employer
            employer = self.firm_list[employer_idx] if employer_idx < len(self.firm_list) else random.choice(self.firm_list)
            self.hh_list.append(Household(self, employer))
            employer_idx += 1

    # actions each day of the month
    # TODO: comment on hhs buying before firms produce
    def act_day(self):
        def act_day_hh():
            random.shuffle(self.hh_list)
            for hh in self.hh_list:
                hh.buy_items()

        def act_day_f():
            for f in self.firm_list:
                f.produce_items()
        
        act_day_hh()
        act_day_f()

    # actions at the beginning of a month
    def act_bom(self):
        def act_bom_f():
            for f in self.firm_list:
                # TODO: should I impl start planning month?
                f.update_wage(self.current_month)
                f.update_hiring_status(self.current_month)
                f.update_price(self.current_month)
                f.reset_demand()

        def act_bom_hh():
            random.shuffle(self.hh_list)
            for hh in self.hh_list:
                hh.find_cheaper_vendor()
                hh.find_stocked_vendor()
                hh.do_jobsearch()
                hh.plan_demand()

        act_bom_f()
        act_bom_hh()

    # actions at the end of a month
    def act_eom(self):
        for f in self.firm_list:
            f.set_reserve()
            f.pay_profits()
        
        for f in self.firm_list:
            f.pay_wages()

        for hh in self.hh_list:
            hh.update_res_wage()

        for f in self.firm_list:
            f.make_layoff_decision()

    def start_sim(self):
        self.print_sim_step("INITIALIZE AGENTS")
        self.init_firms()
        self.init_households()
        self.print_sim_step("INVOKING EVENT LOOP")
        self.event_loop()

    def event_loop(self):
        while(self.current_month < self.num_months):
            self.print_sim_step(f"MONTH {self.current_month}")

            self.print_sim_step("DOING BOM")
            self.act_bom()
            self.print_sim_step(f"DOING {self.days_in_month} DAYS")
            for day in range(self.days_in_month):
                self.act_day()
            self.print_sim_step("DOING EOM")
            self.act_eom()

            self.current_month += 1

from household import Household
from firm import Firm
import random