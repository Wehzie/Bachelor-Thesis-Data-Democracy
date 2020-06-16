

# Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

from simulation import Simulation

def main():
    num_months = 10
    gov_types = [None, 'naive']
    gov_type = gov_types[0]

    #print("(1) Default parameters.")
    #print("(2) Set number of months."

    #user_input = int(input())
    #if(user_input == 2): num_months = int(input("Enter number of months: ")) 

    testsim = Simulation(num_months, gov_type)
    testsim.start_sim()

if __name__ == "__main__":
    main()
    