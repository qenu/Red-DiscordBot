import yaml


def test_trivia_lists():
    from redbot.cogs.trivia import get_core_lists

    list_names = get_core_lists()
    assert list_names
    problem_lists = []
    for lis in list_names:
        with lis.open(encoding="utf-8") as f:
            try:
                dict_ = yaml.safe_load(f)
            except yaml.error.YAMLError as e:
                problem_lists.append((lis.stem, "YAML error:\n{!s}".format(e)))
            else:
                for key in list(dict_.keys()):
                    if key == "CONFIG":
                        if not isinstance(dict_[key], dict):
                            problem_lists.append((lis.stem, "CONFIG is not a dict"))
                    elif key == "AUTHOR":
                        if not isinstance(dict_[key], str):
                            problem_lists.append((lis.stem, "AUTHOR is not a string"))
                    else:
                        if not isinstance(dict_[key], list):
                            problem_lists.append(
                                (lis.stem, "The answers for '{}' are not a list".format(key))
                            )
    if problem_lists:
        msg = ""
        for lis in problem_lists:
            msg += "{}: {}\n".format(lis[0], lis[1])
        raise TypeError("The following lists contain errors:\n" + msg)
