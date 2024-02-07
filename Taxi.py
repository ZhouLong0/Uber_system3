class Taxi:
    def __init__(self, id, pos, seats, env):
        self.__id = id
        self.__pos = pos
        self.__seats = seats
        self.__idle = True
        self.__env = env
        self.__customers = []
        self.path = None

    def get_pos(self):
        return self.__pos

    def get_seats(self):
        return self.__seats

    def set_pos(self, pos):
        self.__pos = pos

    def get_id(self):
        return self.__id

    def set_idle(self):
        self.__idle = True

    def is_idle(self):
        return self.__idle

    def set_occupied(self):
        self.__idle = False

    def get_customers(self):
        return self.__customers

    def get_cost(self):
        if self.__customers == []:
            return 0

        pick_up_points = [cust.get_start() for cust in self.__customers]

        dest_points = [cust.get_dest() for cust in self.__customers]

        path = self.__env.astar_multiple(self.__pos, pick_up_points)
        temp = path[-1]
        path = path + self.__env.astar_multiple(temp, dest_points)

        print(f"Current cost for taxi {self.__id}:", len(path))

        return len(path)

    def get_new_cost(self, customer):

        pick_up_points = [cust.get_start() for cust in self.__customers] + [
            customer.get_start()
        ]

        dest_points = [cust.get_dest() for cust in self.__customers] + [
            customer.get_dest()
        ]

        path = self.__env.astar_multiple(self.__pos, pick_up_points)
        temp = path[-1]
        path = path + self.__env.astar_multiple(temp, dest_points)

        print(f"new cost for taxi {self.__id}:", len(path))

        return len(path)

    def get_price(self):
        print(
            f"Current price for taxi{self.__id}:",
            sum([c.get_price() for c in self.__customers]),
        )
        return sum([c.get_price() for c in self.__customers])

    def get_new_price(self, customer):

        new_price = sum(
            [c.get_price() for c in self.__customers] + [customer.get_price()]
        )
        print(f"new price for taxi{self.__id}:", new_price)
        return new_price

    def get_utility(self):
        utility = self.get_price() - self.get_cost()
        print(f"Current utility for taxi{self.__id}:", utility)
        return utility

    def get_new_utility(self, customer):
        new_utility = self.get_new_price(customer) - self.get_new_cost(customer)
        print(f"new utility for taxi{self.__id}:", new_utility)
        return new_utility

    def isfull(self):
        return len(self.__customers) == self.__seats

    def add_customer(self, customer):
        self.__customers.append(customer)

    def move(self):
        if self.__customers:
            if not self.path:
                self.set_path()

            self.__pos = self.path.pop(0)
            print(f"Taxi {self.__id} moved to {self.__pos}")

            for customer in self.__customers:
                if customer.get_pickup_pos() == self.__pos:
                    print(f"Customer {customer.get_id()} picked up by taxi {self.__id}")
                if customer.get_dest() == self.__pos:
                    print(
                        f"Customer {customer.get_id()} dropped off by taxi {self.__id}"
                    )
                    customer.set_completed()
                    self.__customers.remove(customer)
            return

        print(f"Taxi {self.__id} is idle, so didn't move.")

    def set_path(self):
        """
        Set the path for the taxi to move in order to pick up and drop off the customers
        """
        pick_up_points = [cust.get_start() for cust in self.__customers]

        dest_points = [cust.get_dest() for cust in self.__customers]

        path = self.__env.astar_multiple(self.__pos, pick_up_points)
        temp = path[-1]
        path = path + self.__env.astar_multiple(temp, dest_points)
        self.path = path

    def __repr__(self):
        return f"Taxi {self.__id} at {self.__pos} with {self.__seats} seats, with customers {self.__customers}"
