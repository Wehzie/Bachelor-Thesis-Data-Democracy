

class Gov_rep(object):
    '''
    This government models a representative democracy with a party system.

    Each month all households are income taxed with a single tax rate.
    Each month all households receive a universal basic income.
    Each month all money that is collected from taxes is spent on ubi.
    Each term the government's parliamentary composition changes.
    '''

    def __init__(self, sim: object):
        self.sim = sim                          # link government to the simulation
        self.money = 0                          # money available to government for redistribution
        self.tax_rate = 0                       # taxes are collected each month based on income and taxrate
        self.ubi = 0                            # ubi paid to each hh monthly
        self.parties = [0] * self.sim.g_param['rep_num_parties']    # holds parliamentary composition in percentages per party
                                                # the left most party in the list represents the poorest households

    ######## ######## ######## METHODS ######## ######## ########

    # each term a new government is elected in the form of a parliamentary composition
    def assemble_parliament(self):
        hh_i_sort = sorted(self.sim.hh_list, key=lambda hh: hh.income)   # sort households by income
        num_p = self.sim.g_param['rep_num_parties']
        
        # integrate over households income
        integral = [0]
        for hh in hh_i_sort:
            integral.append(hh.income + integral[-1])

        norm = [i / integral[-1] for i in integral]     # normalize integral
        x = list(range(0, len(norm)))                   # list with number of points in integral
        x = [i /(len(x)-1) for i in x]                  # normalize list

        # Given (x, norm) income_dist(0.2) returns the % of income is received by the poorest 20% of households
        # Given (norm, x) income_dist(0.2) returns the % of households receiving the leftmost 20% of income
        income_dist = interp1d(norm, x, kind='linear')  # interpolate income distribution for integrated incomes
        
        self.parties = []
        step = 1 / num_p
        for i in range(1, num_p+1):
            self.parties.append(round(float(income_dist(step * i) - income_dist(step * (i-1))), 2))

    # households vote for a party based on income
    # party size follows income distribution
    # for example, when the left most 20% of income is received by the poorest 60% of households their party has 60% weight
    # poor party votes for highest taxes, the rich party for the lowest taxes
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

        # calculate tax
        self.tax_rate = 0
        gamma = self.sim.g_param['tax_gamma']                           # maximum gamma value
        gamma_step = gamma / (self.sim.g_param['rep_num_parties']-1)    # stepwise decrease of gamma per party
        for p in self.parties:
            self.tax_rate += (1 - (1 + m_gini)**-gamma) * p
            gamma -= gamma_step

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