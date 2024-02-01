import argparse
import pickle

PAD="-"
NOT="NOT"
NOR="NOR"
DFF="DFF"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=str)
    parser.add_argument("--netlist", action='store_true')
    parser.add_argument("--quiet", action='store_true')
    args = parser.parse_args()

    f = open(args.top+".txt","r+")
    n = f.read()
    f.close()

    pads = []
    nors = []
    dffs = []

    netlist = {}

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
        if s[2] == PAD:
            assert s[4] in ["pi","po"]
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
            if s[4] == "pi":
                if f"I{s[1]}" not in netlist:
                    netlist[f"I{s[1]}"] = {}
                netlist[f"I{s[1]}"]["A"] = s[5]
            else:
                if f"O{s[1]}" not in netlist:
                    netlist[f"O{s[1]}"] = {}
                netlist[f"O{s[1]}"]["A"] = s[5]
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


    # Write KiCAD netlist
    f = open(args.top+".net","w+")
    f.write('(export (version "E")\n')

    f.write('\t(components\n')
    for n in cells:
        f.write(f'\t\t(comp (ref "{n}")\n')
        if n[0] == "D":
            f.write('\t\t\t(value "SN74LVC1G00DCKR")\n')
            f.write('\t\t\t(footprint "cells:SN74LVC1G00DCKR")\n')
            f.write('\t\t\t(libsource (lib "cells") (part "SN74LVC1G00DCKR") (description ""))\n')
        if n[0] == "N":
            f.write('\t\t\t(value "SN74LVC1G79DCKR")\n')
            f.write('\t\t\t(footprint "cells:SN74LVC1G00DCKR")\n')
            f.write('\t\t\t(libsource (lib "cells") (part "SN74LVC1G00DCKR") (description ""))\n')
        if n[0] in ["I","O"]:
            f.write('\t\t\t(value "PAD")\n')
            f.write('\t\t\t(footprint "cells:PAD")\n')
            f.write('\t\t\t(libsource (lib "cells") (part "PAD") (description ""))\n')

        f.write('\t\t)\n')
    f.write('\t)\n')

    # Add Library
    f.write('\t(libraries\n')
    f.write('\t\t(library (logical "cells")\n')
    f.write('\t\t(uri "/Users/ashleyr/RTL-to-PCB/investigation/2023_12_19_nands_and_flops/nands_and_flops/cells.kicad_sym"))\n')
    f.write('\t)\n')

    # Add Net
    f.write('\t(nets\n')
    for i in range(len(all_nets)):
        f.write(f'\t\t(net (code "{i+1}") (name "net{i}")\n')
        for cell in cells:
            for pin in cells[cell]:
                if cells[cell][pin] == i:
                    if cell[0] in ["I","O"]:
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
                    f.write(f'\t\t\t(node (ref "{cell}") (pin "{num}") (pinfunction "{pin}") (pintype "{io}"))\n')
        f.write("\t\t)\n")

    f.write(f'\t\t(net (code "{len(all_nets)+1}") (name "GND")\n')
    for cell in cells:
        if cell[0] != "P":
            f.write(f'\t\t\t(node (ref "{cell}") (pin "3") (pintype "power_in"))\n')
    f.write("\t\t)\n")

    f.write(f'\t\t(net (code "{len(all_nets)+2}") (name "VCC")\n')
    for cell in cells:
        if cell[0] != "P":
            f.write(f'\t\t\t(node (ref "{cell}") (pin "5") (pintype "power_in"))\n')
    f.write("\t\t)\n")

    f.write('\t)\n')
    f.write(')\n')
    f.close()

    # Write custom schematic file
    f = open(args.top+".sch","w+")
    for c in cells:
        f.write(f'{c}\n')
        for p in cells[c]:
            f.write(f'{cells[c][p]}\n')
    f.close()


if "__main__" == __name__:
    main()
