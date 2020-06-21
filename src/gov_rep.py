

# this government models a representative democracy with a party system

# each month all households are income taxed with a single tax rate
# each month all households receives a universal basic income
# all money that is collected from taxes is spent on ubi

# the tax rate changes each year
# the ubi changes each year
# the government changes after each term

class Gov_rep(object):
    
    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, sim: object):
        self.sim = sim                          # link government to the simulation
        self.money = 0                          # money available to government for redistribution
        self.tax_rate = 0                       # taxes are collected each n months based on income and taxrate
        self.ubi = 0                            # ubi paid to each hh monthly
        self.party_size = [0, 0, 0, 0, 0]       # number of members in each quintile party

    ######## ######## ######## METHODS ######## ######## ########

    # each term a new government is elected in the form of a parliamentary composition
    def assemble_parliament(self):
        hh_money_sorted = sorted(self.sim.hh_list, key=lambda hh: hh.money) # sort households by money
        quint = hh_money_sorted[199::200]                                   # quintile cutoff points
        mp_list = random.sample(self.sim.hh_list, 50)                       # members of parliament
        self.party_size = [0, 0, 0, 0, 0]                                   # reset parliament
        for mp in mp_list:
            for i in range(len(quint)):
                if mp.money <= quint[i].money:
                    self.party_size[i] += 1
                    break

    # households are randomly sampled from the population of hhs
    # based on income a hh belongs to a party
    # each party votes for a different tax rate
    # the poorest party votes for highest taxes
    def vote_tax(self):
        # only tax households once enough data is available
        if len(self.sim.stat.hh_stat['metric']['gini']) < 12:
            self.tax_rate = 0
            return

        # only vote for a new tax rate when it's the first month of a year
        if self.sim.current_month % self.sim.months_in_year != 0:
            return

        # first government established after one year has passed
        # only elect a new government once a term has passed
        if (self.sim.current_month - self.sim.months_in_year) % self.sim.g_param['rep_term_length'] == 0:
            self.assemble_parliament()

        year_gini_list = self.sim.stat.hh_stat['metric']['gini'][-12:]
        gini = sum(year_gini_list) / len(year_gini_list)                    # mean gini index of the last year
        
        # the first quintile party demands the highest tax rate
        # with each quintile the demanded tax rate is decreased
        # the weight of a party is determined by the number of members in its party
        # the final tax rate is calculated by averaging the individual votes
        init_tax_factor = 2.5                                               # initial tax chosen by the lowest quintile party
        tax_factor_step = init_tax_factor / len(self.party_size)            # reduction step from initial tax per party
        self.tax_rate = 0
        for p in self.party_size:
            self.tax_rate += gini * init_tax_factor * p
            init_tax_factor -= tax_factor_step
        self.tax_rate = self.tax_rate / sum(self.party_size)

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