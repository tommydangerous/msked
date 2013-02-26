def tier_lab_sum(employees):
    """Return the tier lab sum of employees."""
    if employees:
        try:
            # check to see if list contains Employee model
            employees[0].tier_lab
            return sum([e.tier_lab for e in employees])
        except AttributeError:
            print 'AttributeError: tier_lab_sum()'

def tier_balance(first, second):
    """Check to see if the employee tier levels are balanced."""
    print ('-' * 10) + ' Tier Balance ' + ('-' * 10)
    var   = (len(first) + len(second))/5
    ratio = len(first)/float(len(second))
    f_sum = tier_lab_sum(first)
    s_sum = tier_lab_sum(second)
    mtier = s_sum * ratio
    print 'First Tier: %s, Second Tier: %s, Ratio: %s' % (f_sum, s_sum, ratio)
    if f_sum >= mtier - var and f_sum <= mtier + var:
        return True