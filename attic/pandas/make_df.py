import pandas as pd


def make_df(csv_file):
    """
    turn a csv file into a pandas dataframe
    """

    with open(csv_file) as f:
        lines = f.readlines()

    # Find where breaks in CSV file are located
    # (Split between APs and Clients)
    breaks = []
    for i in range(len(lines)):
        if len(lines[i].split(","))==1:
            breaks.append(i)

    # Use that to extract ap and client data
    try:
        # AP information
        ap_header_s  = lines[breaks[0]+1]
        ap_data_s    = lines[breaks[0]+2:breaks[1]-1]
        
        # Client information
        client_header_s = lines[breaks[1]+1]
        client_data_s   = lines[breaks[1]+2:breaks[2]-1]

    except IndexError:
        print("\n\nERROR: This file does not seem to be from the airodump-ng command.\n")
        exit(1)

        #tokens = [t.strip() for t in lines[i].split(",")]
        #if len(tokens)==1:
        #    breaks.append(i)

    ap_header = [token.strip() for token in ap_header_s.split(",")]

    ap_data = [[k.strip() for k in z.split(",")] for z in ap_data_s]

    ap_df = pd.DataFrame(ap_data, columns=ap_header)


    client_header = [token.strip() for token in client_header_s.split(",")]

    client_data = [[k.strip() for k in z.split(",")] for z in client_data_s]

    # clean up
    for d in client_data:
        if len(client_header) != len(d):
            z = ",".join(d[6:])
            d[6] = z
            del(d[7:])

    client_df = pd.DataFrame(client_data, columns=client_header)

    return ap_df, client_df


