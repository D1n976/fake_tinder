class DataCounter :
    def __init__(self, cur_counter, counter_step, collection):
        self.cur_counter = cur_counter
        self.counter_step = counter_step
        self.data = collection

    def change_counter(self, action):
        if action == 'back' and self.cur_counter - self.counter_step >= 0:
            self.cur_counter -= self.counter_step
            return True
        elif action == 'next' and self.cur_counter + self.counter_step < len(self.data):
            self.cur_counter += self.counter_step
            return True
        return False

    def get_data(self):
        at = self.cur_counter
        to = self.cur_counter + self.counter_step
        return self.data[at : to if to < len(self.data) else len(self.data)]