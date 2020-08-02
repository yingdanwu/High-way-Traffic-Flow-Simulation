from decimal import Decimal, ROUND_UP
import heapq
import Car as Car
import Road as Road
# generate random integer
from random import random
class Solution: 
    def __init__(self):
        self.carDic={}
        self.roadDic={}
        self.ID=1
        self.data=[]
        self.enter_n=[0]*4
        self.exit_n=[0]*4
        self.exitTrue=[0]*4
        self.change=0
        self.carHistory=[]
        self.carChanged=set()
        self.carChangeEvent=[]
        self.roadHistory=[]
        self.roadClock=[0+9*i for i in range(100)]
        self.carWaited=set()
        self.carWaitedEvent=[]

    def genQueue(self,startT,endT,onRoad):
        queue=[]
        t=0
        while t<endT:
            newCar=Car.Car()
            newCar.ID=self.ID
            newCar.speed=1
            newCar.enterT=t
            newCar.T=t
            newCar.mainRoad=onRoad
            queue.append(newCar)
            t+=Decimal(str(random()*0.8+0.0001)).quantize(Decimal('.01'), rounding=ROUND_UP)
            self.carDic[self.ID]=newCar
            self.ID+=1
        return queue
        
    def update_velocity(self,Road,car,i,j):
        curtime=car.T
        if self.roadClock and abs(curtime-self.roadClock[0])<0.1:
            t=self.roadClock.pop(0)
            M=0
            for n in range(0,1):
                M+=self.enter_n[n]-self.exit_n[n]
            self.roadHistory.append(M)
        Road.velocity[i][j]=max(1/3600,(1.8*len(Road.cartime[i][j])/Road.intersection_length*(-0.079244)+53.035999)/3600)
#x:number of car in 1mile, y:average speed mile/hour, y=-0.079244x+53.035999
        car.velocity_history.append(round(Road.velocity[i][j],5))
        t= Road.intersection_length/Road.velocity[i][j]
        t=Decimal(str(t)).quantize(Decimal('.01'), rounding=ROUND_UP)
        car.T+=t
    
    def exitCheck(self):
        a=random()
        if a>0.3:return False
        else:return True
          
    def enter(self,car,FEL,road,j):
        ID=road.ID
        self.enter_n[ID]+=1
        road.intersection_car_number[0][j]+=1
        self.update_velocity(road,car,0,j)
        road.cartime[0][j].append(car.T)
        heapq.heappush(FEL,[car.T,"proceed"+str(ID)+"_1",car.ID,j])
        
    def exit(self,car,FEL,road,j):#j is the lane number
        road.intersection_car_number[-1][j]-=1
        ID=road.ID
        if road.cartime[-1][j]:road.cartime[-1][j].pop()
        self.exit_n[ID]+=1
        if ID==3:return car.ID, car.T
        if j==0 and self.exitCheck():
            self.exitTrue[ID]+=1
            self.data.append([car.ID,car.T])
        else:heapq.heappush(FEL,[car.T,"enter"+str(ID+1),car.ID,j])
    
    def proceed(self,car,FEL,Road_n,intersection_n):
        i,j=intersection_n
        road=self.roadDic[Road_n]
        if road.cartime[i-1][j]:road.cartime[i-1][j].pop(0)
        road.intersection_car_number[i-1][j]-=1
        if i<road.division-1:
            self.changelane(car,FEL,Road_n,intersection_n)
        else:
            road.intersection_car_number[i][j]+=1
            self.update_velocity(road,car,i,j)
            heapq.heappush(FEL, [car.T, "exit"+str(Road_n), car.ID,j])
            road.cartime[i][j].append(car.T)

    def changelane(self,car,FEL,Road_n,intersection_n):
        i,j=intersection_n
        road=self.roadDic[Road_n]
        if random()>0.5:
            if j==0:k=1
            else:k=0
            A,B,C,D=0,0,0,car.T+Decimal(str(road.intersection_length/road.velocity[i-1][j])).quantize(Decimal('.01'))
            if road.cartime[i][j]:C=road.cartime[i][j][-1]
            if road.cartime[i-1][k]:A=road.cartime[i-1][k][0]+Decimal(str(road.intersection_length/road.velocity[i-1][k])).quantize(Decimal('.01'), rounding=ROUND_UP)
            if road.cartime[i][k]:B=road.cartime[i][k][-1]
            if D-C<0.29 and D-B>0.3 and A-D>0.3:
                self.change+=1
                self.carChanged.add(car.ID)
                self.carChangeEvent.append([car.ID,road.ID,D,C,B,A])
                j=k
        road.intersection_car_number[i][j]+=1
        self.update_velocity(road,car,i,j)
        road.cartime[i][j].append(car.T)
        heapq.heappush(FEL,[car.T,"proceed"+str(Road_n)+"_"+str(i+1),car.ID,j])
        
                
    def conflict(self,list,sofar,last,FEL):
        mainroad=[False]*3   ##check whether there is event on the mainroad
        for event in list:
            if event[1] in {"exit0","exit1","exit2"} and event[-1]==0:
                mainroad[int(event[1][-1])]=True
        for event in list:
            if event[1] in {"enter1","enter2","enter3"}:
                i=int(event[1][-1])-1
                if last[i]>event[0]:
                    #print("Back to FEL",list)
                    heapq.heappush(FEL,[event[0]+sofar[i],event[1],event[2],0])
                    list.remove(event)
                else:
                    if mainroad[i]==True:
                        # print("conflict",list)
                        carID=event[2]
                        self.carWaited.add(carID)
                        #print(list,carID)
                        sofar[i]+=Decimal(str(0.5)).quantize(Decimal('.01'), rounding=ROUND_UP)
                        heapq.heappush(FEL,[event[0]+sofar[i],event[1],event[2],0])
                        list.remove(event)
                    else:
                        #print("no conflict",list)
                        sofar[i]=0
                        last[i]=event[0]
        #print("afterlist",list)
        return

    def main(self,startT,endT): 
        FEL=[]
        #Generate Queue at enters
        Q0=self.genQueue(startT,endT,True)
        Q1=self.genQueue(startT,endT,False)
        Q2=self.genQueue(startT,endT,False)
        Q3=self.genQueue(startT,endT,False)
        #Generate four roads with its length and number of sections and IDs
        Road0=Road.Road(0.2,2,2,0)
        Road1=Road.Road(0.8,8,2,1)
        Road2=Road.Road(0.8,8,2,2)
        Road3=Road.Road(0.4,4,2,3)
        self.roadDic[0]=Road0
        self.roadDic[1]=Road1
        self.roadDic[2]=Road2
        self.roadDic[3]=Road3
        #Put the queue at enters into the Future Event List(FEL)
        for car in Q0:
            j=int(random()//(1/2))
            heapq.heappush(FEL,[car.T,"enter0",car.ID,j])
        for car in Q1:
            heapq.heappush(FEL,[car.T,"enter1",car.ID,0])
        for car in Q2:
            heapq.heappush(FEL,[car.T,"enter2",car.ID,0])
        for car in Q3:
            heapq.heappush(FEL,[car.T,"enter3",car.ID,0])
        #Use carHistory to record information of event with the index of Car's ID
        self.carHistory=[[] for _ in range(self.ID+1)]
        #record wait time at entry due to conflict
        Waittime_sofar=[0]*3
        Lastvehicle_outtime=[0]*3
        #Start FEL
        while FEL:
            event=heapq.heappop(FEL)
            curtime=event[0]
            event_list=[event]
            while FEL and FEL[0][0]==curtime:
                event_list.append(heapq.heappop(FEL))
            for event in event_list:
                ID=event[-2]
                self.carHistory[ID].append(event)
            self.conflict(event_list,Waittime_sofar,Lastvehicle_outtime,FEL)  
            for event in event_list:
                ID=event[-2]
                car=self.carDic[event[2]]
                if event[0]>endT:break
                if event[1] in {"enter0","enter1","enter2","enter3"}:
                    road=self.roadDic[int(event[1][-1])]
                    self.enter(car,FEL,road,event[-1])
                elif event[1] in {"exit0","exit1","exit2","exit3"}:
                    road=self.roadDic[int(event[1][-1])]
                    self.exit(car,FEL,road,event[-1])
                else:
                    Road_n=int(event[1][-3])
                    intersection_n=[int(event[1][-1]),event[-1]]
                    self.proceed(car,FEL,Road_n,intersection_n)
                    
    def get_carTotal(self):
        print("Total number of car",self.ID)
    def get_conflictTotal(self):
        print("Total number of conflict",len(self.carWaited))
    def get_laneChange(self):
        print("Total number of lanechange",self.change)
    def get_laneChangeCar(self):
        print("Total number of car changed lane",len(self.carChanged))        
    def get_car_Passing_Enter_Exit(self):
        print("Number of car passed the four enters",self.enter_n)
        print("Number of car passed the four exits",self.exit_n)
        print("Number of car leaves the main road",sum(self.exitTrue)-self.exitTrue[-1]+self.exit_n[-1])
    def get_change_lane_event(self,n):
        change_Lane_List=[]
        for _ in range(n):
            change_Lane_List.append(self.carChanged.pop())
        for ID in change_Lane_List:
            print(self.carHistory[ID])
            for event in self.carChangeEvent:
                if event[0]==ID:print("Changelane: carID,roadID,car_time,car_ahead_time,next_lane_car_time,next_lane_car_behind_time",event)
    def get_conflict_event(self,n):    
        waited_list=[]
        for _ in range(n):
            waited_list.append(self.carWaited.pop())
        for ID in waited_list:
            print(self.carHistory[ID][0:5])
    def get_car_velocity(self,list):
        velocity_list=list
        for carID in velocity_list:
            car=self.carDic[carID]
            #shows where the selected car starts and end
            print("ID:",carID,"Start:",self.carHistory[carID][0][1],"End:",self.carHistory[carID][-1][1])
            print(car.velocity_history)
        
                
        print("finish")
        return 
        
test=Solution()
test.main(0,15*60)  #(startT,endT)
# test.get_carTotal()
# test.get_conflictTotal()
# test.get_laneChange()
# test.get_laneChangeCar()
# test.get_car_Passing_Enter_Exit()
#test.get_change_lane_event(1)#input is how many event do you want
# test.get_conflict_event(1)#input is how many event do you want
test.get_car_velocity([301,401,501])
