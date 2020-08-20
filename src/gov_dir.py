

class Gov_dir(object):
    '''
    This government models a direct democracy where individuals cast direct votes for a tax rate.

    Each month all households are income taxed with a single tax rate.
    Each month all households receive a universal basic income.
    Each month all money that is collected from taxes is spent on ubi.
    '''

    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxes are collected each n months based on income and taxrate
        self.ubi = 0            # ubi paid to each hh monthly

    ######## ######## ######## METHODS ######## ######## ########

    # each household proposes a different tax rate
    # the proposed tax rate is dependent on the hhs position in the distribution of incomes
    # all households have equal weight
    # by averaging individual votes a final tax rate is calculated
    def vote_tax(self):
        taf = self.sim.g_param['tax_adj_freq']           # tax adjustment frequency
        
        # only tax households once enough data is available
        if len(self.sim.stat.hh_stat['metric']['gini_i']) < taf:
            self.tax_rate = 0
            return

        # only vote for a new tax rate when it's the first month of a year
        if self.sim.current_month % taf != 0:
            return

        # mean gini index of the past tax_adj_freq months
        g_list = self.sim.stat.hh_stat['metric']['gini_i'][-taf:]
        m_gini = sum(g_list) / len(g_list)

        # sort households by money
        hh_m_sort = sorted(self.sim.hh_list, key=lambda hh: hh.money)

        # normalize how much money a hh has in relation to the sum of household money
        # transform this to the range of 4 to 0 for poorest and richest households
        maxi_m = hh_m_sort[-1].money                    # money of richest hh
        mini_m = hh_m_sort[0].money                     # money of poorest hh
        mY = self.sim.g_param['tax_gamma']              # maximum gamma value
        gamma_list = [(hh.money - maxi_m) / (mini_m - maxi_m) * mY for hh in hh_m_sort]

        self.tax_rate = 0
        num_hh = self.sim.hh_param['num_hh']            # number of households
        for hh in range(num_hh):
            self.tax_rate += 1 - (1 + m_gini)**-gamma_list[hh]
        self.tax_rate = self.tax_rate / num_hh

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