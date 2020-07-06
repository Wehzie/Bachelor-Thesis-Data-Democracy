# Bachelor-Thesis-Data-Democracy

This program models a simple economy.
Two types of relationships exist between firms and households.
Firstly, firms produce items which are sold to households.
Secondly, firms employ housholds to produce items.
Each month, item prices and wages are updated based on supply and demand.
This is done in a Multi-agent system (MAS) manner.
Here, each agent makes its own decisions with the limited information available to it. 

Additionally, the program implements three types of governments responsible for redistributing money by means of a flat rate tax and a universal basic income (UBI). Only households are taxed and receive UBI. The governments differ in the process of determining the flat tax and ubi. A comparison of these mechanisms is at the center of this work.

## Getting Started

To run the program on you local machine see the following instructions.
 
### Prerequisites

A version of Python 3.5 or greater is needed. On Linux run the following to check your version.

        python3 --version   # Ubuntu, Debian
        python --version    # Arch, Fedora

The Python modules Matplotlib, Numpy and SciPy are needed. Lower versions may work but I have used matplotlib 3.2.1, numpy 1.17.3 and scipy 1.5.1. On Linux run the following to confirm that you have the packages installed.

        pip3 list   # Ubuntu, Debian
        pip list    # Arch, Fedora

### Installing

#### Debian/Ubuntu

Python, pip, Matplotlib and Numpy are installed as follows.

        sudo apt install python3 python3-pip
        pip3 install -U matplotlib numpy scipy

To generate plots in pgf format that can be read by LaTeX, a form of LaTeX must be installed.
The genration of pgf plots is enabled by default, however it can easily be disabled in `main.py`; then a LaTeX install is no longer needed.

        sudo apt install texlive texlive-xetex

## Running the simulation

Clone the project using Git or download manually.

        git clone https://github.com/Wehzie/Bachelor-Thesis-Data-Democracy.git

Before starting the program set your working directory to the project folder.

        cd path/to/Bachelor-Thesis-Data-Democracy

To start the program run the following command. The program will run with default parameters.

        python3 src/main.py

To run the simulation with different parameters open the help menu to learn more about what parameters to set.

        python3 src/main.py --help

To run the simulation in the background after closing the terminal use the following command. Parameters such as --help must stand before the ampersand '&' symbol.

        nohup python3 src/main.py &

## Acknowledgments

This program is a Python reimplementation and extension based on the works of the following paper:  

- Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior and Organization, 86, 102-120. doi:10.1016/j.jebo.2012.12.021

The author of the paper wrote a model in Java and kindly made that code available. He also pointed to a project which lead to a rewrite of the model using a simulation building tool that transpiles to JavaScript. The JavaScript model can be found on https://sim4edu.com/sims/20/LengnickBaselineEconomy-1. In doing the Python rewrite, I mainly relied on the JavaScript code, which is licenced as follows:

 - Copyright 2018 Brandenburg University of Technology, Germany
 - The MIT License (MIT)
 - Luis Gustavo Nardin
 - Gerd Wagner

As such, I would like to thank Matthias Lengnick, Gustavo Nardin and Gerd Wagner for their work.

Furthermore I am happy to have been supervised in my project by Davide Grossi at the University of Groningen in the Netherlands. A special thank you goes to my Papa, Peter Tappe, who was always available for questions regarding economics. Nils Kruse deserves credit for sharing his experience with programming paradigms and Java. In a more indirect way the student association Cover has been a great inspiration. As part of the DisCover committee I got to write a dystopian article about how data could change democracy. This work lead me to approach Professor Grossi with this thesis idea.
