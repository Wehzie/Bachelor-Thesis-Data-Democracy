

# sample randomly from households
# firms are not in government since firms are composed of households, this more closely reflects political reality

# divide households into quintiles by money
# analyze movement between quintiles over time

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
# has to be set such that inflation doesnt push up
# should supply of money increase?
# deflation? maybe more money shifts to firms?
# could also be future work




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
        self.tax_rate = 0       # taxrate collected from each hh monthly
        self.ubi = 0            # ubi paid to each hh monthly

    # a taxrate is voted for based on a target UBI
    # aim to achieve a target equality score 
    def vote_tax(self):
        term_length = 12 * 4    
        statistics.median(self.sim.hh_list)
        

    # ubi is equal for all hhs each month
    # ubi is not constant but is calculated based on available tax money each month
    def calc_ubi(self):
        self.ubi = self.money / self.sim.hh_param['num_hh']

    # Alternatively the taxrate could vary each month
    def collect_tax(self):
        for hh in self.sim.hh_list:
            self.money += hh.pay_tax(tax_rate)

    # TODO: does ubi have to be constant, can this be planned for?
    def pay_ubi(self):
        for hh in self.sim.hh_list:
            hh.receive_ubi(self.ubi)

    # collect tax at end of year
    # pay out ubi next year based on ammased money of previous year
    # ubi changes each year

######## ######## ######## IMPORTS ######## ######## ########

from simulation import Simulation
import statistics