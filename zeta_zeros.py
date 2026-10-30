'''
This script takes a file containing the imaginary parts of the first 2000 zeros of the Riemann zeta function,
computes the high precision versions of these zeros, evaluates the derivative of the zeta function at each zero,
and writes the results to two separate output files.

Usage: python zeta_zeros.py <input low precision zeros file name> <zeros output file name> <derivatives output file name>

The input file should contain the imaginary parts of the zeros, one per line. The output files will contain the imaginary
parts of the zeros and their corresponding derivatives, respectively, with high precision.
'''
import sys
import mpmath as mp

# pylint: disable=line-too-long, multiple-statements

def main():
    """
    Main entry point of the script.
    """
    verbose = True

    # show usage if incorrect number of arguments
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input low precision zeros file name> <zeros output file name> <derivatives output file name>")
        sys.exit(-1)

    if verbose is True: print("Reading low precision zeros from input file...")

    input_file = open(sys.argv[1], 'r', encoding='utf-8')
    lines = input_file.readlines()
    input_file.close()
    low_prec_imag_part = [float(num) for num in lines[0:2000]]

    # get high prec version of first 2000 zeros
    mp.mp.dps = 100

    if verbose is True: print(f"Calculating high precision version of zeros; going out to {mp.mp.dps} decimal places...")

    high_prec_zeros = [mp.findroot(mp.zeta, 0.5 + imag_part*mp.j) for imag_part in low_prec_imag_part] if verbose is False else find_roots_verbose(low_prec_imag_part)
    zeta_derivatives = [mp.zeta(zero, derivative=1) for zero in high_prec_zeros] # evaluate derivative for each zero

    # write to files
    zeros_output_file = open(sys.argv[2], 'w', encoding='utf-8')
    deriv_output_file = open(sys.argv[3], 'w', encoding='utf-8')

    for _, zipped_zero in enumerate(zip(high_prec_zeros, zeta_derivatives)):
        hp_zero, deriv = zipped_zero
        zeros_output_file.write(mp.nstr(hp_zero.imag,100) + '\n')
        deriv_output_file.write(mp.nstr(deriv,100) + '\n')

    zeros_output_file.close()
    deriv_output_file.close()


def find_roots_verbose(low_prec_imag_parts):
    high_prec_zeros = [mp.mpf('nan') for _ in low_prec_imag_parts]

    for i, imag_part in enumerate(low_prec_imag_parts):
        print(f"Iteration {i+1}: finding root for zero with low precision imaginary part: {imag_part}i...")
        high_prec_zeros[i] = mp.findroot(mp.zeta, 0.5 + imag_part*mp.j)
        print(f"Found higher precision zero at: {high_prec_zeros[i].imag}i")

    return high_prec_zeros


if __name__ == '__main__':
    main()
