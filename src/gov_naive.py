


# tax policy (monthly)
#   1. transaction tax for each purchase
#   2. possession tax at the end or beginning of month or each n months
#   3. profit tax (rich households get more dividends)
#   4. wage based tax?
#   5. regardless of source, keep field which keeps track of incoming money. tax based only on this value
#   Grossi: agrees with single income tax and single tax tier

# Arndts: check out Milton Friedman, similar proposals

# government does not keep state or make profit, money that is collected is immediately spent
# single tax value for all instead of tiered tax
# possession vs income taxes, see literature

# goals of tax policy
#   https://www.equalitytrust.org.uk/how-economic-inequality-defined
#   https://data.oecd.org/inequality/income-inequality.htm#indicator-chart
#   https://www.bundesfinanzministerium.de/Content/EN/Standardartikel/Topics/International_affairs/Articles/2019-06-07-social-inequalitiy-and-inclusive-growth.html
#   https://now.allthatstats.com/articles/income-quintile-share-ratio-54
#   1. minimize Gini Coefficient
#   2. minimize income quintile share ratio (S80/S20 ratio)
#   3. minimize Palma Ratio
#   4. minimize poverty, defined as having a household income less than 60% of median income.
#   Grossi: Pick one.

# explain why equality is good and with what other desireable parameters it correlates

# money redistribution by basic universal income (also taxed) each month
# parties have different ideas on how high ubi should be
# based on this they have target taxes



# third type of government where people aren't asked and taxes are take to eliminate poverty
# no one is asked
# it is simply calculated how much taxes are needed to eliminate poverty according to the definition

# flavors of ubi
# 1. centrally calculated
# 2. asked democratically direction vs. traditional

# on the matter of UBI inflation is an issue in the current debate
# has to be set such that inflation doesn't push up
# should supply of money increase?
# deflation? maybe more money shifts to firms?
# could also be future work

class Gov_naive(object):
    
    def __init__(self, sim: object):
        self.sim = sim          # link government to the simulation
        self.money = 0          # money available to government for redistribution
        self.tax_rate = 0       # taxrate collected from each hh monthly
        self.ubi = 0            # ubi paid to each hh monthly

    # TODO: test out some factors here (0.5 and 2)
    # taxrate is proportional to the gini index
    def vote_tax(self):
        self.tax_rate = self.sim.stat.hh_stat['metric']['gini'][-1]

    # ubi is equal for all hhs each month
    def calc_ubi(self):
        self.ubi = self.money / self.sim.hh_param['num_hh']

    # collect taxes from all households
    def collect_tax(self):
        for hh in self.sim.hh_list:
            self.money += hh.pay_tax(tax_rate)

    # pay equal ubi to all households
    def pay_ubi(self):
        for hh in self.sim.hh_list:
            hh.receive_ubi(self.ubi)

    # collect tax at end of year
    # pay out ubi next year based on amassed money of previous year
    # ubi changes each year
    # tax changes each 4 years

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation