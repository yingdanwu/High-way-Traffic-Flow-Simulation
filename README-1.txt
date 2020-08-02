Please open: Main.py in Pyhton3

Input:
At the last line of the code: the two input is test.main(startT,endT) in second
Our simulation is for US101 for 15min, test.main(startT=0, endT=15*60)

Execution

Output:
There are 8 methods to get the simulation results.
1.get_carTotal():
	Get total number of cars generated in the FEL
2.get_conflictTotal():
	Get total number of conflicts taking place at the enters, which causes the delay of entering cars
3.get_laneChange():
	Get total number of a car changing lanes
4.get_laneChangeCar():
	Get total numer of the cars that has changed lanes
5.get_car_Passing_Enter_Exit():
	Get number of cars passing the four enters. The car can enter from the entrance or from the last section's end.
	Get number of cars passing the four exits. After passing the exits, the can exit the main road or proceed to the next section of the main road. 
	Get number of cars leaving the main road. Sum up the nnumber of cars that leaves the main road at four exits. 
6.get_change_lane_event(n):#input is how many events do you want
	Get n number of change-lane events.
	The first output is the history of a car that has changed lane. The second output is the situation where the car changes the lane.
	
	For instance:
	[[Decimal('468.95'), 'enter0', 1152, 1], [Decimal('479.39'), 'proceed0_1', 1152, 1], [Decimal('489.42'), 'exit0', 1152, 1], [Decimal('489.42'), 'enter1', 1152, 1], 
	[Decimal('499.45'), 'proceed1_1', 1152, 1], [Decimal('509.48'), 'proceed1_2', 1152, 1], [Decimal('519.51'), 'proceed1_3', 1152, 1], [Decimal('526.49'), 'proceed1_4', 1152, 0], 
	[Decimal('533.67'), 'proceed1_5', 1152, 0], [Decimal('540.85'), 'proceed1_6', 1152, 0], [Decimal('548.03'), 'proceed1_7', 1152, 0], [Decimal('555.21'), 'exit1', 1152, 0]]
	Changelane: carID,roadID,car_time,car_ahead_time,next_lane_car_time,next_lane_car_behind_time [1152, 1, Decimal('529.15'), Decimal('529.15'), Decimal('525.16'), Decimal('530.30')]
	
	It describes the car with ID:#1152 enters at #0 enter at #1 lane at 468.95s and proceeds until 529.15s changes lane at the 4th intersection of the #1 road.

7.get_conflict_event(1):#input is how many events do you want
	Get n number of conlict events.
	The output is the history of a car that wants to enter the mainroad, but wait for a certain time yielding to the mainroad's cars.
	
	For instance:
	[[Decimal('64.08'), 'enter2', 4608, 0], [Decimal('64.58'), 'enter2', 4608, 0], [Decimal('424.08'), 'proceed2_1', 4608, 0], [Decimal('784.08'), 'proceed2_2', 4608, 0], 
	[Decimal('806.66'), 'proceed2_3', 4608, 0]]

	It describes the car with ID:#4608 at #2 enter wants to enter the mainroad at 64.08s, but it conflicts with the mainroad'car. Thus, it waits until 64.58s and
	enters at #2 enter and proceeds to further...

8.get_car_velocity([301,401,501]):#input is list of carID that is 0<ID<5000
	Get the velocity history every 0.1 mile for a list of cars with their IDs.
	
	For instance:
	ID: 301 Start: enter0 End: proceed1_3
	[0.00602, 0.00958, 0.00028, 0.00028, 0.00028]
	ID: 401 Start: enter0 End: exit3
	[0.00879, 0.00919, 0.00919, 0.00998, 0.00998, 0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 
	0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01077, 0.01077, 0.01077, 0.01077, 0.01077]
	ID: 501 Start: enter0 End: exit3
	[0.01156, 0.01156, 0.01117, 0.01117, 0.01117, 0.01117, 0.01117, 0.01077, 0.01077, 0.01037, 
	0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01037, 0.01077, 0.01077, 0.01077, 0.01077]
	
	It describes the velocity history of #301, #401, #501 cars. For instance, #401 car enters from #0 enter with 0.00879 mile/s and leaves at #3 exit with 0.01077mile/s.