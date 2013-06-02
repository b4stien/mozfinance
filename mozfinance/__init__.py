# -*- coding: utf-8 -*-
"""Package to manage finances of a prestation-based business."""

# Array of monthly bonuses methods. These methods will be given all
# monthly params, and must return a float.
#
# Example usage:
#     def bonus_net_margin(**kwargs):
#         if kwargs['m_bc'] >= float(10000):
#             return 0.02*kwargs['m_bc']
#         return float(0)
#
#     COMMISSIONS_BONUSES.append(bonus_net_margin)

COMMISSIONS_BONUSES = []

# Array of filters that will be applied to all prestation queries.
# Useful if mozfinance must consider only certain prestations.
#
# Example usage:
#     PRESTATIONS_FILTERS.append(Prestation.status == 'Done')

PRESTATIONS_FILTERS = []


# Internal dictonary for additional variables on objects.

_ATTRIBUTES_DICT = {
    'month': {
        'revenue': 'month_revenue',
        'gross_margin': 'month_gross_margin',
        'commission_base': 'month_commission_base',
        'net_margin': 'month_net_margin',
        'total_cost': 'month_total_cost',
        'salesmen_com': 'month_salesmen_com'
    },
    'prestation': {
        'cost': 'prestation_cost',
        'margin': 'prestation_margin',
        'salesmen_com': 'prestation_salesmen_com'
    },
    'year': {
        'revenue': 'year_revenue',
        'gross_margin': 'year_gross_margin',
        'net_margin': 'year_net_margin'
    }
}
