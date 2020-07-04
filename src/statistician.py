

import numpy as np


class Statistician(object):
    '''
    The statistician class is abstract and not instantiated it inherits the data storage dictionary and plotting capabilities.
    '''

    ######## ######## ######## CONSTRUCTOR ######## ######## ########

    def __init__(self, num_months: int, gov_type: str, num_runs: int):

        self.sim = None                                    # simulation initially empty, use setter to set
        self.gov_type = gov_type
        self.x_months = [m for m in range(num_months)]     # x-axis for most plots is time in months
        self.num_runs = num_runs

        self.f_stat = {

            'dist': {
                'money': np.empty((0, 100)),        # TODO: Read from sim
            },
            
            'sum': {
                'money': np.empty((0, num_months)),
            },

            'avg': {
                'money': np.empty((0, num_months)),
                'num_items': np.empty((0, num_months)),
                'item_price': np.empty((0, num_months)),
                'marginal_cost': np.empty((0, num_months)),
                'demand': np.empty((0, num_months)),
                'num_employees': np.empty((0, num_months)),
                'wage': np.empty((0, num_months)),
                'months_hiring': np.empty((0, num_months)),     # number of months looking for employees
            },
        }

        self.hh_stat = {

            'dist': {
                'money': np.empty((0, 1000)),       # TODO: Read from sim
            },

            'sum': {
                'money': np.empty((0, num_months)),
            },
            
            'avg': {
                'money': np.empty((0, num_months)),
                'employment': np.empty((0, num_months)),        # household employment rate
                'res_wage': np.empty((0, num_months)),
            },

            'metric': {
                'hoover': np.empty((0, num_months)),
                'gini': np.empty((0, num_months)),
            },
        }

        self.g_stat = {

            'fix': {                # direct readings
                'tax': np.empty((0, num_months)),
                'ubi': np.empty((0, num_months)),
                'parties': np.empty((0, num_months*5)),      # representative government's party composition (5 parties) over time
            }
        }

    # set the simulation object
    def set_sim(self, sim: object):
        self.sim = sim

    # invoke the appropriate plots given the configuration of the simulation
    def invoke_plots(self):
        self.plot_equality()
        self.plot_money()
        self.plot_wage()
        self.plot_demand()
        self.plot_items()
        self.plot_connections()
        if self.gov_type != 'none':
            self.plot_tax()
            self.plot_ubi()
            if self.gov_type == 'rep':
                self.plot_parties()
        self.hist_money()

    # plot the gini and hover indices of economic equality against time
    def plot_equality(self):
        pass

    # plot averages for firm money and household money against time
    def plot_money (self):
        pass

    # plot averages for firm wage and household reservation wage against time
    def plot_wage (self):
        pass

    # plot averages for number of items a firm has in stock and demand 
    def plot_demand (self):
        pass

    # plot firm's marginal cost and item price as well as household employment rate
    def plot_items (self):
        pass

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
    def plot_connections (self):
        pass

    # plot the tax rate set by government for each month
    def plot_tax(self):
        pass
    # plot the universal basic income set by government for each month
    def plot_ubi(self):
        pass

    # plot the party composition of the representative government for each month
    def plot_parties(self):
        pass

    # money distribution at the end of the simulation
    def hist_money(self):
        pass