from oops import oops

def extract_csv_data(csv_file):
    """
    Turn a CSV file into 4 lists:
    One list with AP header lines
    One list with AP data lines
    One list of client header lines
    One list with client data lines
    """

    with open(csv_file) as f:
        lines = f.readlines()

    # Find where breaks in CSV file are located
    # (Split between APs and Clients)
    breaks = []
    for i in range(len(lines)):
        tokens = [t.strip() for t in lines[i].split(",")]
        if len(tokens)==1:
            breaks.append(i)

    # Use that to extract ap and client data
    
    try:
        # AP information
        ap_header    = lines[breaks[0]+1]
        ap_data      = lines[breaks[0]+2:breaks[1]-1]
        
        # Client information
        client_header = lines[breaks[1]+1]
        client_data   = lines[breaks[1]+2:breaks[2]-1]

    except IndexError:
        print("\n\nERROR: This file does not seem to be from the airodump-ng command.\n")
        exit(1)

    return ap_header, ap_data, client_header, client_data

if __name__=="__main__":
    oops()
