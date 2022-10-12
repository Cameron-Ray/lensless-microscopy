from datetime import datetime


class Sample:
    def __init__(self, id, growth_rate_data, current_time, colony_count=0):
        self.id = id
        self.colony_count = colony_count
        self.load_time = current_time
        self.growth_rate_data = growth_rate_data

    def get_Elapsed_Time(self):
        elapsed = datetime.datetime.now() - self.load_time
        return str(elapsed)

    def update_Growth_Rate(self, inst_colony_count):
        today = datetime.today().strftime('%Y-%m-%d')
        self.growth_rate_data[today] = inst_colony_count

    def calculate_Inst_Growth_Rate(self):
        today = datetime.today().strftime('%Y-%m-%d')
        yesterday = (datetime.today() - datetime.timedelta(day=1)).strftime('%Y-%m-%d')

        if len(self.growth_rate_data) > 1:
            return ((self.growth_rate_data[today] - self.growth_rate_data[yesterday])/self.growth_rate_data[yesterday])*100
        elif len(self.growth_rate_data) <= 1:
            return 0