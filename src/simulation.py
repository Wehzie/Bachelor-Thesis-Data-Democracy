

class Simulation(object):
    '''
    The Simulation object contains instances of firms, households and the government.
    The Simulation sets parameters that control firm and household behavior.
    The main event loop method part of the Simulation object.
    '''

    ######## ######## ######## STATIC VARIABLES ######## ######## ########

    days_in_month = 21                  # number of working days in a month
    months_in_year = 12                 # number of months in a year

    # TODO: Initialize all parameters with randomness.
    f_param = {
        'num_firms': None,              # total number of firms
        'months_lo_wage': 24,           # gamma: duration (months) after which wage is decreased when all positions filled
        'wage_adj_rate': 0.019,         # delta: rate at which wages are adjusted
        'inv_up': 1,                    # phi_up: rate at which number of items in stock are considered too many
        'inv_lo': 0.25,                 # phi_lo: rate at which number of items in stock are considered too few    
        'price_up': 1.15,               # varphi_up: rate at which prices are considered too high
        'price_lo': 1.025,              # varphi_lo: rate at which prices are considered too low
        'price_adj_rate': 0.02,         # vartheta: rate at which prices are updated
        'price_adj_prob': 0.75,         # theta: probability at which prices are updated
        'tech_lvl': 3,                  # lambda: technology parameter influences an employees item production rate
        'buffer_rate': 0.1,             # chi: rate at which a firm builds a money buffer

        'lo_wage_months': 1,            # duration (months) of full employment after which wages are decreased

        'init_money': 0,                # firm's starting balance
        'init_reserve': 0,              # firm's starting savings
        'init_items': 50,               # firm's starting inventory
        'init_avg_price': 1,            # firm's average starting price
        'init_avg_wage': 52,            # firm's average starting wage
    }

    hh_param = {
        'num_hh': None,                     # total number of households
        'lower_vendor_price': 0.01,         # xi: percent by which a new vendor's prices must be cheaper, normalized to 1
        'unemployed_ask_num': 5,            # beta: number of firms an unemployed household asks for a job each month
        'repl_employer_prob': 0.1,          # pi: probability that a hh satisfied with its wage asks another firm for a job
        'cost_decay': 0.9,                  # alpha: rate at which monthly expenses decay relative to wealth
        'repl_vend_price_prob': 0.25,       # psi_price: probability of replacing a firm a hh buys from due to high prices 
        'repl_vend_inv_prob': 0.25,         # psi_quant: probability or replacing a firm a hh buys from due to little inventory
        'lo_res_wage_unemployed': 0.1,      # hh's reservation wage decrease rate during month of unemployment
                                            # reservation wage is the minimum wage a hh is willing to work for
        'demand_sat': 0.05,                 # hh is satisfied with buying a little less percent of items it planned to buy

        'init_money': 100,                  # hh's starting balance
        'num_vendors': 7,                   # number of firms a hh buys from
        'rw_change_employed': 1,            # reservation wage change during month of employment
        'rw_change_unemployed': 0.9,        # reservation wage change during month of unemployment
        'rw_change_fired': 1,               # reservation wage change at moment of being fired
    }

    g_param = {
        'tax_gamma': 4,                     # tax voting relies on this factor that expresses will for redistribution
        'rep_term_length': 48,              # representative government's term length in months
    }

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, num_months: int, num_runs: int, gov_type: str, num_f: int, num_hh: int, plot_param: dict):
        self.num_runs = num_runs            # the number of runs simulated
        self.num_months = num_months        # number of months simulated
        self.current_month = 0              # currently simulated month by number
        self.gov_type = gov_type            # the type of government used

        self.f_param['num_firms'] = num_f   # number of firms simulated
        self.hh_param['num_hh'] = num_hh    # number of households simulated

        self.firm_list = []                 # list of all firms in the model
        self.hh_list = []                   # list of all hh in the model

        self.stat = None                    # tracking, plotting and analyzing data
        self.gov = None                     # government responsible for tax and ubi

        self.plot_param = plot_param        # control plotting behavior
        self.print_hashes = '######## ######## ########'        # pretty command line printing

    ######## ######## ######## METHODS ######## ######## ########

    def print_sim_step(self, step: str):
        print(f"{self.print_hashes:<30} {step:>15}")

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

    # initialize the stat_run object
    def init_stat_run(self):
        self.stat = Stat_run(self.num_months, self.num_runs, self.gov_type, self.f_param['num_firms'], self.hh_param['num_hh'], self.plot_param)
        self.stat.set_sim(self)

    # initialize the government
    def init_government(self):
        if self.gov_type == 'none': return
        if self.gov_type == 'data': self.gov = Gov_data(self)
        if self.gov_type == 'rep': self.gov = Gov_rep(self)
        if self.gov_type == 'dir': self.gov = Gov_dir(self)

    # actions at the beginning of a month
    def act_bom(self):
        def act_bom_f():
            for f in self.firm_list:
                f.update_wage(self.current_month)
                f.update_hiring_status(self.current_month)
                f.update_price(self.current_month)
                f.reset()

        def act_bom_hh():
            random.shuffle(self.hh_list)
            for hh in self.hh_list:
                hh.reset_income()
                hh.find_cheaper_vendor()
                hh.find_stocked_vendor()
                hh.do_jobsearch()
                hh.plan_demand()

        act_bom_f()
        act_bom_hh()

    # actions each day of the month
    # hhs goods before firms produce since production takes time
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

        self.gov_action()

    def start_sim(self):
        self.print_sim_step("INITIALIZE AGENTS")
        self.init_firms()
        self.init_households()
        self.init_stat_run()
        self.init_government()
        self.print_sim_step("INVOKING EVENT LOOP")
        self.event_loop()

    def sum_hh_money(self) -> float:
        hh_sum = 0
        for hh in self.hh_list:
            hh_sum += hh.money
        return hh_sum

    def gov_action(self):
        if self.gov_type == 'none': return
        self.gov.vote_tax()
        self.gov.collect_tax()
        self.gov.calc_ubi()
        self.gov.pay_ubi()

    def event_loop(self):
        while(self.current_month < self.num_months):
            print(f"{self.print_hashes:<30} {'MONTH:':>15} {self.current_month:>10}")

            self.act_bom()
            for day in range(self.days_in_month):
                self.act_day()
            self.act_eom()
            self.stat.up_stat()

            self.current_month += 1

        if self.plot_param['plot_per_run']:
            print(f"\n{self.print_hashes:<30} {'CREATING PLOTS':>15}")
            self.stat.invoke_plots()

######## ######## ######## IMPORTS ######## ######## ########

from household import Household
from firm import Firm
from stat_run import Stat_run
from gov_data import Gov_data
from gov_rep import Gov_rep
from gov_dir import Gov_dir
import random
