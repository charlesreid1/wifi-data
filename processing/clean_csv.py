import os

def parse_ap_client_data( csv_file ):

    basename = os.path.splitext(csv_file)[0]
    
    with open(basename+'.csv','r') as f:
        stuff = f.readlines()
    
    # strip whitespace:
    stuff = [z.strip() for z in stuff]
    
    # find blank lines:
    blank_lines = [i for i,z in enumerate(stuff) if z=='']
    
    # first and last lines always blank
    # middle line is where file is split
    
    # -----
    ap_stuff = []
    for i in range(blank_lines[0],blank_lines[1]):
        ap_stuff.append( stuff[i] )
    
    with open(basename+'_ap.csv','w') as f:
        for txt in ap_stuff:
            f.write("%s\n" % txt )
    
    print "Finished writing AP data to file %s_ap.csv"%(basename)
    
    # -----
    client_stuff = []
    for i in range(blank_lines[1],blank_lines[2]):
        client_stuff.append( stuff[i] )
    
    with open(basename+'_client.csv','w') as f:
        for txt in client_stuff:
            f.write("%s\n" % txt )
    
    print "Finished writing client data to file %s_client.csv"%(basename)

if __name__=="__main__":

    for f in os.listdir('.'):
        if f.endswith('.csv'): 
            if '_ap' not in f and '_client' not in f: 
                print f
                parse_ap_client_data(f)

    print "\n\n\nAll done!\n\n\n\n"
