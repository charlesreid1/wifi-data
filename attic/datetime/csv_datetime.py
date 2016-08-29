import datetime


# Example: parse two rows of information about access points
ap1 = "96:1A:CA:37:4C:50, 2016-02-04 14:29:12, 2016-02-04 14:25:15,  1,  54, OPN, ,   , -77,        2,        0,   0.  0.  0.  0,  11, xfinitywifi, "
ap2 = "10:86:8C:54:A5:B2, 2016-02-04 14:29:15, 2016-02-04 14:26:35, 11,  54, WPA2 WPA, CCMP TKIP,PSK, -76,        2,        0,   0.  0.  0.  0,  14, GiraffeAttack3, "
ap3 = "E8:3E:FC:9F:45:10, 2016-02-04 14:29:12, 2016-02-04 14:27:17,  1,  54, WPA2, CCMP TKIP,PSK, -66,        2,        0,   0.  0.  0.  0,   6, Fovich, "
ap4 = "02:15:99:A9:A5:B8, 2016-02-04 14:29:14, 2016-02-04 14:28:21,  4,  54, WPA2, CCMP,PSK, -66,        3,        0,   0.  0.  0.  0,  16, DIRECT-HnML-2160, "
ap5 = "96:C7:92:32:E7:60, 2016-02-04 14:29:15, 2016-02-04 14:29:19,  6,  54, OPN, ,   , -62,        1,        0,   0.  0.  0.  0,  11, xfinitywifi, "

# This all_ap variable is exactly what would result if you used Python's 
# built-in readlines() method:
# a list of strings.
all_ap = [ap1, ap2, ap3, ap4, ap5]



# Start by tokenizing the string
# Loop over each row
for ap in all_ap:

	tokens_with_whitespace = ap.split(",")
	tokens = [a.strip() for a in tokens_with_whitespace]
        import pdb; pdb.set_trace()
	
	# only two columns with date/time info:
	# column 1 and 2 (indexing starting at zero)
        print "-"*30

        print "Token 1: \""+tokens[1]+"\""
        print "Token 2: \""+tokens[2]+"\""

        dt1 = datetime.datetime.strptime(tokens[1], "%Y-%m-%d %H:%M:%S")
        dt2 = datetime.datetime.strptime(tokens[2], "%Y-%m-%d %H:%M:%S")

        print dt1.second
        print dt2.second


