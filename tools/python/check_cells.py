import argparse

PAD="-"
NOT="NOT"
NOR="NOR"
DFF="DFF"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str)
    parser.add_argument("--top", type=str)
    parser.add_argument("--netlist", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    args = parser.parse_args()

    f = open(args.filename,"r+")
    n = f.read()
    f.close()

    pads = []
    nors = []
    dffs = []

    netlist = {}

    if not args.quiet:
        print(f"\t\t\t\t{args.filename}")
    else:
        print(f"{args.filename}:")


    if not args.quiet:
        print("Instance Check...", end='')
    for l in n.split("\n")[0:-1]:
        s = l.split("\t")
        assert s[0] == args.top

    if not args.quiet:
        print("OK")

    if not args.quiet:
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
    if not args.quiet:
        print("OK")

    if not args.quiet:
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
    if not args.quiet:
        print("OK")

    if not args.quiet:
        print("Rename Cells...", end='')
    cells = {}
    for i,n in enumerate(netlist):
        cells[f"{n[0]}{i}"] = netlist[n]
    if not args.quiet:
        print("OK")

    if not args.quiet:
        print("Collecting All Nets...",end='')
    all_nets = []
    for n in cells:
        for s in cells[n]:
            for p in s:
                net = s[p]
                if net not in all_nets:
                    all_nets.append(net)
    if not args.quiet:
        print("OK")

    if not args.quiet:
        print("Renaming All Nets...",end='')
    for n in cells:
        for s in cells[n]:
            for p in s:
                for i,net in enumerate(all_nets):
                    if s[p] == net:
                        s[p] = i
    if not args.quiet:
        print("OK")

    if not args.quiet:
        print("Cell Count:\t\t",end='')
    cnt = {"P": 0, "N": 0, "D": 0}
    for t in cnt:
        for n in cells:
            if t == n[0]:
                cnt[t] += 1
    print(f"{cnt['P']:30} P(s) {cnt['N']:5} N(s) {cnt['D']:5} D(s)")
    if not args.quiet:
        print("")

    if args.netlist:
        print("Print Netlist:")
        for n in cells:
            print(n, end='')
            for p in cells[n]:
                print(f"\t{p}", end='')
            print("")
    print("")

if "__main__" == __name__:
    main()
