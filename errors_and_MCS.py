'''
Ввести параметр transmit_error_probability
При передаче N транспортных блоков(TB) посчитать сколько с ошибкой - BLER
Для 5G NR есть следующие типы модуляций:
QPSK
16 QAM
64 QAM
256 QAM

Начинаем приемлимое значение BLER
При передаче M бит посчитать сколько с ошибкой - Bit error rate
Ошибки в секунду - Bit error rate


Name	    Bits per symbol	    Number of symbols
QPSK        2                   2^2 = 4
16 QAM	    4	                2^4 = 16
64 QAM	    6	                2^6 = 64
256 QAM 	8	                2^8 = 256

In 5G, One NR Resource Block (RB) contains 12 sub-carriers in frequency domain similar to LTE.
In LTE resource block bandwidth is fixed to 180 KHz but in NR it is not fixed and depend on sub-carrier spacing.
'''
from math import log10, log2, floor

'''
MCS Index M Binary Code Rate Overall Code Rate rc
0         4        0.11719 0.2344
5         16 0.36914 1.4766
11        64 0.45508 2.7305
20        256 0.66650 5.3320
27        256 0.92578 7.4063
'''
sub_carriers = 12


modulations_bits_per_symbol = {
    'QPSK': 2,
    '16QAM': 4,
    '64QAM': 6,
    '256QAM': 8
}
# TBS for N_info <= 3824
TBS_N_info_less_eq_3824 = {

}


def get_transmit_characteristic(q):
    df = 2**q * 15

    if df == 15:
        return {'RB_size': sub_carriers * df, 'min_RBs': 24, 'max_RBs': 275, 'min_BW': 4320000, 'max_BW': 49500000}
    elif df == 30:
        return {'RB_size': sub_carriers * df, 'min_RBs': 24, 'max_RBs': 275, 'min_BW': 8640000, 'max_BW': 99000000}
    elif df == 60:
        return {'RB_size': sub_carriers * df, 'min_RBs': 24, 'max_RBs': 275, 'min_BW': 17280000, 'max_BW': 198000000}
    elif df == 120:
        return {'RB_size': sub_carriers * df, 'min_RBs': 24, 'max_RBs': 275, 'min_BW': 34560000, 'max_BW': 396000000}
    elif df == 240:
        return {'RB_size': sub_carriers * df, 'min_RBs': 24, 'max_RBs': 138, 'min_BW': 69120000, 'max_BW': 397440000}
    else:
        raise ValueError


def Eb_N0_from_dbSINR(db_SINR, bit_rate, BANDWIDTH=get_transmit_characteristic(0)['min_BW']):
    power_ratio_SINR = 10**(db_SINR/10)
    Eb_N0 = power_ratio_SINR * BANDWIDTH / bit_rate
    return Eb_N0


def CNR_db(Eb_N0, bit_rate, BANDWIDTH=get_transmit_characteristic(0)['min_BW']):
    CNR = Eb_N0 * bit_rate / BANDWIDTH
    CNR_in_db = 10*log10(bit_rate / BANDWIDTH) + 10*log10(Eb_N0)
    return CNR_in_db


'''
N_RE total no. of REs available for data transfer
R is Code Rate
Qm is Modulation Order
v is no. of MIMO layers
'''


def calculate_TBS(RB_count, R, Qm, v, N_RB_SC=12, N_SH_SYMBL=14, N_PRB_DMRS=6, N_PRB_oh=0):
    N_RE1 = N_RB_SC*N_SH_SYMBL - N_PRB_DMRS - N_PRB_oh
    N_RE = min(156, N_RE1) * RB_count
    N_info = N_RE * R * Qm * v
    if N_info <= 3824:
        n = max(3, floor(log2(N_info))-6)
        N_info = max(24, 2**n * floor(N_info/(2**n)))
    print(N_info)


SINR_and_Report_Mapping = {
    1: [-23, -22.5],
    2: [-22.5, -22.0],
    3: [-22.0, -21.5],
    4: [-21.5, -21.0],
    5: [-21.0, -20.5],
    6: [-20.5, -20.0],
    7: [-20.0, -19.5],
    8: [-19.5, -19.0],
    9: [-19.0, -18.5],
    10: [-18.5, -18.0],
    11: [-18.0, -17.5],
    12: [-17.5, -17.0],
    13: [-17.0, -16.5],
    14: [-16.5, -16.0],
    15: [-16.0, -15.5],
    16: [-15.5, -15.0],
    17: [-15.0, -14.5],
    18: [-14.5, -14.0],
    19: [-14.0, -13.5],
    20: [-13.5, -13.0],
    21: [-13.0, -12.5],
    22: [-12.5, -12.0],
    23: [-12.0, -11.5],
    24: [-11.5, -11.0],
    25: [-11.0, -10.5],
    26: [-10.5, -10.0],
    27: [-10.0, -9.5],
    28: [-9.5, -9.0],
    29: [-9.0, -8.5],
    30: [-8.5, -8.0],
    31: [-8.0, -7.5],
    32: [-7.5, -7.0],
    33: [-7.0, -6.5],
    34: [-6.5, -6.0],
    35: [-6.0, -5.5],
    36: [-5.5, -5.0],
    37: [-5.0, -4.5],
    38: [-4.5, -4.0],
    39: [-4.0, -3.5],
    40: [-3.5, -3.0],
    41: [-3.0, -2.5],
    42: [-2.5, -2.0],
    43: [-2.0, -1.5],
    44: [-1.5, -1.0],
    45: [-1.0, -0.5],
    46: [-0.5, 0.0],
    47: [0.0, 0.5],
    48: [0.5, 1.0],
    49: [1.0, 1.5],
    50: [1.5, 2.0],
    51: [2.0, 2.5],
    52: [2.5, 3.0],
    53: [3.0, 3.5],
    54: [3.5, 4.0],
    55: [4.0, 4.5],
    56: [4.5, 5.0],
    57: [5.0, 5.5],
    58: [5.5, 6.0],
    59: [6.0, 6.5],
    60: [6.5, 7.0],
    61: [7.0, 7.5],
    62: [7.5, 8.0],
    63: [8.0, 8.5],
    64: [8.5, 9.0],
    65: [9.0, 9.5],
    66: [9.5, 10.0],
    67: [10.0, 10.5],
    68: [10.5, 11.0],
    69: [11.0, 11.5],
    70: [11.5, 12.0],
    71: [12.0, 12.5],
    72: [12.5, 13.0],
    73: [13.0, 13.5],
    74: [13.5, 14.0],
    75: [14.0, 14.5],
    76: [14.5, 15.0],
    77: [15.0, 15.5],
    78: [15.5, 16.0],
    79: [16.0, 16.5],
    80: [16.5, 17.0],
    81: [17.0, 17.5],
    82: [17.5, 18.0],
    83: [18.0, 18.5],
    84: [18.5, 19.0],
    85: [19.0, 19.5],
    86: [19.5, 20.0],
    87: [20.0, 20.5],
    88: [20.5, 21.0],
    89: [21.0, 21.5],
    90: [21.5, 22.0],
    91: [22.0, 22.5],
    92: [22.5, 23.0],
    93: [23.0, 23.5],
    94: [23.5, 24.0],
    95: [24.0, 24.5],
    96: [24.5, 25.0],
    97: [25.0, 25.5],
    98: [25.5, 26.0],
    99: [26.0, 26.5],
    100: [26.5, 27.0],
    101: [27.0, 27.5],
    102: [27.5, 28.0],
    103: [28.0, 28.5],
    104: [28.5, 29.0],
    105: [29.0, 29.5],
    106: [29.5, 30.0],
    107: [30.0, 30.5],
    108: [30.5, 31.0],
    109: [31.0, 31.5],
    110: [31.5, 32.0],
    111: [32.0, 32.5],
    112: [32.5, 33.0],
    113: [33.0, 33.5],
    114: [33.5, 34.0],
    115: [34.0, 34.5],
    116: [34.5, 35.0],
    117: [35.0, 35.5],
    118: [35.5, 36.0],
    119: [36.0, 36.5],
    120: [36.5, 37.0],
    121: [37.0, 37.5],
    122: [37.5, 38.0],
    123: [38.0, 38.5],
    124: [38.5, 39.0],
    125: [39.0, 39.5],
    126: [39.5, 40.0]
}


def get_reported_value(dbSINR):
    dbSINR = float(dbSINR)
    if dbSINR < -23.0:
        return 0
    elif dbSINR > 40.0:
        return 127
    else:
        for key, value in zip(SINR_and_Report_Mapping.keys(), SINR_and_Report_Mapping.values()):
            if value[0] <= dbSINR <= value[1]:
                return key
            else:
                continue


if __name__ == '__main__':
    c = get_transmit_characteristic(4)
    calculate_TBS(c['min_RBs'], )

