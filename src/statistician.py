

class Statistician(object):

    def __init__(self, sim: object):
        self.sim = sim
        self.money = {'f': [], 'hh': [], 'f_reserve': []}
        self.price = []
        self.wage = []
        self.employment = []

        # TODO: For now averages are stored, consider splitting up for further statistics, e.G. median, spreads etc.
        self.f_stat = {
            'avg': {
                'money': [],
                'reserve': [],
                'num_items': [],
                'item_price': [],
                'marginal_cost': [],
                'demand': [],
                'num_employees': [],
                'wage': [],
                'months_hiring': [],    # number of months looking for employees
            },
        }

        self.hh_stat = {
            'avg': {
                'money': [],
                'employment': [],   # number employed households, normalized
                'num_vendors': [],
                'res_wage': [],
            },
        }

    # TODO: Create 4 plots showing this
    # Money: f_money, f_reserve, hh_money
    # Wage: f_wage, f_marginal_cost, hh_res_wage
    # Items: f_num_items, f_item_price, f_demand
    # Employment: f_num_employees, f_months_hiring, hh_employment, hh_num_vendors

    ######## ######## ######## METHODS ######## ######## ########

    def calc_avg(self):
        f_list = self.sim.firm_list
        num_f = self.sim.f_param['num_firms']

        self.f_stat['avg']['money'].append(sum([f.money for f in f_list]) / num_f)
        self.f_stat['avg']['reserve'].append(sum([f.reserve for f in f_list]) / num_f)
        self.f_stat['avg']['num_items'].append(sum([f.num_items for f in f_list]) / num_f)
        self.f_stat['avg']['item_price'].append(sum([f.item_price for f in f_list]) / num_f)
        self.f_stat['avg']['marginal_cost'].append(sum([f.marginal_cost for f in f_list]) / num_f)
        self.f_stat['avg']['demand'].append(sum([f.demand for f in f_list]) / num_f)
        self.f_stat['avg']['num_employees'].append(sum([len(f.list_employees) for f in f_list]) / num_f)
        self.f_stat['avg']['wage'].append(sum([f.wage for f in f_list]) / num_f)
        self.f_stat['avg']['months_hiring'].append(sum([self.sim.current_month - f.month_hiring for f in f_list]) / num_f)

        hh_list = self.sim.hh_list
        num_hh = self.sim.hh_param['num_hh']

        self.hh_stat['avg']['money'].append(sum([hh.money for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['employment'].append(sum([1 if hh.employer else 0 for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['num_vendors'].append(sum([len(hh.vendor_list) for hh in hh_list]) / num_hh)
        self.hh_stat['avg']['res_wage'].append(sum([hh.res_wage for hh in hh_list]) / num_hh)
    
    # each month notify the statistician of what is going on in the simulation
    def up_stat(self):
        self.calc_avg()

    # TODO: think about days within a month
    # plot hh and firm money against time
    def plot_money_reserve(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_f_money = self.f_stat['avg']['money']
        y2_hh_money = self.hh_stat['avg']['money']
        y3_f_reserve = self.f_stat['avg']['reserve']

        fig, ax = plt.subplots()
        # BUG: Firm money and firm reserve curves are identical
        ax.plot(x_months, y1_f_money, 'r', label='Firms')
        ax.plot(x_months, y2_hh_money, 'b', label='Households')
        ax.plot(x_months, y3_f_reserve, 'g', label='Firm Reserve')

        ax.set(xlabel='Months', ylabel='Money',
            title='Household and Firm Money')
        ax.grid()
        ax.legend()

        fig.savefig('money.png')
        plt.show()
    
    # TODO: price and wage
    # in reference to https://sim4edu.com/sims/20/index.html?lang=de
    def plot_price_wage_employment(self):
        x_months = [m for m in range(self.sim.num_months)]
        y1_num_employees = self.f_stat['avg']['num_employees']
        y2_employment = self.hh_stat['avg']['employment']
        y3_price = self.f_stat['avg']['item_price']
        y4_wage = self.f_stat['avg']['wage']
        y5_months_hiring = self.f_stat['avg']['months_hiring']

        fig, ax = plt.subplots()
        ax.plot(x_months, y1_num_employees, 'r', label='Average number of firm employees')
        ax.plot(x_months, y2_employment, 'g', label='Household employment rate')            # BUG: 100% (1.00)
        ax.plot(x_months, y3_price, 'b', label='Item price')
        ax.plot(x_months, y4_wage, 'k', label='Wage')
        ax.plot(x_months, y5_months_hiring, 'm', label='Months Hiring')

        ax.set(xlabel='Months', ylabel='Price, wage, employment',
            title='Price, wage, employment')
        ax.grid()
        ax.legend()

        fig.savefig('price_wage_employment.png')
        plt.show()

    def invoke_plots(self):
        self.plot_money_reserve()
        self.plot_price_wage_employment()

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import matplotlib
import matplotlib.pyplot as plt
import numpy as np