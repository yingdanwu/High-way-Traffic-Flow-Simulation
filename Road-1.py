class Road():
    def __init__(self,l,division,lane_num,ID):
        self.ID=ID
        self.division=division
        self.lane_num=lane_num
        self.length=l
        self.intersection_length=l/division
        self.number=0
        self.intersection_car_number=[[0 for j in range(lane_num)] for i in range(division)]
        self.velocity=[[20/3600 for _ in range(lane_num)] for _ in range(division)]
        self.cartime=[[[] for _ in range(lane_num)]for _ in range(division)]