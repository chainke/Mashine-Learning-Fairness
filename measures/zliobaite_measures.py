from sklearn.neighbors import KNeighborsClassifier

#######################
# absolute measures
#######################

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

    return 0 if p_pos == 0 else p_pos_0 / p_pos
    #return p_pos_0 / p_pos


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

    #return (p_pos_0 * p_neg_1) / (p_pos_1 * p_neg_0)
    return 0 if (p_pos_1 * p_neg_0) == 0 else (p_pos_0 * p_neg_1) / (p_pos_1 * p_neg_0)

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

    return 0 if p_pos_0 == 0 else p_pos_1 / p_pos_0
    #return p_pos_1 / p_pos_0


def mean_difference(outcomes, protected):
    """
        Measures the difference between the means of the targets of the protected group and the general group.
        If there is no difference, then there is no discrimination.

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

    return p_pos_0 - p_pos_1



def normalized_difference(outcomes, protected):
    """
        Measures the mean difference normalized by the rate of positive outcomes.

        Parameters
        ----------
        outcomes: list of int
                  Either 0 or 1

        protected: list of int
                   Either 0 or 1

        Returns
        -------
        r : float
            measure of discrimination. 1 = max discrimination, 0 = no discrimination

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

    p_pos = outcomes.count(1) / n
    p_neg = outcomes.count(0) / n
    p_s1 = protected.count(1) / n
    p_s0 = protected.count(0) / n

    dmax = min((p_pos / p_s0),(p_neg / p_s1))

    return 0 if dmax == 0 else (p_pos_0 - p_pos_1) / dmax
    #return (p_pos_0 - p_pos_1) / dmax


#######################
# conditional measures
#######################

def unexplained_difference(outcomes, protected, stratum):
    """
        Measures the mean difference minus the difference that can be explained.

        Parameters
        ----------
        outcomes: list of int
                  Either 0 or 1

        protected: list of int
                   Either 0 or 1

        Returns
        -------
        r : float
            measure of discrimination. 

    """

    assert (len(outcomes) > outcomes.count(0) + outcomes.count(1), "Outcomes must only contain the values 0 or 1")
    assert (len(protected) > protected.count(0) + protected.count(1), "Protected must only contain the values 0 or 1")
    assert (len(outcomes) == len(protected), "Outcomes and Protected have to be the same length")
    assert (len(protected) == len(stratum), "Protected and Stratum have to be the same length")

    n = len(outcomes)

    joined_stratum_protected = []
    for i in range(n):
        joined_stratum_protected.append((stratum[i], protected[i]))

    joined_outcomes_protected_stratum = []
    for i in range(n):
        joined_outcomes_protected_stratum.append((outcomes[i], protected[i], stratum[i]))


    de = 0
    for i in range(n):
        count_strato_neg = joined_stratum_protected.count(stratum[i], 0)
        count_strato_pos = joined_stratum_protected.count(stratum[i], 1)

        p_strato_neg = count_strato_neg / n
        p_strato_pos = count_strato_pos / n

        # p_star is the desired acceptance rate within strata i
        p_star = ((joined_outcomes_protected_stratum.count(1, 0, stratum[i]) / count_strato_neg) + (joined_outcomes_protected_stratum.count(1, 1, stratum[i]) / p_strato_pos)) / 2

        # the explained difference
        de += p_star * (p_strato_neg - p_strato_pos)

    du = mean_difference(outcomes, protected) - de

    return du


#######################
# Situation measures
#######################

def situation_testing(outcomes, protected, individuals, t, k):
    """
        Measures which fraction of individuals in the protected group are considered to be discriminated against.
        Positive and negative discrimination is handled separately.
        Compares each individual to the opposite group and see if the decision would be different. With this, it
        signals direct discrimination for each individual.

        Parameters
        ----------
        outcomes: list of int
                  Either 0 or 1

        protected: list of int
                   Either 0 or 1
                   all individuals of the protected group

        individuals: list of feature-vectors?
                     contains all individuals

        t: int
           threshold of maximum tolerable difference

        k: int
           nearest neighbours

        Returns
        -------
        r : int
            either 0 or 1 ??
            is discriminated or not

    """
    
    # estimate D(s¹)
    d_protected_pos = [] # contains all s¹
    d_outcome_pos = [] # contains all y|s¹
    d_individuals_pos = [] # contains all u|s¹
    for i in range(protected):
        if(protected[i] == 1):
            d_protected_pos.append(protected[i])
            d_outcome_pos.append(outcome[i])
            d_individuals_pos.append(individuals[i])


    # absolute value of individuals in D(s¹)
    abs_d_pos = len(d_protected_pos)

    # estimate D(s⁰)
    d_outcome_neg = [] # contains all y|s⁰
    d_individuals_neg = [] # contains all u|s⁰
    for i in range(protected):
        if(protected[i] == 0):
            d_outcome_neg.append(outcome[i])
            d_individuals_neg.append(individuals[i])

    # setup knn
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(individuals, outcomes)
    neighbor_indices = [] # contains the indices of all found neighbors

    # sum over all individuals u in D(s¹)
    i_res = 0 # the result of the summed indicator function results
    diff_d_pos = 0 # the result of the summed labels for the neighbours of u with s¹
    diff_d_neg = 0 # the result of the summed labels for the neighbours of u with s⁰
    for u in d_protected_pos:
        # estimate diff_d_pos:
        # find y of the k nearest neighbours of u in d_individuals_pos     
        neighbor_indices = knn.kneighbors(d_individuals_pos, k, false)
        for i in neighbor_indices:
            diff_d_pos += d_outcome_pos[i]

        # estimate diff_d_neg:
        # find y of the k nearest neighbours of u in d_individuals_neg
        neighbor_indices = knn.kneighbors(d_individuals_neg, k, false)
        for i in neighbor_indices:
            diff_d_neg += d_outcome_neg[i]

        diff_d_pos = diff_d_pos / k
        diff_d_neg = diff_d_neg / k

        # sum up results of indicator function
        i_res += indicator_situation_testing((diff_d_neg - diff_d_pos) >= t)

    return i_res / abs_d_pos



def indicator_situation_testing(b):
    """
        Indicator function that takes 1 if true, 0 otherwise.


        Parameters
        ----------
        b: true or false


        Returns
        -------
        i : int
            1 if true, 0 otherwise

    """

    if(b):
        return 1
    else:
        return 0



