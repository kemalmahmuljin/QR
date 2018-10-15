#> =============================================================================
#>                     This confidential and proprietary code
#>                       may be used only as authorized by a
#>                         licensing agreement from
#>                     KU Leuven, ESAT Department, COSIC Group
#>                    https://securewww.esat.kuleuven.be/cosic/
#>                        _____  ____    ____   ____  _____
#>                       / ___/ / __ \  / __/  /  _/ / ___/
#>                      / /__  / /_/ / _\ \   _/ /  / /__
#>                      \___/  \____/ /___/  /___/  \___/
#>
#>                              ALL RIGHTS RESERVED
#>        The entire notice above must be reproduced on all authorized copies.
#> =============================================================================
#> File name     : utils.py
#> Time created  : Fri Sep 14 14:44:26 2018
#> Author        : dsijacic (dsijacic@esat.kuleuven.be)
#> Details       :
#>               :
#> =============================================================================

def ppBytes(byteArray, bytesPerLine=16, label="B"):
    assert type(byteArray) == bytearray
    s = '< ' + label + '\n'
    i = 0
    for b in byteArray:

        if i > 0 and not (i % bytesPerLine):
            s += '\n'
        s += '{:02x} '.format(b)
        i += 1
    s += '\n \\>'
    print(s)
