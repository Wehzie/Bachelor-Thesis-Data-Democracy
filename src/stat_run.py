

from statistician import Statistician
from simulation import Simulation
import numpy as np
import matplotlib.pyplot as plt

class Stat_run(Statistician):
    '''
    The stat_run object stores and processes data about a single simulation run.
    It inherits methods to visualize this data.
    '''

    ######## ######## ######## METHODS ######## ######## ########

    def calc_dist(self):
        self.f_stat['dist']['money'] = np.append(self.f_stat['dist']['money'], [f.money for f in self.sim.firm_list])
        self.hh_stat['dist']['money'] = np.append(self.hh_stat['dist']['money'], [hh.money for hh in self.sim.hh_list])

    def calc_sum(self):
        hh_list = self.sim.hh_list
        firm_list = self.sim.firm_list

        self.hh_stat['sum']['money'] = np.append(self.hh_stat['sum']['money'], sum([hh.money for hh in hh_list]))
        self.f_stat['sum']['money'] = np.append(self.f_stat['sum']['money'], sum([f.money for f in firm_list]))

    # calculate averages for a set of firm and household characteristics
    def calc_avg(self):
        f_list = self.sim.firm_list
        num_f = self.sim.f_param['num_firms']

        self.f_stat['avg']['money'] = np.append(self.f_stat['avg']['money'], self.f_stat['sum']['money'][-1] / num_f)
        self.f_stat['avg']['num_items'] = np.append(self.f_stat['avg']['num_items'], sum([f.num_items for f in f_list]) / num_f)
        self.f_stat['avg']['item_price'] = np.append(self.f_stat['avg']['item_price'], sum([f.item_price for f in f_list]) / num_f)
        self.f_stat['avg']['marginal_cost'] = np.append(self.f_stat['avg']['marginal_cost'], sum([f.marginal_cost for f in f_list]) / num_f)
        self.f_stat['avg']['demand'] = np.append(self.f_stat['avg']['demand'], sum([f.demand for f in f_list]) / num_f)
        self.f_stat['avg']['num_employees'] = np.append(self.f_stat['avg']['num_employees'], sum([len(f.list_employees) for f in f_list]) / num_f)
        self.f_stat['avg']['wage'] = np.append(self.f_stat['avg']['wage'], sum([f.wage for f in f_list]) / num_f)
        self.f_stat['avg']['months_hiring'] = np.append(self.f_stat['avg']['months_hiring'], sum([self.sim.current_month - f.month_hiring for f in f_list]) / num_f)

        hh_list = self.sim.hh_list
        num_hh = self.sim.hh_param['num_hh']

        self.hh_stat['avg']['money'] = np.append(self.hh_stat['avg']['money'], self.hh_stat['sum']['money'][-1] / num_hh)
        self.hh_stat['avg']['employment'] = np.append(self.hh_stat['avg']['employment'], sum([1 if hh.employer else 0 for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['res_wage'] = np.append(self.hh_stat['avg']['res_wage'], sum([hh.res_wage for hh in hh_list]) / num_hh)
    
    def calc_metric(self):
        self.hh_stat['metric']['hoover'] = np.append(self.hh_stat['metric']['hoover'], self.calc_hoover())
        self.hh_stat['metric']['gini'] = np.append(self.hh_stat['metric']['gini'], self.calc_gini())

    def calc_gov(self):
        self.g_stat['fix']['tax'] = np.append(self.g_stat['fix']['tax'], self.sim.gov.tax_rate)
        self.g_stat['fix']['ubi'] = np.append(self.g_stat['fix']['ubi'], self.sim.gov.ubi)
        if self.gov_type == 'rep':
            self.g_stat['fix']['parties'] = np.append(self.g_stat['fix']['parties'], self.sim.gov.party_size)

    # calculate the hoover index as defined on https://wikimedia.org/api/rest_v1/media/math/render/svg/3e117654142eaec6efa377da812394d213955db4
    # from https://en.wikipedia.org/wiki/Hoover_index
    def calc_hoover(self):
        sum_diff_i_mean = 0
        for hh in self.sim.hh_list:
            sum_diff_i_mean += abs(hh.money - self.hh_stat['avg']['money'][-1])
        return 1/2 * sum_diff_i_mean / self.hh_stat['sum']['money'][-1]

    # based on https://github.com/oliviaguest/gini
    def calc_gini(self):
        array = np.array([hh.money for hh in self.sim.hh_list])
        # All values are treated equally, arrays must be 1d:
        array = array.flatten()
        if np.amin(array) < 0:
            # Values cannot be negative:
            array -= np.amin(array)
        # Values cannot be 0:
        array += 0.0000001
        # Values must be sorted:
        array = np.sort(array)
        # Index per array element:
        index = np.arange(1,array.shape[0]+1)
        # Number of array elements:
        n = array.shape[0]
        # Gini coefficient:
        return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

    # each month notify stat_run of what is going on in the simulation
    def up_stat(self):
        if self.sim.current_month == self.sim.num_months-1:     # in the last month of a run store money distribution
            self.calc_dist()
        self.calc_sum()
        self.calc_avg()
        self.calc_metric()
        if self.gov_type != 'none':
            self.calc_gov()

    ######## ######## ######## SINGLE RUN PLOTS ######## ######## ########
    
    # plot the gini and hover indices of economic equality against time
    def plot_equality(self):
        y1_hoover = self.hh_stat['metric']['hoover']
        y2_gini = self.hh_stat['metric']['gini']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_hoover, 'r', label='Hoover index')
        ax.plot(self.x_months, y2_gini, 'b', label='Gini index')

        ax.set(xlabel='Months', ylabel='Equality', title='Metrics of economic equality')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_' + self.gov_type + '_equality.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_' + self.gov_type + '_equality.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_' + self.gov_type + '_equality.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for firm money and household money against time
    def plot_money(self):
        y1_f_money = self.f_stat['avg']['money']
        y2_hh_money = self.hh_stat['avg']['money']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_money, 'r', label='Money firm average')
        ax.plot(self.x_months, y2_hh_money, 'b', label='Money household average')

        ax.set(xlabel='Months', ylabel='Money', title='Money distribution between firms and households')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_money.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_money.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_money.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for firm wage and household reservation wage against time
    def plot_wage(self):
        y1_f_wage = self.f_stat['avg']['wage']
        y2_hh_res_wage = self.hh_stat['avg']['res_wage']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_wage, 'r', label='Wage firm average')
        ax.plot(self.x_months, y2_hh_res_wage, 'b', label='Reservation wage household average')
        
        ax.set(xlabel='Months', ylabel='Money', title='Wage and reservation wage')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_wage.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_wage.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_wage.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for number of items a firm has in stock and demand 
    def plot_demand(self):
        y1_f_num_items = self.f_stat['avg']['num_items']
        y2_f_demand = self.f_stat['avg']['demand']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_num_items, 'r', label='Number of stocked items firm average')
        ax.plot(self.x_months, y2_f_demand, 'b', label='Demand firm average')

        ax.set(xlabel='Months', ylabel='Items', title='Item demand and price')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_demand.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_demand.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_demand.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot firm's marginal cost and item price
    def plot_item_cost(self):
        y1_f_marginal_cost = self.f_stat['avg']['marginal_cost']
        y2_f_item_price = self.f_stat['avg']['item_price']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_marginal_cost, 'r', label='Marginal cost firm average')
        ax.plot(self.x_months, y2_f_item_price, 'b', label='Item price firm average')

        ax.set(xlabel='Months', ylabel='', title='Item price and marginal cost')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_item_cost.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_item_cost.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_item_cost.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot household employment rate
    def plot_employment(self):
        y1_hh_employment = self.hh_stat['avg']['employment']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_hh_employment, 'b', label='Employment rate')

        ax.set(xlabel='Months', ylabel='', title='Household employment rate')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_employment.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_employment.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_employment.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
    def plot_connections(self):
        y1_f_num_employees = self.f_stat['avg']['num_employees']
        y2_f_months_hiring = self.f_stat['avg']['months_hiring']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_f_num_employees, 'r', label='Number of employees firm average')
        ax.plot(self.x_months, y2_f_months_hiring, 'b', label='Recruiting duration firm average')

        ax.set(xlabel='Months', ylabel='', title='Employer-employee relations')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_connections.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_connections.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_connections.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot the tax rate set by government for each month
    def plot_tax(self):
        y1_tax = self.g_stat['fix']['tax']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_tax, 'r', label='Tax rate')

        ax.set(xlabel='Months', ylabel='Tax rate', title='Taxation')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_tax.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_tax.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_tax.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot the universal basic income set by government for each month
    def plot_ubi(self):
        y1_ubi = self.g_stat['fix']['ubi']

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_ubi, 'r', label='UBI')

        ax.set(xlabel='Months', ylabel='Money', title='Universal Basic Income')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_ubi.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_ubi.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_ubi.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    # plot the party composition of the representative government for each month
    def plot_parties(self):
        parties = deque(self.g_stat['fix']['parties'])
        y1_party, y2_party, y3_party, y4_party, y5_party = ([] for i in range(5))
        for i in range(len(parties)//5):
            y1_party.append(parties.popleft())
            y2_party.append(parties.popleft())
            y3_party.append(parties.popleft())
            y4_party.append(parties.popleft())
            y5_party.append(parties.popleft())

        fig, ax = plt.subplots()
        ax.plot(self.x_months, y1_party, 'r', label='Party quintile 1')     # party representing the poorest quintile of hhs
        ax.plot(self.x_months, y2_party, 'g', label='Party quintile 2')
        ax.plot(self.x_months, y3_party, 'b', label='Party quintile 3')
        ax.plot(self.x_months, y4_party, 'k', label='Party quintile 4')
        ax.plot(self.x_months, y5_party, 'c', label='Party quintile 5')

        ax.set(xlabel='Months', ylabel='Party size', title='Party composition')
        ax.grid()
        ax.legend()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_parties.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_parties.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_parties.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

    def hist_money(self):
        # money distribution at the end of the simulation
        f_money_list = self.f_stat['dist']['money']
        hh_money_list = self.hh_stat['dist']['money']

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.hist(f_money_list, bins=int(self.sim.f_param['num_firms']/10))
        ax2.hist(hh_money_list, bins=int(self.sim.hh_param['num_hh']/10))

        fig.suptitle("Money distribution within households and firms")
        ax1.set(xlabel='Money', ylabel='Number of firms')
        ax1.grid()
        ax2.set(xlabel='Money', ylabel='Number of households')
        ax2.grid()
        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_hist_money.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_hist_money.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_hist_money.png', dpi=300)
        if self.plot_param['show_plots']: plt.show()

######## ######## ######## TODOS ######## ######## ########


    # TODO: Text in figures should be rendered with LaTeX to fit the paper font
    # TODO: Remove plotting in this class and integrate with stat_runs to reduce duplication.
    # TODO: Write results of stat_runs to file. Allow invoking plots without having to rerun the simulation.

    # NEW STATISTICS
    # TODO: Compare average taxed money to average received UBI in a ratio
    # TODO: Are days within a month relevant?
    #       Items are produced and sold each day.
    #       Stock depletion through the course of a month.
    # TODO: How many customers does the firm with most/least customers have?
    # TODO: Indication for movement between quantiles in firms and households.
    #       Average duration within the same quintile for households.
    #       Average number of different visited quantiles for households.  
    # TODO: Average employment duration. Time of households with one firm.
    # TODO: Average duration of relationship between buying household and selling firm.
    # TODO: Average frequency of firings at firms.
    #       Relationship between firings and wealth of firms.
    #       Relationship between quitting for another employer and wealth of households.

    # PLOTTING
    # TODO: Implement different kinds of dotted lines for black and white suitable display
    # TODO: error bars, box plots, violin plots are great
    # TODO: Prettier graphs https://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame
    # TODO: Party composition graph: How to deal with overlapping lines?