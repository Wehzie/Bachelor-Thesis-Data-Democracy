

# this government considers economic parameters for setting taxes
# individuals and representatives are not part of the decision making process

# each month all households are income taxed with a single tax rate
# each month all households receives a universal basic income
# all money that is collected from taxes is spent on ubi

# the tax rate changes each month
# the ubi changes each month

class Gov_naive(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly

    # calculate a tax rate from the gini index
    def vote_tax(self):
        # only tax households once enough data is available
        if len(self.sim.stat.hh_stat['metric']['gini']) == 0:           
            self.tax_rate = 0
            return

        # taxrate is proportional to the gini index
        self.tax_rate = self.sim.stat.hh_stat['metric']['gini'][-1] * self.sim.g_param['naive_tax_rate']

    # collect taxes from all households each month
    def collect_tax(self):
        for hh in self.sim.hh_list:
            self.money += hh.pay_tax(self.tax_rate)

    # ubi is equal for all hhs each month
    def calc_ubi(self):
        self.ubi = self.money / self.sim.hh_param['num_hh']

    # pay equal ubi to all households each month
    def pay_ubi(self):
        for hh in self.sim.hh_list:
            hh.receive_ubi(self.ubi)
        self.money = 0

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation