

# data driven government
# taxes are adjusted monthly
# parliament is replaced by the entire population of households
# for each household a target tax is calculated instead of categorizing them into 5 parties
# all households have equal weight



class Gov_data(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly

    def vote_tax(self):

        # before a gini index has been calculated assume an arbitrary tax rate
        if len(self.sim.stat.hh_stat['metric']['gini']) == 0:
            self.tax_rate = 0.1
        else:
            median_money = self.sim.hh_list[self.sim.hh_param['num_hh'] // 2].money
            self.tax_rate = 0
            for hh in self.sim.hh_list:
                self.tax_rate += self.sim.stat.hh_stat['metric']['gini'][-1] * median_money / hh.money
            self.tax_rate = self.tax_rate /self.sim.hh_param['num_hh']

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

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import random