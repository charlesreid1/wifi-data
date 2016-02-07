with open('../csv/awesome-01.csv') as f:
    lines = f.readlines()



# Find where breaks in CSV file are located
# (Split between APs and Clients)
breaks = []
for i in range(len(lines)):
    tokens = [t.strip() for t in lines[i].split(",")]
    if len(tokens)==1:
        breaks.append(i)



# Use that to extract ap and client data

ap_header    = lines[breaks[0]+1]
ap_data      = lines[breaks[0]+2:breaks[1]-1]

client_header = lines[breaks[1]+1]
client_data   = lines[breaks[1]+2:breaks[2]-1]


print "AP MAC list:"
for ap in ap_data:
    print ap[0]

