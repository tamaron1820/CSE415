def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    Perfect shuffle means splitting a list into two halves and then interleaving
    them. For example, the perfect shuffle of [0, 1, 2, 3, 4, 5, 6, 7] is
    [0, 4, 1, 5, 2, 6, 3, 7]."""
    a = len(even_list)
    half = a//2
    b=even_list[:half]
    c=even_list[half:]
    d=[]
    for i in range(0,a):
        d.append(b[i])
        d.append(c[i])
    return d   