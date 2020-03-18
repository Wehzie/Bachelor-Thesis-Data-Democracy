

from simulation import Simulation

def main():
    num_months = 100

    #print("(1) Default parameters.")
    #print("(2) Set number of months.")

    #user_input = int(input())
    #if(user_input == 2): num_months = int(input("Enter number of months: ")) 

    testsim = Simulation(num_months)
    testsim.start_sim()

if __name__ == "__main__":
    main()
    