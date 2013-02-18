def tier_lab_sum(employees):
    """Return the tier lab sum of employees."""
    if employees:
        try:
            # check to see if list contains Employee model
            employees[0].tier_lab
            return sum([e.tier_lab for e in employees])
        except AttributeError:
            print 'AttributeError: tier_lab_sum()'

def tier_lab_balance_check(employees, min_tier):
    """Check to see if the employee tier levels are balanced."""
    if tier_lab_sum(employees) > (min_tier - 4) and tier_lab_sum(
            employees) < (min_tier + 4):
        return True
    else:
        return False