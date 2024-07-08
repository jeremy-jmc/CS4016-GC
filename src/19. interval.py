def interval_arithmetic(f, interval):
    import sympy as sp

    # Define the variable and the function
    x = sp.Symbol('x')
    f_expr = sp.sympify(f)

    # Define the interval
    a, b = interval

    # Step 1: Calculate the interval for each term
    terms = f_expr.as_ordered_terms()

    term_intervals = []
    for term in terms:
        # Calculate the interval for each term
        if term.has(x):
            term_diff = term.diff(x)
            term_min = term.subs(x, a)
            term_max = term.subs(x, b)
            if term_diff != 0:
                crit_points = sp.solveset(
                    term_diff, x, domain=sp.Interval(a, b))
                for cp in crit_points:
                    if a <= cp <= b:
                        term_min = min(term_min, term.subs(x, cp))
                        term_max = max(term_max, term.subs(x, cp))
            term_intervals.append([term_min, term_max])
        else:
            term_intervals.append([term, term])

    # Step 2: Sum the intervals
    final_interval = [sum(interval[0] for interval in term_intervals), sum(
        interval[1] for interval in term_intervals)]

    # Display the steps
    print(f"Function: {f_expr}")
    print(f"Interval for x: [{a}, {b}]")
    print("\nStep-by-step interval calculations:")
    for term, interval in zip(terms, term_intervals):
        print(f"Term: {term} -> Interval: [{interval[0]}, {interval[1]}]")
    print(f"\nFinal interval: [{final_interval[0]}, {final_interval[1]}]")

    return final_interval


# Example usage:
f = 'x**2 - 2*x + 1'
interval = [1, 2]

range_of_f = interval_arithmetic(f, interval)
print(
    f"\nThe range of f(x) = {f} when x ∈ [{interval[0]}, {interval[1]}] is: {range_of_f}")
