import pymatgen.io.vasp.outputs as vasp_utility
import pymatgen.io.cube as cube_utility
import pymatgen.core.periodic_table as ptable
import numpy as np
import argparse

ANG_TO_BOHR = 1.889725985
AMU_TO_EV = -1/27.212

def main(input, output):
    vol_data = vasp_utility.VolumetricData.from_hdf5(filename=input)
    struct = vol_data.structure
    atom_count = len(struct)
    origin = (0, 0, 0)
    ngrid = vol_data.dim

    lattice = np.asarray(vol_data.structure.lattice.as_dict()['matrix']) * ANG_TO_BOHR
    for i in range(3):
        lattice[i] = lattice[i] / ngrid[i]

    header = ['--------------------REPEAT charges--------------------\n',
            '---cube file created from VASP (LOCPOT and OUTCAR)----\n',
            '% 5s' % atom_count,
            '% 12.6f% 12.6f% 12.6f\n' % origin,
            '% 5s' % ngrid[0],
            '% 12.6f% 12.6f% 12.6f\n' % tuple(lattice[0]),
            '% 5s' % ngrid[1],
            '% 12.6f% 12.6f% 12.6f\n' % tuple(lattice[1]),
            '% 5s' % ngrid[2],
            '% 12.6f% 12.6f% 12.6f\n' % tuple(lattice[2])]

    coords = []

    for n, atom in enumerate(struct):
        coords.append('%5.0f% 12.6f% 12.6f% 12.6f% 12.6f\n' % (ptable.Element(struct[n].specie).Z,
                                                            ptable.Element(struct[n].specie).Z,
                                                            atom.coords[0] * ANG_TO_BOHR,
                                                            atom.coords[1] * ANG_TO_BOHR,
                                                            atom.coords[2] * ANG_TO_BOHR))


    data = []

    for x in range(ngrid[0]):
        for y in range(ngrid[1]):
            for n_iter, z in enumerate(range(ngrid[2])):
                data.append('%13.5E' % (vol_data.data['total'][x][y][z] * AMU_TO_EV))
                if not (n_iter + 1) % ngrid[2]:
                    data.append("\n")
                elif not (n_iter + 1) % 6:
                    data.append("\n")

    lines = header + coords + data

    with open(output, "w") as f:
        for line in lines:
            f.write(line)
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)

    args = parser.parse_args()

    input = args.input
    output = args.output

    main(input, output)
