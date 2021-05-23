async function statistician() {
return (
`









plt.rcParams['axes.grid'] = True
plt.rcParams["errorbar.capsize"] = 3

class Statistician(object):
    '''
    The Statistician class is abstract and not instantiated it inherits the data storage dictionary and plotting capabilities.
    '''

    ######## ######## ######## CONSTRUCTOR ######## ######## ########


    def __init__(self, num_months: int, num_runs: int, gov_type: str, num_f: int, num_hh: int, plot_param: dict):

        self.sim = None                                     # simulation initially empty, use setter to set
        self.gov_type = gov_type                            # type of government
        self.x_months = [m for m in range(num_months)]      # x-axis for most plots is time in months
        self.num_runs = num_runs                            # number of runs simulated
        self.plot_param = plot_param                        # plotting parameters

        # firm statistics
        self.f_stat = {

            'dist': {
                'money': np.empty((0, num_f)),
                'wage': np.empty((0, num_f)),
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

        # household statistics
        self.hh_stat = {

            'dist': {
                'money': np.empty((0, num_hh)),
                'income': np.empty((0, num_hh)),
            },

            'sum': {
                'money': np.empty((0, num_months)),
            },
            
            'avg': {
                'money': np.empty((0, num_months)),
                'employment': np.empty((0, num_months)),        # household employment rate
                'res_wage': np.empty((0, num_months)),
                'income': np.empty((0, num_months)),
            },

            'metric': {
                'gini_i': np.empty((0, num_months)),            # gini on income
                'gini_m': np.empty((0, num_months)),            # gini on money
            },
        }

        # government statistics
        self.g_stat = {

            'fix': {                # direct readings
                'tax': np.empty((0, num_months)),
                'ubi': np.empty((0, num_months)),
                'parties': np.empty((0, num_months*5)),      # representative government's party composition (5 parties) over time
            }
        }

######## ######## ######## METHODS ######## ######## ########

    # set the simulation object
    def set_sim(self, sim: object):
        self.sim = sim

    # invoke the appropriate plots given the configuration of the simulation
    def invoke_plots(self):
        self.plot_equality()
        self.plot_money()
        self.plot_wage()
        self.plot_demand()
        self.plot_item_cost()
        self.plot_employment()
        self.plot_connections()
        if self.gov_type != 'none':
            self.plot_tax()
            self.plot_ubi()
            if self.gov_type == 'rep':
                self.plot_parties()
        self.hist_income()
        self.hist_money()
        self.dist_income()
        if self.plot_param['save_csv']:
            print_hashes = "######## ######## ########"
            js.document.getElementById('text_output').value += '\\n' + str(f"\\n{print_hashes:<30} {'SAVING DATA':>15}")
            self.save()

    # save data to file
    def save(self):
        with open('dat/data '+str(datetime.datetime.now().strftime("%H:%M:%S"))+'.csv','a') as f:
            for stat_key, stat_val in self.f_stat.items():
                for measure_key, measure_val in stat_val.items():
                    np.savetxt(f, self.f_stat[stat_key][measure_key], delimiter=',', header='firm '+str(stat_key)+' '+str(measure_key))

            for stat_key, stat_val in self.hh_stat.items():
                for measure_key, measure_val in stat_val.items():
                    np.savetxt(f, self.hh_stat[stat_key][measure_key], delimiter=',', header='hh '+str(stat_key)+' '+str(measure_key))
                    
            if self.gov_type != 'none':
                for stat_key, stat_val in self.g_stat.items():
                    for measure_key, measure_val in stat_val.items():
                        if len(measure_val) == 0: continue                  # only add party data for the representative government
                        np.savetxt(f, self.g_stat[stat_key][measure_key], delimiter=',', header='gov '+str(stat_key)+' '+str(measure_key))

######## ######## ######## PLOTS ######## ######## ########

    # evaluate the plot parameters for saving
    def save_fig(self, fig, plot_name):
        if self.plot_param['save_pgf']: fig.savefig('img/fig_' + self.gov_type + '_' + plot_name +'.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_' + self.gov_type + '_' + plot_name + '.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_' + self.gov_type + '_' + plot_name + '.png', dpi=300)
    
    # plot the gini index based on income and money distribution
    def plot_equality(self):
        if self.sim.num_runs > 1:
            y1_gini_m = np.mean(self.hh_stat['metric']['gini_m'], axis=0)
            y2_gini_i = np.mean(self.hh_stat['metric']['gini_i'], axis=0)
            e1 = stats.sem(self.hh_stat['metric']['gini_m'])
            e2 = stats.sem(self.hh_stat['metric']['gini_i'])
        else:
            y1_gini_m = self.hh_stat['metric']['gini_m']
            y2_gini_i = self.hh_stat['metric']['gini_i']
            e1, e2 = 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_gini_m, e1, elinewidth=0.5, capthick=0.5, linestyle="-.", color='r', label='Gini coefficient of money')
        plt.errorbar(self.x_months, y2_gini_i, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label='Gini coefficient of income')
        ax.set(xlabel='Months', ylabel='Equality')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Metrics of economic equality')
        self.save_fig(fig, 'equality')

    # plot averages for firm money and household money against time
    def plot_money(self):
        if self.sim.num_runs > 1:
            y1_f_money = np.mean(self.f_stat['avg']['money'], axis=0)
            y2_hh_money = np.mean(self.hh_stat['avg']['money'], axis=0)
            e1 = stats.sem(self.f_stat['avg']['money'])
            e2 = stats.sem(self.hh_stat['avg']['money'])
        else:
            y1_f_money = self.f_stat['avg']['money']
            y2_hh_money = self.hh_stat['avg']['money']
            e1 = 0
            e2 = 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_money, e1, elinewidth=0.5, capthick=0.5, linestyle="-.", color='r', label="Firms' money")
        plt.errorbar(self.x_months, y2_hh_money, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label="Households' money")
        ax.set(xlabel='Months', ylabel='Money')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Money for firms and households')
        self.save_fig(fig, 'money')

    # plot averages for firm wage, household income and household reservation wage against time
    def plot_wage(self):
        if self.sim.num_runs > 1:
            y1_f_wage = np.mean(self.f_stat['avg']['wage'], axis=0)
            y2_hh_res_wage = np.mean(self.hh_stat['avg']['res_wage'], axis=0)
            y3_hh_income = np.mean(self.hh_stat['avg']['income'], axis=0)
            e1 = stats.sem(self.f_stat['avg']['wage'])
            e2 = stats.sem(self.hh_stat['avg']['res_wage'])
            e3 = stats.sem(self.hh_stat['avg']['income'])
        else:
            y1_f_wage = self.f_stat['avg']['wage']
            y2_hh_res_wage = self.hh_stat['avg']['res_wage']
            y3_hh_income = self.hh_stat['avg']['income']
            e1, e2, e3 = 0, 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_wage, e1, elinewidth=0.5, capthick=0.5, linestyle=":", color='r', label="Firms' wage")
        plt.errorbar(self.x_months, y2_hh_res_wage, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label="Households' reservation wage")
        plt.errorbar(self.x_months, y3_hh_income, e3, elinewidth=0.5, capthick=0.5, linestyle="-.", color='g', label="Households' income")
        ax.set(xlabel='Months', ylabel='Money')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Wage, income and reservation wage')
        self.save_fig(fig, 'wage')   

    # plot averages for number of items a firm has in stock and demand 
    def plot_demand(self):
        if self.sim.num_runs > 1:
            y1_f_num_items = np.mean(self.f_stat['avg']['num_items'], axis=0)
            y2_f_demand = np.mean(self.f_stat['avg']['demand'], axis=0)
            e1 = stats.sem(self.f_stat['avg']['num_items'])
            e2 = stats.sem(self.f_stat['avg']['demand'])
        else:
            y1_f_num_items = self.f_stat['avg']['num_items']
            y2_f_demand = self.f_stat['avg']['demand']
            e1, e2 = 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_num_items, e1, elinewidth=0.5, capthick=0.5, linestyle="-.", color='r', label="Firms' stock size")
        plt.errorbar(self.x_months, y2_f_demand, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label="Firms' demand")
        ax.set(xlabel='Months', ylabel='Items')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Item demand and price')
        self.save_fig(fig, 'demand')

    # plot firm's marginal cost and item price
    def plot_item_cost(self):
        if self.sim.num_runs > 1:
            y1_f_marginal_cost = np.mean(self.f_stat['avg']['marginal_cost'], axis=0)
            y2_f_item_price = np.mean(self.f_stat['avg']['item_price'], axis=0)
            e1 = stats.sem(self.f_stat['avg']['marginal_cost'])
            e2 = stats.sem(self.f_stat['avg']['item_price'])
        else:
            y1_f_marginal_cost = self.f_stat['avg']['marginal_cost']
            y2_f_item_price = self.f_stat['avg']['item_price']
            e1, e2 = 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_marginal_cost, e1, elinewidth=0.5, capthick=0.5, linestyle="-.", color='r', label="Firms' marginal cost")
        plt.errorbar(self.x_months, y2_f_item_price, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label="Firms' item price")
        ax.set(xlabel='Months', ylabel='Money')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Item price and marginal cost')
        self.save_fig(fig, 'item_cost')

    # plot household employment rate
    def plot_employment(self):
        if self.sim.num_runs > 1:
            y1_hh_employment = np.mean(self.hh_stat['avg']['employment'], axis=0)
            e1 = stats.sem(self.hh_stat['avg']['employment'])
        else:
            y1_hh_employment = self.hh_stat['avg']['employment']
            e1, e2 = 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_hh_employment, e1, elinewidth=0.5, capthick=0.5, linestyle="-", color='b', label='Employment rate')
        ax.set(xlabel='Months', ylabel='Employment rate')

        if self.plot_param['title']: ax.set(title="Households' employment rate")
        self.save_fig(fig, 'employment')

    # plot averages for
        # firms' number of employees
        # the duration for which firms have been looking to hire
    def plot_connections(self):
        if self.sim.num_runs > 1:
            y1_f_num_employees = np.mean(self.f_stat['avg']['num_employees'], axis=0)
            y2_f_months_hiring = np.mean(self.f_stat['avg']['months_hiring'], axis=0)
            e1 = stats.sem(self.f_stat['avg']['num_employees'])
            e2 = stats.sem(self.f_stat['avg']['months_hiring'])
        else:
            y1_f_num_employees = self.f_stat['avg']['num_employees']
            y2_f_months_hiring = self.f_stat['avg']['months_hiring']
            e1, e2 = 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_f_num_employees, e1, elinewidth=0.5, capthick=0.5, linestyle="-.", color='r', label="Firms' number of employees")
        plt.errorbar(self.x_months, y2_f_months_hiring, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label="Firms' recruiting duration")
        ax.set(xlabel='Months', ylabel='')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Employment relations')
        self.save_fig(fig, 'connections')
        
    # plot the tax rate set by government for each month
    def plot_tax(self):
        if self.sim.num_runs > 1:
            y1_tax = np.mean(self.g_stat['fix']['tax'], axis=0)
            e1 = stats.sem(self.g_stat['fix']['tax'])
        else:
            y1_tax = self.g_stat['fix']['tax']
            e1 = 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_tax, e1, elinewidth=0.5, capthick=0.5, linestyle="-", color='b', label='Tax rate')
        ax.set(xlabel='Months', ylabel='Tax rate')

        if self.plot_param['title']: ax.set(title='Flat tax rate')
        self.save_fig(fig, 'tax')
        
    # plot the universal basic income set by government for each month
    def plot_ubi(self):
        if self.sim.num_runs > 1:
            y1_ubi = np.mean(self.g_stat['fix']['ubi'], axis=0)
            e1 = stats.sem(self.g_stat['fix']['ubi'])
        else:
            y1_ubi = self.g_stat['fix']['ubi']
            e1 = 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_ubi, e1, elinewidth=0.5, capthick=0.5, linestyle="-", color='b', label='UBI')
        ax.set(xlabel='Months', ylabel='Money')

        if self.plot_param['title']: ax.set(title='Universal Basic Income')
        self.save_fig(fig, 'ubi')

    # plot the party composition of the representative government for each month
    def plot_parties(self):
        if self.sim.num_months > 1:
            parties = self.g_stat['fix']['parties']
            y1_party, y2_party, y3_party, y4_party, y5_party = (np.empty((0, self.sim.num_months)) for i in range(5))

            for row in range(np.size(parties, 0)):
                col = 0
                y1_col, y2_col, y3_col, y4_col, y5_col = (np.empty(0) for i in range(5))
                while col < np.size(parties, 1):
                    y1_col, y2_col, y3_col, y4_col, y5_col = np.append(y1_col, parties[row][col]), np.append(y2_col, parties[row][col+1]), np.append(y3_col, parties[row][col+2]), np.append(y4_col, parties[row][col+3]), np.append(y5_col, parties[row][col+4])
                    col += 5
                y1_party, y2_party, y3_party, y4_party, y5_party = np.vstack((y1_party, y1_col)), np.vstack((y2_party, y2_col)), np.vstack((y3_party, y3_col)), np.vstack((y4_party, y4_col)), np.vstack((y5_party, y5_col))

            e1, e2, e3, e4, e5 = stats.sem(y1_party), stats.sem(y2_party), stats.sem(y3_party), stats.sem(y4_party), stats.sem(y5_party)
            y1_party, y2_party, y3_party, y4_party, y5_party = np.mean(y1_party, axis=0), np.mean(y2_party, axis=0), np.mean(y3_party, axis=0), np.mean(y4_party, axis=0), np.mean(y5_party, axis=0)
        else:
            parties = deque(self.g_stat['fix']['parties'])
            y1_party, y2_party, y3_party, y4_party, y5_party = ([] for i in range(5))
            for i in range(len(parties)//5):
                y1_party.append(parties.popleft())
                y2_party.append(parties.popleft())
                y3_party.append(parties.popleft())
                y4_party.append(parties.popleft())
                y5_party.append(parties.popleft())
            e1, e2, e3, e4, e5 = 0, 0, 0, 0, 0

        fig, ax = plt.subplots()
        plt.errorbar(self.x_months, y1_party, e1, elinewidth=0.5, capthick=0.5, linestyle=":", color='r', label='Party quintile 1')     # party representing the poorest quintile of hhs
        plt.errorbar(self.x_months, y2_party, e2, elinewidth=0.5, capthick=0.5, linestyle="--", color='b', label='Party quintile 2')
        plt.errorbar(self.x_months, y3_party, e3, elinewidth=0.5, capthick=0.5, linestyle="-.", color='g', label='Party quintile 3')
        plt.errorbar(self.x_months, y4_party, e4, elinewidth=0.5, capthick=0.5, dashes=[1, 3, 5, 7], color='k', label='Party quintile 4')
        plt.errorbar(self.x_months, y5_party, e5, elinewidth=0.5, capthick=0.5, dashes=[5, 15, 5, 20], color='c', label='Party quintile 5')
        ax.set(xlabel='Months', ylabel='Party size')
        ax.legend()

        if self.plot_param['title']: ax.set(title='Representative parliament composition')
        self.save_fig(fig, 'parties')
        
    # money distribution at the end of the simulation
    def hist_money(self):
        if self.sim.num_runs > 1:
            f_money_list = (self.f_stat['dist']['money']).flatten()
            hh_money_list = (self.hh_stat['dist']['money']).flatten()
        else:
            f_money_list = self.f_stat['dist']['money']
            hh_money_list = self.hh_stat['dist']['money']

        fig, (ax1, ax2) = plt.subplots(1, 2)
        
        ax1.hist(f_money_list, bins=int(self.sim.f_param['num_firms']/10))
        ax2.hist(hh_money_list, bins=int(self.sim.hh_param['num_hh']/10))

        ax1.set(xlabel='Money', ylabel='Number of firms')
        ax2.set(xlabel='Money', ylabel='Number of households')

        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()

        if self.plot_param['title']: fig.suptitle("Money distribution in firms and households")
        self.save_fig(fig, 'hist_money')

    # income distribution at the end of the simulation
    def hist_income(self):
        if self.sim.num_runs > 1:
            f_wage_list = (self.f_stat['dist']['wage']).flatten()
            hh_income_list = (self.hh_stat['dist']['income']).flatten()
        else:
            f_wage_list = self.f_stat['dist']['wage']
            hh_income_list = self.hh_stat['dist']['income']

        fig, (ax1, ax2) = plt.subplots(1, 2)
    
        ax1.hist(f_wage_list, bins=int(self.sim.f_param['num_firms']/10))
        ax2.hist(hh_income_list, bins=int(self.sim.hh_param['num_hh']/10))
        
        ax1.set(xlabel='Wage', ylabel='Number of firms')
        ax2.set(xlabel='Income', ylabel='Number of households')

        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()

        if self.plot_param['title']: fig.suptitle("Wage and income distribution in firms and households")
        self.save_fig(fig, 'hist_income')
    
    # Plot Lorenz income curve (only tested for single run)
    def dist_income(self):
        if self.sim.num_runs > 1: return

        # income distribution at the end of the simulation as line graph
        hh_dist_income = self.hh_stat['dist']['income']
        hh_dist_income.sort()

        hh_income_integral = [0]
        for hh in hh_dist_income:
            hh_income_integral.append(hh + hh_income_integral[-1])
        hh_income_norm = [hh / hh_income_integral[-1] for hh in hh_income_integral]

        hh_income_x = list(range(0, len(hh_income_norm)))       # x has num_hh entries
        hh_income_x = [point / (len(hh_income_x)-1) for point in hh_income_x]
        # 0.2 on x-axis shows the percentage of the sum of incomes on the y-axis

        f_dist_wage = self.f_stat['dist']['wage']
        f_dist_wage.sort()

        f_wage_integral = [0]
        for f in f_dist_wage:
            f_wage_integral.append(f + f_wage_integral[-1])

        f_wage_norm = [f / f_wage_integral[-1] for f in f_wage_integral]
        f_wage_x = list(range(0, len(f_wage_norm)))       # x has num_f entries
        f_wage_x = [point / (len(f_wage_x)-1) for point in f_wage_x]

        fig, (ax1, ax2) = plt.subplots(1, 2)

        ax1.plot(f_wage_x, f_wage_norm, 'r', label='Firms per wage')
        ax1.set(xlabel='Firms', ylabel='Wage')

        ax2.plot(hh_income_x, hh_income_norm, 'b', label='Households per income')
        ax2.set(xlabel='Households', ylabel='Income')
        ax2.yaxis.set_label_position("right")
        ax2.yaxis.tick_right()

        if self.plot_param['save_pgf']: fig.savefig('img/fig_'+ self.gov_type +'_dist_income.pgf')
        if self.plot_param['save_pdf']: fig.savefig('img/fig_'+ self.gov_type +'_dist_income.pdf')
        if self.plot_param['save_png']: fig.savefig('img/fig_'+ self.gov_type +'_dist_income.png', dpi=300)

        if self.plot_param['title']: fig.suptitle("Income and wage distribution within households and firms")
        self.save_fig(fig, 'dist_income')

######## ######## ######## TODO ######## ######## ########

    # PROPOSAL FOR ADDITIONAL STATISTICS
    # How many customers does the firm with most/least customers have?
    # Indication for movement between quantiles in firms and households.
    # Average duration within the same income/money quintile for households.
    # Average time a households stays with the same firm.
    # Average duration a households buys from the same firm.
    # Average frequency of firings at firms.

`)
}
