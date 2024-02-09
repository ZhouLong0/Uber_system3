import json
import random
import numpy as np
import sys
import io
import os
import matplotlib.pyplot as plt

from Taxi import Taxi
from Customer import Customer
from Environment import Environment
from UberSystem import UberSystem


class Simulation:
    def __init__(self, env, customers, taxis):
        self.env = env
        self.customers = len(customers)
        self.taxis = len(taxis)
        self.uber_system = UberSystem(taxis, customers, self.env)
        #self.message_count_per_round = []

    def generate_environment_data(num_taxis, num_customers, grid_size):
        # Generate the environment matrix with 0 values
        environment = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        # Randomly place taxis and customers in the matrix, avoiding collisions
        available_positions = [
            (x, y) for x in range(grid_size) for y in range(grid_size)
        ]
        taxi_positions = random.sample(available_positions, num_taxis)
        available_positions = [
            pos for pos in available_positions if pos not in taxi_positions
        ]
        customer_positions_start = random.sample(available_positions, num_customers)
        available_positions = [
            pos for pos in available_positions if pos not in customer_positions_start
        ]
        customer_positions_des = random.sample(available_positions, num_customers)

        data = {
            "Customers": [
                {
                    "Customer": i + 1,
                    "start_pos": [list(start_pos)],
                    "dest_pos": [list(des_pos)],
                }
                for i, (start_pos, des_pos) in enumerate(
                    zip(customer_positions_start, customer_positions_des)
                )
            ],
            "Taxis": [
                {"Taxi": i + 1, "start_pos": [list(pos)], "n_seats": 4}
                for i, pos in enumerate(taxi_positions)
            ],
            "Environment": environment,
        }

        return data

    def generate_test_cases(
            num_customers, num_taxis, grid_size=10
    ):
         data = Simulation.generate_environment_data(num_taxis, num_customers, grid_size)
         with open(
              os.path.join(
                   "experiment", f"Customers_{num_customers}_Taxis_{num_taxis}.json"
                   ),
                   "w",) as f:
              json.dump([data], f, indent=4)
    


    @staticmethod
    def read_from_file(filepath):
        customers = []
        taxis = []
        with open(filepath, "r") as file:
            try:
                simulations = json.load(file)
            except:
                raise Exception("File is not JSON")

        for simulation in simulations:
            CustomerList = simulation["Customers"]
            TaxiList = simulation["Taxis"]
            grid = np.array(simulation["Environment"])
            env = Environment(grid)

            for customer in CustomerList:
                customers.append(
                    Customer(
                        customer["Customer"],
                        tuple(customer["start_pos"][0]),
                        tuple(customer["dest_pos"][0]),
                    )
                )
            for taxi in TaxiList:
                taxis.append(
                    Taxi(
                        taxi["Taxi"], tuple(taxi["start_pos"][0]), taxi["n_seats"], env
                    )
                )

        return Simulation(env, customers, taxis)

    def simulate(self, num_turns, num_taxis,num_customers):
        self.message_count_per_round = []
        logs = []
        for _ in range (num_turns):
            original_stdout = sys.stdout
            sys.stdout = io.StringIO()

            # self.env.print_state()
            self.uber_system.simulate(1)
            sys.stdout.seek(0)
            message_list = sys.stdout.read().splitlines()

            logs.append(message_list)

            sys.stdout = original_stdout

        with open(os.path.join("logs", f"Logs_{num_taxis}_taxis_{num_customers}_customers.json"), "w") as json_file:
            json.dump({"logs": logs}, json_file, indent=4)


if __name__ == "__main__":
    # Save the data to a JSON file
    random.seed(99)
    num_taxis = 100
    num_customers = 20
    Simulation.generate_test_cases(
        num_customers, num_taxis, grid_size=20
    )

    # Simulation
    sim_rec = Simulation.read_from_file(f"experiment\Customers_{num_customers}_Taxis_{num_taxis}.json")
    sim_rec.simulate(50,num_taxis,num_customers)

    print("number of taxis: ", num_taxis)
    print("Final Total Welfare: ", sim_rec.uber_system.get_welfare()/num_taxis)
    print("Final Delivery Time: ", sim_rec.uber_system.get_customer_duration())

    # todo: make the grid with obstacles
    