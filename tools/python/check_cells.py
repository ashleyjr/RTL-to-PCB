import argparse

PAD="-"
NOT="$_NOT_"
NOR="$_NOR_"
DFF="$_DFF_PN0_"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str)
    parser.add_argument("--top", type=str)
    parser.add_argument("--netlist", action='store_true')
    args = parser.parse_args()

    f = open(args.filename,"r+")
    n = f.read()
    f.close()

    pads = []
    nors = []
    dffs = []

    netlist = {}


    print("Instance Check...", end='')
    for l in n.split("\n")[0:-1]:
        s = l.split("\t")
        assert s[0] == args.top
    print("OK")

    print("Cells Check...", end='')
    for l in n.split("\n")[0:-1]:
        s = l.split("\t")
        assert s[2] in [PAD, NOT, NOR, DFF]
        if s[2] == NOT:
            assert s[3] in ["A", "Y"]
        if s[2] == NOR:
            assert s[3] in ["A", "B", "Y"]
        if s[2] == DFF:
            assert s[3] in ["D", "Q", "C", "R"]
    print("OK")

    print("Building cell list...", end='')
    for l in n.split("\n")[0:-1]:
        s = l.split("\t")

        if s[2] == PAD:
            assert s[1] not in netlist
            if f"P{s[1]}" not in netlist:
                netlist[f"P{s[1]}"] = []
            netlist[f"P{s[1]}"].append({"A" : s[5]})

        if s[2] == NOT:
            if f"N{s[1]}" not in netlist:
                netlist[f"N{s[1]}"] = []
            netlist[f"N{s[1]}"].append({s[3] : s[5]})
            if s[3] == "A":
                netlist[f"N{s[1]}"].append({"B" : s[5]})

        if s[2] == NOR:
            if f"N{s[1]}" not in netlist:
                netlist[f"N{s[1]}"] = []
            netlist[f"N{s[1]}"].append({s[3] : s[5]})

        if s[2] == DFF:
            if f"D{s[1]}" not in netlist:
                netlist[f"D{s[1]}"] = []
            netlist[f"D{s[1]}"].append({s[3] : s[5]})
    print("OK")

    print("Rename Cells...")
    cells = {}
    for i,n in enumerate(netlist):
        cells[f"{n[0]}{i}"] = netlist[n]
    print("OK")

    print("Collecting All Nets...")
    all_nets = []
    for n in cells:
        for s in cells[n]:
            for p in s:
                net = s[p]
                if net not in all_nets:
                    all_nets.append(net)
    print("OK")

    print("Renaming All Nets...")
    for n in cells:
        for s in cells[n]:
            for p in s:
                for i,net in enumerate(all_nets):
                    if s[p] == net:
                        s[p] = i
    print("OK")


    print("Cell Count...")
    for t in ["P", "N", "D"]:
        i = 0
        for n in cells:
            if t == n[0]:
                i += 1
        print(f"\t{i} {t}(s)")

    if args.netlist:
        print("Print Netlist")
        for n in cells:
            print(n, end='')
            for p in cells[n]:
                print(f"\t{p}", end='')
            print("")

if "__main__" == __name__:
    main()
