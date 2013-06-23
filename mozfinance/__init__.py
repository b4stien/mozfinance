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
