

# this government models a direct democracy where individuals cast direct votes for a tax rate

# each month all households are income taxed with a single tax rate
# each month all households receives a universal basic income
# all money that is collected from taxes is spent on ubi

# the tax rate changes each year
# the ubi changes each year

class Gov_dir(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly

    # each household proposes a tax rate
    # all households have equal weight
    # by averaging indiviual votes a final tax rate is calculated
    def vote_tax(self):
        # only tax households once enough data is available
        if len(self.sim.stat.hh_stat['metric']['gini']) < 12:
            self.tax_rate = 0
            return

        year_gini_list = self.sim.stat.hh_stat['metric']['gini'][-12:]
        gini = sum(year_gini_list) / len(year_gini_list)                    # mean gini index of the last year
        
        median_money = self.sim.hh_list[self.sim.hh_param['num_hh'] // 2].money
        self.tax_rate = 0
        for hh in self.sim.hh_list:
            # gini index is multiplied by a measure of how far a hh is below or above the median money
            self.tax_rate += gini * median_money / hh.money
        self.tax_rate = self.tax_rate / self.sim.hh_param['num_hh']

        # tax rate shouldn't exceed 100% of the income
        if self.tax_rate > 1: self.tax_rate = 1

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
import random