def formula_checker(formula):
    """Check if a formula is valid.

    The complete list of available variables is in warfinance.business.compute,
    in the _get_prestation_commission_params method's body.

    """
    kwargs = {
        'm_ca': float(1),
        'm_mb': float(1),
        'm_bc': float(1),
        'm_tc': float(1),
        'm_ff': float(1),
        'p_c': float(1),
        'p_m': float(1),
        'p_pv': float(1)
    }

    try:
        formula = str(formula).format(**kwargs)
    except KeyError:
        return False

    try:
        bla = eval(formula)
    except (SyntaxError, NameError):
        return False

    try:
        float(bla)
    except TypeError:
        return False

    return True
