def parents_and_children(all_posts):
    """
    Given a list of raw posts from the DB, return a dictionary where the keys are thread posts and
    their values are all of the thread replies.
    >>> parents_and_children([
    ...     {'parent': None, "id": 1}, # thread, because parent=null
    ...     {'parent': 1, "id": 2},    # reply, because parent references another post
    ...     {'parent': None, "id": 3},
    ...     {'parent': 1, "id": 4},
    ... ])
    {1: [2, 4], 3: []}
    """
    result = {}
    for post in all_posts:
        if post["parent"] is None:
            result[post["id"]] = []
        else:
            if not result.get(post["parent"], None):
                result[post["parent"]] = []
            result[post["parent"]].append(post["id"])
    return result