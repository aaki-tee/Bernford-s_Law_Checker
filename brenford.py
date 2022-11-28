import csv
import math
import random
import collections

"""
Standard benford percentages
"""
BRENFORD_PERCENTAGES = [0, 0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]

def readfile(filename):
    """
    Read csv file in server
    Results are returned in the form of list
    """

    def conversion_to_list(file):
        return [row[0] for row in reader if row[0].isdigit()]

    with open(filename, 'r') as file:
        reader = csv.reader(file)

        return conversion_to_list(reader)


def calculate_brenford_values(data):

    """
    Calculates a set of values from the numeric list
    input data showing how closely the first digits
    fit the Benford Distribution.
    Results are returned as a list of dictionaries.
    """
    result = []

    list_of_first_digit = sorted(list(map(lambda n: str(n)[0], data)))
    frequencies_of_first_digit = collections.Counter(list_of_first_digit)
    

    
    for n in range(1, 10):
        data_frequency = frequencies_of_first_digit[str(n)]
        data_frequency_percentage = data_frequency / len(data)
        benford_frequency = len(data) * BRENFORD_PERCENTAGES[n]
        benford_frequency_percent = BRENFORD_PERCENTAGES[n]

        
        
        result.append({
            "digit": n,
            "expected_frequency": benford_frequency ,
            "expected_percentage": benford_frequency_percent,
            "observed_frequency": data_frequency,
            "observed_percentage": data_frequency_percentage
        })

    return result

def test_brenford(distribution):
    """
    Use chi-square test to check if the dataset follows the brendford law or not
    """
    chi_square_stat = 0
    for digit in distribution:
        chi_square = math.pow((digit["observed_frequency"] - digit["expected_frequency"]), 2)
        chi_square_stat += chi_square

    return chi_square < 15.51

def check_brenford(file, random_dist=False):
    """
    connects above three function 
    """
    if random_dist:
        data_list = [random.randint(1, 1000) for i in range(10000)]
    else:
        data_list = readfile(file)
    
    result = calculate_brenford_values(data_list)

    if test_brenford(result):
        return test_brenford(result), result
    return test_brenford(result), None