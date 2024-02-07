import Environment as Env


class Customer:
    def __init__(self, id, start, dest):
        self.__id = id
        self.__start = start
        self.__dest = dest
        self.__idle = True
        self.picked_up = False
        self.__completed = False

    def get_dest(self):
        return self.__dest

    def get_start(self):
        return self.__start

    def is_idle(self):
        return self.__idle

    def get_req_seats(self):
        return self.__req_seats

    def get_id(self):
        return self.__id

    def set_completed(self):
        self.__completed = True

    def get_price(self):
        return 2 * abs(self.__start[0] - self.__dest[0]) + 2 * abs(
            self.__start[1] - self.__dest[1]
        )

    def get_pickup_pos(self):
        return self.__start

    def set_taken(self):
        self.__idle = False

    def is_completed(self):
        return self.__completed

    def __repr__(self):
        return f"Customer {self.__id} from {self.__start} to {self.__dest}"
