from datetime import *

x = "2016-02-04 22:09:06"

print x

x_datetime = datetime.strptime(x, "%Y-%m-%d %H:%M:%S")


import pdb; pdb.set_trace()


## to print a list of every method of this datetime object:
#print dir(x_datetime)



# Demo
print "-"*30
print "The month is:", x_datetime.month
print "The day is:", x_datetime.day
print "The hour is:", x_datetime.hour
print "The day of the week is:", x_datetime.weekday()
print "As a Python tuple:", x_datetime.utctimetuple()
print "-"*30

