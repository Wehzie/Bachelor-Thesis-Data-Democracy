

# households are randomly sampled from the population of hhs
# based on income a hh belongs to a party
# each party votes for a different tax rate
# the poorest party votes for highest taxes

class Gov_rep(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly

    def vote_tax(self):
        hh_money_sorted = sorted(self.sim.hh_list, key=lambda hh: hh.money) # sort households by money
        quint = hh_money_sorted[199::200]                                   # quintile cutoff points
        mp_list = random.sample(self.sim.hh_list, 50)                       # members of parliament
        party_size = [0, 0, 0, 0, 0]
        for mp in mp_list:
            for i in range(len(quint)):
                if mp.money <= quint[i].money:
                    party_size[i] += 1
                    break

        # before a gini index has been calculated assume an arbitrary tax rate
        if len(self.sim.stat.hh_stat['metric']['gini']) == 0:
            self.tax_rate = 0.1
        else:
            gini = self.sim.stat.hh_stat['metric']['gini'][-1]
            init_tax_factor = 2.5
            tax_factor_step = 0.5
            self.tax_rate = 0
            # the first quintile party demands the highest tax rate
            # with each quintile the demanded tax rate is decreased
            # the weight of a party is determined by the number of members in its party
            # the final tax rate is calculated by averaging the individual votes
            for p in party_size:
                self.tax_rate += gini * init_tax_factor * p
                init_tax_factor -= tax_factor_step
            self.tax_rate =  self.tax_rate / sum(party_size)

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