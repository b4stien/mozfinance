# -*- coding: utf-8 -*-
"""List of commissions' variables and helpers for commissions
computation.

"""


_COMMISSIONS_VARIABLES = {
    'month': {
        'm_ca': {'attr': 'revenue', 'text': u'Chiffre d\'affaire du mois'},
        'm_mb': {'attr': 'gross_margin', 'text': u'Marge brute du mois'},
        'm_bc': {'attr': 'commission_base', 'text': u'Base de commission du mois'},
    },
    'prestation': {
        'p_tc': {'attr': 'total_cost', 'text': u'Total des coûts de la prestation'},
        'p_m': {'attr': 'margin', 'text': u'Marge de la prestation'},
        'p_pv': {'attr': 'selling_price', 'text': u'Prix de vente de la prestation'},
    }
}


def formula_checker(formula):
    """Return True if a formula is valid, and False otherwise."""
    keys = list()

    for key in _COMMISSIONS_VARIABLES['prestation']:
        keys.append(key)

    for key in _COMMISSIONS_VARIABLES['month']:
        keys.append(key)

    kwargs = {}
    for key in keys:
        kwargs[key] = float(1)

    try:
        formula = str(formula).format(**kwargs)
    except KeyError:
        return False

    try:
        raw_result = eval(formula)
    except (SyntaxError, NameError):
        return False

    try:
        float(raw_result)
    except TypeError:
        return False

    return True
