import os

def parse_ap_client_data( csv_file ):

    basename = os.path.splitext(csv_file)[0]

    print "Preparing to parse CSV file %s.csv"%(basename)
    
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

    if len(blank_lines) > 1:
        start = blank_lines[0]
        finish = blank_lines[1]
    else:
        start = 0
        finish = blank_lines[0]

    for i in range(start,finish):
        ap_stuff.append( stuff[i] )
    
    with open(basename+'_ap.csv','w') as f:
        for txt in ap_stuff:
            if txt<>'':
                f.write("%s\n" % txt )
    
    print "Finished writing AP data to file %s_ap.csv"%(basename)
    
    # -----
    client_stuff = []

    if len(blank_lines) > 1:
        start = blank_lines[1]
        finish = blank_lines[2]
    else:
        start = blank_lines[0]
        finish = len(stuff)

    for i in range(start, finish): 
        client_stuff.append( stuff[i] )
    
    with open(basename+'_client.csv','w') as f:
        for j,txt in enumerate(client_stuff):
            if txt<>'':

                # here is where you clean out extra commas
                # there should only be 7 columns
                # or 6 commas 
                # (or, index 5 with python's n-1 indexing)

                # comma index for this row of text
                txt_list = list(txt)
                ci = [i for i,z in enumerate(txt_list) if z==","]

                # at every comma index above the 5th,
                # turn the char at taht position into ';'
                if len(ci)>5:
                    for k in ci[6:]:
                        txt_list[k] = ';'

                # recombine char list into a string
                txt = ''.join(txt_list)

                f.write("%s\n" % txt )
    
    print "Finished writing client data to file %s_client.csv"%(basename)

if __name__=="__main__":

    for f in os.listdir('.'):
        if f.endswith('.csv'): 
            if '_ap' not in f and '_client' not in f: 
                print f
                parse_ap_client_data(f)

    print "\n\n\nAll done!\n\n\n\n"
