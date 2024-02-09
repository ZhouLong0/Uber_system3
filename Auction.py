class Auction:
    def __init__(self, taxis, customers, env):
        self.__taxis = taxis
        self.__customers = customers
        self.__env = env

    def start_auction(self):
        """
        Start the auction for the customers
        """
        for customer in self.__customers:
            self.auction_per_customer(customer)

    def auction_per_customer(self, customer):
        print("starting auction for customer: ", customer)
        bids = {}

        for taxi in self.__taxis:
            if taxi.isfull():
                continue
            if taxi.get_new_utility(customer) - taxi.get_utility() >0:
                bids[taxi] = taxi.get_new_utility(customer) - taxi.get_utility()
                print("taxi: ", taxi.get_id(), " bid: ", bids[taxi])
            else: print("taxi: ", taxi.get_id(),"did not bid.")

        if bids:
            winner_taxi = max(bids, key=bids.get)
            print(
                "winner taxi: ", winner_taxi.get_id(), " with bid: ", bids[winner_taxi]
            )
            winner_taxi.add_customer(customer)
            winner_taxi.set_occupied()
            no_first = [taxi for taxi in bids if taxi != winner_taxi]
            second_winner = bids[max(no_first, key = bids.get)]if len(no_first)>0 else 0
            winner_taxi.update_profit(bids[winner_taxi]-second_winner)
            customer.set_taken()

        else:
            print("No bids for customer: ", customer.get_id())
