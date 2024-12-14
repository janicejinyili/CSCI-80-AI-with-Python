import csv
import sys


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    print(evidence)


def load_data(filename):

    with open(filename) as f:
        reader = csv.DictReader(f)
        rows = [list(row.values()) for row in reader]
    evidence = [row[0:17] for row in rows]
    label = [int(row[17] == 'TRUE') for row in rows]
    months = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
    for e in evidence:
        e[0] = int(e[0])
        e[1] = float(e[1])
        e[2] = int(e[2])
        e[3] = float(e[3])
        e[4] = int(e[4])
        e[5] = float(e[5])
        e[6] = float(e[6])
        e[7] = float(e[7])
        e[8] = float(e[8])
        e[9] = float(e[9])
        e[10] = months.index(e[10])
        e[11] = int(e[11])
        e[12] = int(e[12])
        e[13] = int(e[13])
        e[14] = int(e[14])
        e[15] = int(e[15] == 'Returning_Visitor')
        e[16] = int(e[16] == 'TRUE')
    return(evidence,label)


if __name__ == "__main__":
    main()