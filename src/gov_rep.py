

class Gov_rep(object):
    '''
    This government models a representative democracy with a party system.

    Each month all households are income taxed with a single tax rate.
    Each month all households receives a universal basic income.
    All money that is collected from taxes is spent on ubi.

    The tax rate changes each year.
    The ubi changes each year.
    The government changes after each term.
    '''

    def __init__(self, sim: object):
        self.sim = sim                          # link government to the simulation
        self.money = 0                          # money available to government for redistribution
        self.tax_rate = 0                       # taxes are collected each n months based on income and taxrate
        self.ubi = 0                            # ubi paid to each hh monthly
        self.party_size = [0, 0, 0, 0, 0]       # number of members in each quintile party

    ######## ######## ######## METHODS ######## ######## ########

    # each term a new government is elected in the form of a parliamentary composition
    def assemble_parliament(self):
        hh_m_sort = sorted(self.sim.hh_list, key=lambda hh: hh.money)   # sort households by money
        num_p = self.sim.g_param['rep_num_parties']
        
        # integrate over households money
        integral = [0]
        for hh in hh_m_sort:
            integral.append(hh.money + integral[-1])

        norm = [i / integral[-1] for i in integral]     # normalize integral
        x = list(range(0, len(norm)))                   # list with number of points in integral
        x = [i /(len(x)-1) for i in x]                  # normalize list

        # Given (x, norm) income_dist(0.2) returns the % of money owned by the poorest 20% of households
        # Given (norm, x) income_dist(0.2) returns the % of households owned by the leftmost 20% of money
        income_dist = interp1d(norm, x, kind='linear')  # interpolate income distribution for integrated incomes
        
        self.party_size = []
        step = 1 / num_p
        for i in range(1, num_p+1):
            self.party_size.append(round(float(income_dist(step * i) - income_dist(step * (i-1))), 2))

    # households are randomly sampled from the population of hhs
    # based on income a hh belongs to a party
    # each party votes for a different tax rate
    # the poorest party votes for highest taxes
    def vote_tax(self):
        taf = self.sim.g_param['tax_adj_freq']           # tax adjustment frequency

        # only tax households once enough data is available
        if len(self.sim.stat.hh_stat['metric']['gini_i']) < taf:
            self.tax_rate = 0
            return

        # only vote for a new tax rate when it's the first month of a year
        if self.sim.current_month % taf != 0:
            return

        # first government established after one year has passed
        # only elect a new government once a term has passed
        if (self.sim.current_month - taf) % self.sim.g_param['rep_term_length'] == 0:
            self.assemble_parliament()

        # mean gini index of the past tax_adj_freq months
        g_list = self.sim.stat.hh_stat['metric']['gini_i'][-taf:]
        m_gini = sum(g_list) / len(g_list)

        # the first quintile party demands the highest tax rate
        # with each quintile the demanded tax rate is decreased
        # the weight of a party is determined by the number of members in its party
        # the final tax rate is calculated by averaging the individual votes
        init_tax_factor = 2.5                                               # initial tax chosen by the lowest quintile party
        tax_factor_step = init_tax_factor / len(self.party_size)            # reduction step from initial tax per party
        self.tax_rate = 0
        for p in self.party_size:
            self.tax_rate += m_gini * init_tax_factor * p
            init_tax_factor -= tax_factor_step
        # self.tax_rate = self.tax_rate / sum(self.party_size)

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
from scipy.interpolate import interp1d