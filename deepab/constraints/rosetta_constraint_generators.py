import os

import torch

from .ConstraintType import ConstraintType
from .Constraint import Constraint

logit_to_energy = lambda _, y: -1 * y


def write_histogram_file(constraint: Constraint,
                         histogram_dir: str,
                         prob_to_energy=logit_to_energy) -> str:
    x_vals = [str(round(val.item(), 5)) for val in constraint.x_vals]
    y_vals = [
        str(round(val.item(), 5))
        for val in prob_to_energy(constraint.x_vals, constraint.y_vals)
    ]

    x_axis = "x_axis\t" + "\t".join([val for val in x_vals])
    y_axis = "y_axis\t" + "\t".join([val for val in y_vals])

    histogram_file = "{}_{}_{}".format(constraint.constraint_type.name,
                                       constraint.residue_1.index,
                                       constraint.residue_2.index)
    histogram_file = os.path.join(histogram_dir, histogram_file)

    with open(histogram_file, "w") as f:
        f.write(x_axis + "\n")
        f.write(y_axis + "\n")

    return histogram_file


def get_ca_distance_constraint(constraint: Constraint,
                               histogram_dir: str,
                               prob_to_energy=logit_to_energy) -> str:
    assert type(constraint) == Constraint
    assert constraint.constraint_type == ConstraintType.ca_distance

    histogram_file = write_histogram_file(constraint,
                                          histogram_dir,
                                          prob_to_energy=prob_to_energy)

    residue_1 = constraint.residue_1
    residue_2 = constraint.residue_2

    constraint_line = "AtomPair CA {0} CA {1} SPLINE ca_dist_{0}_{1} {2} 0 1 {3}\n".format(
        residue_1.index, residue_2.index, histogram_file, constraint.bin_width)

    return constraint_line


def get_cb_distance_constraint(constraint: Constraint,
                               histogram_dir: str,
                               prob_to_energy=logit_to_energy) -> str:
    assert type(constraint) == Constraint
    assert constraint.constraint_type == ConstraintType.cb_distance

    histogram_file = write_histogram_file(constraint,
                                          histogram_dir,
                                          prob_to_energy=prob_to_energy)

    residue_1 = constraint.residue_1
    residue_2 = constraint.residue_2

    constraint_line = "AtomPair CB {0} CB {1} SPLINE cb_dist_{0}_{1} {2} 0 1 {3}\n".format(
        residue_1.index, residue_2.index, histogram_file, constraint.bin_width)

    return constraint_line


def get_no_distance_constraint(constraint: Constraint,
                               histogram_dir: str,
                               prob_to_energy=logit_to_energy) -> str:
    assert type(constraint) == Constraint
    assert constraint.constraint_type == ConstraintType.no_distance

    histogram_file = write_histogram_file(constraint,
                                          histogram_dir,
                                          prob_to_energy=prob_to_energy)

    residue_1 = constraint.residue_1
    residue_2 = constraint.residue_2

    constraint_line = "AtomPair N {0} O {1} SPLINE no_dist_{0}_{1} {2} 0 1 {3}\n".format(
        residue_1.index, residue_2.index, histogram_file, constraint.bin_width)

    return constraint_line


def get_omega_dihedral_constraint(constraint: Constraint,
                                  histogram_dir: str,
                                  prob_to_energy=logit_to_energy) -> str:
    assert type(constraint) == Constraint
    assert constraint.constraint_type == ConstraintType.omega_dihedral

    assert constraint.residue_1.identity != "G"
    assert constraint.residue_2.identity != "G"

    histogram_file = write_histogram_file(constraint,
                                          histogram_dir,
                                          prob_to_energy=prob_to_energy)

    residue_1 = constraint.residue_1
    residue_2 = constraint.residue_2

    constraint_line = "Dihedral CA {0} CB {0} CB {1} CA {1} SPLINE omega_{0}_{1} {2} 0 1 {3}\n".format(
        residue_1.index, residue_2.index, histogram_file, constraint.bin_width)

    return constraint_line


def get_theta_dihedral_constraint(constraint: Constraint,
                                  histogram_dir: str,
                                  prob_to_energy=logit_to_energy) -> str:
    assert type(constraint) == Constraint
    assert constraint.constraint_type == ConstraintType.theta_dihedral

    assert constraint.residue_1.identity != "G"
    assert constraint.residue_2.identity != "G"

    histogram_file = write_histogram_file(constraint,
                                          histogram_dir,
                                          prob_to_energy=prob_to_energy)

    residue_1 = constraint.residue_1
    residue_2 = constraint.residue_2

    constraint_line = "Dihedral N {0} CA {0} CB {0} CB {1} SPLINE theta_{0}_{1} {2} 0 1 {3}\n".format(
        residue_1.index, residue_2.index, histogram_file, constraint.bin_width)

    return constraint_line


def get_phi_planar_constraint(constraint: Constraint,
                              histogram_dir: str,
                              prob_to_energy=logit_to_energy) -> str:
    assert type(constraint) == Constraint
    assert constraint.constraint_type == ConstraintType.phi_planar

    assert constraint.residue_1.identity != "G"
    assert constraint.residue_2.identity != "G"

    histogram_file = write_histogram_file(constraint,
                                          histogram_dir,
                                          prob_to_energy=prob_to_energy)

    residue_1 = constraint.residue_1
    residue_2 = constraint.residue_2

    constraint_line = "Angle CA {0} CB {0} CB {1} SPLINE phi_{0}_{1} {2} 0 1 {3}\n".format(
        residue_1.index, residue_2.index, histogram_file, constraint.bin_width)

    return constraint_line


constraint_type_generator_dict = {
    ConstraintType.ca_distance: get_ca_distance_constraint,
    ConstraintType.cb_distance: get_cb_distance_constraint,
    ConstraintType.no_distance: get_no_distance_constraint,
    ConstraintType.omega_dihedral: get_omega_dihedral_constraint,
    ConstraintType.theta_dihedral: get_theta_dihedral_constraint,
    ConstraintType.phi_planar: get_phi_planar_constraint,
}