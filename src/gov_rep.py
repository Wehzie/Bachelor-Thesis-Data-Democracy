
# sample randomly from households
# firms are not in government since firms are composed of households, this more closely reflects political reality

# divide households into quintiles by money
# analyze movement between quintiles over time

# representative government
# on inception a 4 year plan is made that is not deviated from
# this plan is an agreement on how to tax in the 4 coming years
# members of parliament MOP belong to 1 of 5 parties (set by wealth quintiles)
# depending on the wealth of each group, a target UBI is calculated
# a voting and negotiation process is replaced by a calculation factoring each groups target UBI
# the weight of a group's vote is determined by the number of its members
# Via the negotiated UBI a target tax value is calculated


class Gov_rep(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly
        self.parliament = {}

    def vote_tax(self):
        # Germany has 83 million citizens
        # While varying in practise, by law Deutscher Bundestag has 598 representatives
        # Germany by population lies somwhere in the middle of representative democracies (Finland has 5 mil and India has 1.35 bil)
        # 83000000/598 = 138796. 1 MP represents more than 100000 people.
        # In Finland: 5000000/200 = 25000
        # With just 1000 households a similar relationship cannot be achieved
        # I choose parliament size 50 since there are 5 quintiles of people and there is a fair chance for each quintile to be represented


        #list of hh sorted by money
        #divide into quinitles of 0-199, 200-399 ... -999
        #look at money of hh 200, 400, 600, 800 those are the cutoff points
        #in mp_list count the number of people within each bin
        #rep_gov_comp = [num_members_q1, nm_q2, ...] 

        mp_list = random.sample(self.sim.hh_list, 50)



        self.parliament = {}

        # Fini
        if len(self.sim.stat.hh_stat['metric']['gini']) == 0:
            self.tax_rate = 0.1
        else:
            self.tax_rate = self.sim.stat.hh_stat['metric']['gini'][-1] * 0.1

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

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import random