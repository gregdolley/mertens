'''
This script reads in the high precision zeros and derivatives of the zeta function, evaluates rho * zeta'(rho) for each zero,
and then evaluates the argument and reciprocal of rho * zeta'(rho). The results are written to separate output files.
'''
import sys
import mpmath as mp

# pylint: disable=line-too-long

def main():
    """
    Main function entry-point.
    """
    if  len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <zeros input file name> <derivatives input file name> <arg output file name> <alpha output file>")
        sys.exit(-1)

    mp.mp.dps = 100

    # read high prec zeros
    with open(sys.argv[1],'r', encoding='utf-8') as zeros_input_file:
        zero_lines: list[str] = zeros_input_file.readlines()
        high_prec_imag_part = [mp.mpf(num) for num in zero_lines]

    # read high prec derivatives
    with open(sys.argv[2],'r', encoding='utf-8') as deriv_input_file:
        deriv_lines = deriv_input_file.readlines()
        high_prec_derivs = [mp.mpmathify(num) for num in deriv_lines]

    # evaluate rho * zeta'(rho)
    rho_times_zeta = [(0.5 + high_prec_imag_part[i]*mp.j)*high_prec_derivs[i] for i in range(len(high_prec_imag_part))]

    # evaluate arg of (rho * zeta'(rho))
    arg_rhos = [mp.arg(rho) for rho in rho_times_zeta]

    # evaluate reciprocal of (rho * zeta'(rho))
    alpha_rhos = [1/abs(rho) for rho in rho_times_zeta]

    # write to files
    arg_output_file = open(sys.argv[3], 'w', encoding='utf-8')
    alpha_output_file = open(sys.argv[4], 'w', encoding='utf-8')
    for i in range(len(rho_times_zeta)):
        arg_output_file.write(mp.nstr(arg_rhos[i],100) + '\n')
        alpha_output_file.write(mp.nstr(alpha_rhos[i],100) + '\n')
    arg_output_file.close()
    alpha_output_file.close()


if __name__=='__main__':
    main()
