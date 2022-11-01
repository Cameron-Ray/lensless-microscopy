import datetime


class Sample:
    def __init__(self, id, growth_rate_data, current_time, colony_count=0):
        self.id = id
        self.colony_count = colony_count
        self.load_time = current_time
        self.growth_rate_data = growth_rate_data

    def get_Sample_ID(self):
        if self.id == None:
            return "No Sample Loaded"
        else:
            return self.id
        
    def get_Colony_Count(self):
        if self.colony_count == None:
            return "No Sample Loaded"
        else:
            return self.colony_count

    def get_Elapsed_Time(self):
        if self.load_time == None:
            return "No Sample Loaded"
        else:
            elapsed = datetime.datetime.now() - self.load_time
            return str(elapsed.days) + "d " + str(elapsed.seconds//3600) + "h " + str(elapsed.seconds//60) + "m"

    def update_Growth_Rate(self, inst_colony_count):
        today = datetime.today().strftime('%Y-%m-%d')
        self.growth_rate_data[today] = inst_colony_count

    def calculate_Inst_Growth_Rate(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        if self.growth_rate_data == None:
            return "No Sample Loaded"
        else:
            if len(self.growth_rate_data) > 1:
                return ((self.growth_rate_data[today] - self.growth_rate_data[yesterday])/self.growth_rate_data[yesterday])*100
            elif len(self.growth_rate_data) <= 1:
                return "Not Enough Data"
