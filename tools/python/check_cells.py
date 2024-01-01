import argparse
import pickle

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

    #if not args.quiet:
    #    print(f"\t\t\t\t{args.filename}")
    #else:
    #    print(f"{args.filename}:")


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
                netlist[f"P{s[1]}"] = {}
            netlist[f"P{s[1]}"]["A"] = s[5]

        if s[2] == NOT:
            if f"N{s[1]}" not in netlist:
                netlist[f"N{s[1]}"] = {}
            netlist[f"N{s[1]}"][s[3]] = s[5]
            if s[3] == "A":
                netlist[f"N{s[1]}"]["B"] = s[5]

        if s[2] == NOR:
            if f"N{s[1]}" not in netlist:
                netlist[f"N{s[1]}"] = {}
            netlist[f"N{s[1]}"][s[3]] = s[5]

        if s[2] == DFF:
            if f"D{s[1]}" not in netlist:
                netlist[f"D{s[1]}"] = {}
            netlist[f"D{s[1]}"][s[3]] = s[5]
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
            net = cells[n][s]
            if net not in all_nets:
                all_nets.append(net)
    if not args.quiet:
        print("OK")

    if not args.quiet:
        print("Renaming All Nets...",end='')
    for n in cells:
        for s in cells[n]:
            for i,net in enumerate(all_nets):
                if cells[n][s] == net:
                    cells[n][s] = i
    if not args.quiet:
        print("OK")

    if not args.quiet:
        print("Cell Count:\t\t",end='')
    cnt = {"P": 0, "N": 0, "D": 0}
    for t in cnt:
        for n in cells:
            if t == n[0]:
                cnt[t] += 1
    #print(f"{cnt['P']:30} P(s) {cnt['N']:5} N(s) {cnt['D']:5} D(s)")
    if not args.quiet:
        print("")

    if args.netlist:
        print("Print Netlist:")
        for n in cells:
            print(n, end='')
            for p in cells[n]:
                print(f"\t{p}", end='')
            print("")

    print('(export (version "E")')

    print('\t(components')
    for n in cells:
        print(f'\t\t(comp (ref "{n}")')
        if n[0] == "D":
            print('\t\t\t(value "SN74LVC1G00DCKR")')
            print('\t\t\t(footprint "cells:SN74LVC1G00DCKR")')
            print('\t\t\t(libsource (lib "cells") (part "SN74LVC1G00DCKR") (description ""))')
        if n[0] == "N":
            print('\t\t\t(value "SN74LVC1G79DCKR")')
            print('\t\t\t(footprint "cells:SN74LVC1G00DCKR")')
            print('\t\t\t(libsource (lib "cells") (part "SN74LVC1G00DCKR") (description ""))')
        if n[0] == "P":
            print('\t\t\t(value "PAD")')
            print('\t\t\t(footprint "cells:PAD")')
            print('\t\t\t(libsource (lib "cells") (part "PAD") (description ""))')

        print('\t\t)')
    print('\t)')

    # Add Library
    print('\t(libraries')
    print('\t\t(library (logical "cells")')
    print('\t\t(uri "/Users/ashleyr/RTL-to-PCB/investigation/2023_12_19_nands_and_flops/nands_and_flops/cells.kicad_sym"))')
    print('\t)')

    # Add Net
    print('\t(nets')
    for i in range(len(all_nets)):
        print(f'\t\t(net (code "{i+1}") (name "net{i}")')
        for cell in cells:
            for pin in cells[cell]:
                if cells[cell][pin] == i:
                    if cell[0] == "P":
                        if pin == "A":
                            num = "1"
                            io = "output"
                    if cell[0] == "D":
                        if pin == "Q":
                            num = "4"
                            io = "output"
                        if pin == "D":
                            num = "1"
                            io = "input"
                        if pin == "C":
                            num = "2"
                            io = "input"
                    if cell[0] == "N":
                        if pin == "A":
                            num = "1"
                            io = "input"
                        if pin == "B":
                            num = "2"
                            io = "input"
                        if pin == "Y":
                            num = "4"
                            io = "output"
                    print(f'\t\t\t(node (ref "{cell}") (pin "{num}") (pinfunction "{pin}") (pintype "{io}"))')
        print("\t\t)")

    print(f'\t\t(net (code "{len(all_nets)+1}") (name "GND")')
    for cell in cells:
        if cell[0] != "P":
            print(f'\t\t\t(node (ref "{cell}") (pin "3") (pintype "power_in"))')
    print("\t\t)")

    print(f'\t\t(net (code "{len(all_nets)+2}") (name "VCC")')
    for cell in cells:
        if cell[0] != "P":
            print(f'\t\t\t(node (ref "{cell}") (pin "5") (pintype "power_in"))')
    print("\t\t)")

    print('\t)')
    print(')')

    with open('test.pkl', 'wb') as f:
        pickle.dump(cells, f)


if "__main__" == __name__:
    main()
