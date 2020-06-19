
# TODO: track income during n months
# TODO: collect tax after n months
# TODO: pay UBI monthly after n months have passed
# TODO: goal is to minimize Gini Coefficient

# government does not keep state or make profit, money that is collected is immediately spent
# single tax value for all instead of tiered tax

class Gov_naive(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly

    # taxrate is proportional to the gini index
    def vote_tax(self):
        if len(self.sim.stat.hh_stat['metric']['gini']) == 0:           # before the gini index is available a fixed tax rate is set
            self.tax_rate = 0.1 
        else:
            self.tax_rate = self.sim.stat.hh_stat['metric']['gini'][-1] * self.sim.g_param['naive_tax_rate']

    # collect taxes from all households
    def collect_tax(self):
        for hh in self.sim.hh_list:
            self.money += hh.pay_tax(self.tax_rate)

    # ubi is equal for all hhs each month
    def calc_ubi(self):
        self.ubi = self.money / self.sim.hh_param['num_hh']

    # pay equal ubi to all households
    def pay_ubi(self):
        for hh in self.sim.hh_list:
            hh.receive_ubi(self.ubi)
        self.money = 0

    # collect tax at end of year
    # pay out ubi next year based on amassed money of previous year
    # ubi changes each year
    # tax changes each 4 years

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation