import heapq
import numpy as np
import random
import time
from Auction import Auction
from Environment import Environment
from Customer import Customer


class UberSystem:
    def __init__(self, taxis, customers, env):
        """
        drivers: list of drivers
        customers: list of customers
        env: Environment object
        """
        self.__taxis = taxis
        self.__customers = customers
        self.__env = env
        self.__round = 0

    def get_customers(self):
        return self.__customers

    def get_rides(self):
        return self.__rides

    def report_num_customers(self):
        return self.__customers

    def report_num_taxis(self):
        return self.__taxis

    def get_free_taxis(self):
        return [taxi for taxi in self.__taxis if taxi.is_idle()]

    def get_idle_customers(self):
        return [customer for customer in self.__customers if customer.is_idle()]

    def get_idle_taxis(self):
        return [taxi for taxi in self.__taxis if taxi.is_idle()]

    def start_auction(self):
        """
        Start the auction for the customers
        """
        print("New auction starting")
        print("Taxis: ", self.__taxis)
        print("Customers: ", self.__customers)

        print("partecipating taxis: ", self.get_idle_taxis())
        print("partecipating customers: ", self.get_idle_customers())

        if self.get_idle_taxis() and self.get_idle_customers():
            auction = Auction(
                self.get_idle_taxis(), self.get_idle_customers(), self.__env
            )
            auction.start_auction()

        else:
            print("no taxis or customers to start auction")

    def simulate_one_turn(self):
        """
        Simulate one turn of the Uber System
        """
        print(
            f"-----------------------------Round {self.__round}-----------------------------"
        )

        for taxi in self.__taxis:
            taxi.move()
        self.update_customer()
        self.update_taxis()

        self.__round += 1

        print(
            f"---------------------Map---------------------"
        )
        grid = self.__env.get_grid().copy()
        for taxi in self.__taxis:
            grid[taxi.get_pos()[0],taxi.get_pos()[1]] = len(taxi.get_customers())
        print(grid)

    def update_taxis(self):
        """
        Update the taxis in the system
        """
        for taxi in self.__taxis:
            if not taxi.get_customers():
                taxi.set_idle()

    def update_customer(self):
        """
        Update the customers in the system
        """
        for customer in self.__customers:
            if customer.is_completed():
                self.__customers.remove(customer)
                print(f"customer {customer.get_id()} completed")

    def spawn_customers(self):
        """
        Spawn new customers in the system
        """
        num_customers = random.randint(0, 2)
        for i in range(num_customers):
            start = (
                random.randint(0, self.__env.get_grid().shape[0] - 1),
                random.randint(0, self.__env.get_grid().shape[1] - 1),
            )
            dest = (
                random.randint(0, self.__env.get_grid().shape[0] - 1),
                random.randint(0, self.__env.get_grid().shape[1] - 1),
            )
            # destination can't be the same as start
            while dest == start:
                dest = (
                    random.randint(0, self.__env.get_grid().shape[0] - 1),
                    random.randint(0, self.__env.get_grid().shape[1] - 1),
                )

            customer = Customer(i, start, dest)
            self.__customers.append(customer)
            print(f"customer {i} spawned at {start} with destination {dest}")

    def simulate(self, num_rounds):
        """
        Simulate the Uber System for num_rounds
        """
        random.seed(48)
        for i in range(num_rounds):
            print(
                f"-----------------------------Round {self.__round}-----------------------------"
            )
            self.spawn_customers()

            if self.__round % 10 == 0:
                self.start_auction()

            self.simulate_one_turn()

    def print_state(self):
        print(
            f"-----------------------------Round {self.__round} State of Uber System -----------------------------"
        )
        print("Taxis: ")
        for taxi in self.__taxis:
            print(taxi)
        print("Customers: ")
        for customer in self.__customers:
            print(customer)
        print("\n")
