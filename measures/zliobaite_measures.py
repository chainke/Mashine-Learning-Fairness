

def elift(outcomes, protected):
    """
        Calculates elift ratio for given data set.
        Similar to impact ratio, but does not divide by general group in denominator.

        Parameters
        ----------
        outcomes: list of int
                  Either 0 or 1

        protected: list of int
                   Either 0 or 1

        Returns
        -------
        r : float
            measure of discrimination

    """

    assert (len(outcomes) > outcomes.count(0) + outcomes.count(1), "Outcomes must only contain the values 0 or 1")
    assert (len(protected) > protected.count(0) + protected.count(1), "Protected must only contain the values 0 or 1")
    assert (len(outcomes) == len(protected), "Outcomes and Protected have to be the same length")

    n = len(outcomes)

    joined = []
    for i in range(n):
        joined.append((outcomes[i], protected[i]))

    p_pos_0 = joined.count((1, 0)) / n
    p_pos = outcomes.count(1) / n

    return p_pos_0 / p_pos


def odds_ratio(outcomes, protected):
    """
        Calculates odds ratio for given data set.
        Used to measure association between exposure and outcome.

        Parameters
        ----------
        outcomes: list of int
                  Either 0 or 1

        protected: list of int
                   Either 0 or 1

        Returns
        -------
        r : float
            measure of discrimination

    """

    assert (len(outcomes) > outcomes.count(0) + outcomes.count(1), "Outcomes must only contain the values 0 or 1")
    assert (len(protected) > protected.count(0) + protected.count(1), "Protected must only contain the values 0 or 1")
    assert (len(outcomes) == len(protected), "Outcomes and Protected have to be the same length")

    n = len(outcomes)

    joined = []
    for i in range(n):
        joined.append((outcomes[i], protected[i]))

    p_pos_0 = joined.count((1, 0)) / n # Anzahl outcomes[i] = 1 und protected[i] = 0 / n
    p_pos_1 = joined.count((1, 1)) / n
    p_neg_0 = joined.count((0, 0)) / n
    p_neg_1 = joined.count((0, 1)) / n

    return (p_pos_0 * p_neg_1) / (p_pos_1 * p_neg_0)


def impact_ratio(outcomes, protected):
    """
        Calculates impact ratio(also called slift) for given data set.
        Ratio of positive outcomes for the protected group over the general group.

        Parameters
        ----------
        outcomes: list of int
                  Either 0 or 1

        protected: list of int
                   Either 0 or 1

        Returns
        -------
        r : float
            measure of discrimination

    """

    assert (len(outcomes) > outcomes.count(0) + outcomes.count(1), "Outcomes must only contain the values 0 or 1")
    assert (len(protected) > protected.count(0) + protected.count(1), "Protected must only contain the values 0 or 1")
    assert (len(outcomes) == len(protected), "Outcomes and Protected have to be the same length")

    n = len(outcomes)

    joined = []
    for i in range(n):
        joined.append((outcomes[i], protected[i]))

    p_pos_0 = joined.count((1, 0)) / n
    p_pos_1 = joined.count((1, 1)) / n

    return p_pos_1 / p_pos_0