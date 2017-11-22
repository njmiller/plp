from __future__ import print_function

import numpy as np
import pandas as pd


# def load_recipe_list_numpy(fn, allow_duplicate_groups=False):
#     dtype = [('OBJNAME', 'S128'), ('OBJTYPE', 'S128'),
#              ('GROUP1', 'S128'), ('GROUP2', 'S128'),
#              ('EXPTIME', 'f'), ('RECIPE', 'S128'),
#              ('OBSIDS', 'S1024'),  ('FRAMETYPES', 'S1024')]
#     d = np.genfromtxt(fn, delimiter=",", names=True, comments="#",
#                       dtype=dtype)
#     recipe_list = []
#     for row in d:
#         recipe_name = row["RECIPE"].strip()
#         obsids = [int(v) for v in row["OBSIDS"].strip().split()]
#         frametypes = row["FRAMETYPES"].strip().split()
#         recipe_list.append((recipe_name, obsids, frametypes, row))

#     return recipe_list


# def load_recipe_list_pandas(fn, allow_duplicate_groups=False):
#     dtypes = [('OBJNAME', 'U128'), ('OBJTYPE', 'U128'),
#               ('GROUP1', 'U128'), ('GROUP2', 'U128'),
#               ('EXPTIME', 'f'), ('RECIPE', 'U128'),
#               ('OBSIDS', 'U1024'),  ('FRAMETYPES', 'U1024')]

#     # names = [_[0] for _ in dtypes]
#     df = pd.read_csv(fn, skiprows=0, dtype=dict(dtypes), comment="#",
#                      escapechar="\\", skipinitialspace=True,
#                      engine="python")

#     update_group1 = True

#     if update_group1:
#         msk = (df["GROUP1"] == "1")
#         s_obsids = [(r.split()[0] if m else g) for r, g, m
#                     in zip(df["OBSIDS"], df["GROUP1"], msk)]

#         if np.any(msk):
#             # print "RECIPE: repacing group1 value of 1 with 1st obsids."
#             # print [s for s, m in zip(s_obsids, msk) if m ]

#             df["GROUP1"] = s_obsids

#     for i, row in df.iterrows():
#         if row["OBJTYPE"] != "TAR":
#             if row["GROUP1"] != row["OBSIDS"].split()[0]:
#                 msg = ("GROUP1 should be identical to "
#                        "1st OBSIDS unless the OBJTYPE is "
#                        "TAR : "
#                        "GROUP1=%s, OBSID[0]=%s")
#                 raise ValueError(msg % (row["GROUP1"],
#                                         row["OBSIDS"].split()[0]))

#     if not allow_duplicate_groups:
#         for i, row in df.groupby(["GROUP1", "RECIPE"]):
#             if len(row) > 1:
#                 msg = "Dupicate group names with same recipe found: "
#                 msg += "GROUP1={} OBJTYPE={}".format(row["GROUP1"],
#                                                      row["RECIPE"])
#                 raise ValueError(msg)

#     d = df.to_records(index=False)

#     # d = np.genfromtxt(fn, delimiter=",", names=True, comments="#",
#     #                   dtype=dtype)
#     recipe_list = []
#     for row in d:
#         recipe_name = row["RECIPE"].strip()
#         obsids = [int(v) for v in row["OBSIDS"].strip().split()]
#         frametypes = row["FRAMETYPES"].strip().split()
#         recipe_list.append((recipe_name, obsids, frametypes, row))

#     return recipe_list


# load_recipe_list = load_recipe_list_pandas


# def make_recipe_dict(recipe_list):
#     recipe_dict = {}
#     for recipe_name, obsids, frametypes, row in recipe_list:
#         _ = (obsids, frametypes, row)
#         recipe_dict.setdefault(recipe_name, []).append(_)
#     return recipe_dict


def get_multi_fnmatch_pattern(fnmatch_list):

    import re
    import fnmatch
    p_list = []
    for fnmatch1 in fnmatch_list:
        p = re.compile(fnmatch.translate(fnmatch1))
        p_list.append(p)

    def p_match(s, p_list=p_list):
        for p in p_list:
            if p.match(s):
                return True
        return False

    return p_match


# class Recipes(object):
#     def __init__(self, fn, allow_duplicate_groups=False):
#         self._fn = fn
#         self.recipe_list = load_recipe_list(fn,
#                                             allow_duplicate_groups)
#         self.recipe_dict = make_recipe_dict(self.recipe_list)

#     def select_multi(self, recipe_names, starting_obsids=None):
#         selected = []
#         for recipe_name in recipe_names:
#             _ = self.select_fnmatch(recipe_name, starting_obsids)
#             selected.extend(_)

#     def select_fnmatch(self, recipe_fnmatch, starting_obsids=None):

#         if isinstance(recipe_fnmatch, str):
#             recipe_fnmatch_list = [recipe_fnmatch]
#         else:
#             recipe_fnmatch_list = recipe_fnmatch

#         p_match = get_multi_fnmatch_pattern(recipe_fnmatch_list)

#         from collections import OrderedDict
#         dict_by_1st_obsid = OrderedDict((recipe_item[1][0], recipe_item)
#                                         for recipe_item in self.recipe_list
#                                         if p_match(recipe_item[0]))

#         if starting_obsids is None:
#             starting_obsids = dict_by_1st_obsid.keys()

#         selected = [dict_by_1st_obsid[s1] for s1 in starting_obsids]

#         return selected

#     def select_fnmatch_by_groups(self, recipe_fnmatch, groups=None):

#         if isinstance(recipe_fnmatch, str):
#             recipe_fnmatch_list = [recipe_fnmatch]
#         else:
#             recipe_fnmatch_list = recipe_fnmatch

#         p_match = get_multi_fnmatch_pattern(recipe_fnmatch_list)

#         _ = []
#         for recipe_item in self.recipe_list:
#             for recipe_name in recipe_item[0].split("|"):
#                 if p_match(recipe_name):
#                     recipe_item_new = (recipe_name, ) + recipe_item[1:]
#                     _.append((recipe_item[-1]["GROUP1"],
#                               recipe_item_new))

#         # from collections import OrderedDict
#         # dict_by_group = OrderedDict(_)

#         if groups is None:
#             selected = [s1[1] for s1 in _]
#         else:
#             selected = [s1[1] for s1 in _ if s1[0] in groups]

#         return selected


# class Recipes2(object):
#     def __init__(self, fn, allow_duplicate_groups=False):
#         self._fn = fn
#         self.recipe_list = load_recipe_list(fn,
#                                             allow_duplicate_groups)

#     # def select_multi(self, recipe_names, starting_obsids=None):
#     #     selected = []
#     #     for recipe_name in recipe_names:
#     #         _ = self.select_fnmatch(recipe_name, starting_obsids)
#     #         selected.extend(_)

#     # def select_fnmatch(self, recipe_fnmatch, starting_obsids=None):

#     #     if isinstance(recipe_fnmatch, str):
#     #         recipe_fnmatch_list = [recipe_fnmatch]
#     #     else:
#     #         recipe_fnmatch_list = recipe_fnmatch

#     #     p_match = get_multi_fnmatch_pattern(recipe_fnmatch_list)

#     #     from collections import OrderedDict
#     #     dict_by_1st_obsid = OrderedDict((recipe_item[1][0], recipe_item)
#     #                                     for recipe_item in self.recipe_list
#     #                                     if p_match(recipe_item[0]))

#     #     if starting_obsids is None:
#     #         starting_obsids = dict_by_1st_obsid.keys()

#     #     selected = [dict_by_1st_obsid[s1] for s1 in starting_obsids]

#     #     return selected

#     def select_fnmatch_by_groups(self, recipe_fnmatch, groups=None):

#         if isinstance(recipe_fnmatch, str):
#             recipe_fnmatch_list = [recipe_fnmatch]
#         else:
#             recipe_fnmatch_list = recipe_fnmatch

#         p_match = get_multi_fnmatch_pattern(recipe_fnmatch_list)

#         _ = []
#         for recipe_item in self.recipe_list:
#             for recipe_name in recipe_item[0].split("|"):
#                 if p_match(recipe_name):
#                     recipe_item_new = (recipe_name, ) + recipe_item[1:]
#                     _.append((recipe_item[-1]["GROUP1"],
#                               recipe_item_new))

#         # from collections import OrderedDict
#         # dict_by_group = OrderedDict(_)

#         if groups is None:
#             selected = [s1[1] for s1 in _]
#         else:
#             selected = [s1[1] for s1 in _ if s1[0] in groups]

#         return selected


# def load_recipe_as_dict_numpy(fn):
#     dtype = [('OBJNAME', 'U128'),
#              ('OBJTYPE', 'U128'),
#              ('GROUP1', 'U128'),
#              ('GROUP2', 'U128'),
#              ('EXPTIME', 'f'),
#              ('RECIPE', 'U128'),
#              ('OBSIDS', 'U1024'),
#              ('FRAMETYPES', 'U1024')]

#     d = np.genfromtxt(fn, delimiter=",", names=True, comments="#",
#                       dtype=dtype)

#     for k in ["RECIPE", "OBJNAME", "OBJTYPE"]:
#         d[k] = [n.strip() for n in d[k]]

#     obsids = [[int(v) for v in row["OBSIDS"].strip().split()] for row in d]
#     frametypes = [row["FRAMETYPES"].strip().split() for row in d]
#     starting_obsids = [o[0] for o in obsids]

#     r = dict(starting_obsid=starting_obsids,
#              objname=d["OBJNAME"],
#              obstype=d["OBJTYPE"],
#              group1=d["GROUP1"],
#              group2=d["GROUP2"],
#              exptime=d["EXPTIME"],
#              recipe=d["RECIPE"],
#              obsids=obsids,
#              frametypes=frametypes)

#     return r


def load_recipe_as_dict(fn):

    dtypes = [('OBJNAME', 'S128'), ('OBJTYPE', 'S128'),
              ('GROUP1', 'S128'), ('GROUP2', 'S128'),
              ('EXPTIME', 'f'), ('RECIPE', 'S128'),
              ('OBSIDS', 'S1024'),  ('FRAMETYPES', 'S1024')]

    df = pd.read_csv(fn, skiprows=0, dtype=dtypes, comment="#",
                     escapechar="\\", skipinitialspace=True)
    d = df.to_records(index=False)

    for k in ["RECIPE", "OBJNAME", "OBJTYPE"]:
        d[k] = [n.strip() for n in d[k]]

    obsids = [[v for v in row["OBSIDS"].strip().split()] for row in d]
    frametypes = [row["FRAMETYPES"].strip().split() for row in d]
    starting_obsids = [o[0] for o in obsids]

    group1 = d["GROUP1"]
    try:
        if np.all(d["GROUP1"].astype("i") == 1):
            group1 = starting_obsids
    except ValueError:
        pass

    r = dict(starting_obsid=starting_obsids,
             objname=d["OBJNAME"],
             obstype=d["OBJTYPE"],
             group1=group1,  # d["GROUP1"],
             group2=d["GROUP2"],
             exptime=d["EXPTIME"],
             recipe=d["RECIPE"],
             obsids=obsids,
             frametypes=frametypes)

    return r


def _check(df, allow_duplicate_groups=False):
    for i, row in df.iterrows():
        if row["obstype"] != "TAR":
            if row["group1"] != row["obsids"][0]:
                msg = ("GROUP1 should be identical to "
                       "1st OBSIDS unless the OBJTYPE is "
                       "TAR : "
                       "GROUP1=%s, OBSID[0]=%s")
                raise ValueError(msg % (row["group1"],
                                        row["obsids"][0]))

    if not allow_duplicate_groups:
        for i, row in df.groupby(["group1", "recipe"]):
            if len(row) > 1:
                msg = ("Dupicate group names with same recipe found: "
                       "GROUP1={} RECIPE={}".format(row["group1"],
                                                    row["recipe"]))
                raise ValueError(msg)


class RecipeLog(pd.DataFrame):
    def __init__(self, fn, allow_duplicate_groups=False):
        d = load_recipe_as_dict(fn)

        columns = ["starting_obsid", "objname", "obstype",
                   "recipe", "obsids", "frametypes",
                   "exptime", "group1", "group2"]
        super(RecipeLog, self).__init__(d, columns=columns)
        # self.set_index("starting_obsid", inplace=True)
        self._substitute_group1()
        _check(self, allow_duplicate_groups)

    def subset(self, **kwargs):
        """
        You can index the data frame by theie values,
        but obsids and frametypes are not allowed as they are inherently list.
        """
        bad_k = [k for k in kwargs.iterkeys()
                 if k in ["obsids", "frametypes"]]

        if bad_k:
            raise ValueError("keyname %s cannot be selected." % bad_k)

        from collections import Iterable

        m_reversed = np.ones(len(self.index), dtype=bool)

        for k, v in kwargs.iteritems():
            if isinstance(v, str):
                m = (self[k] == v)
            elif isinstance(v, Iterable):
                m = self[k].isin(v)
            else:
                m = (self[k] == v)

            m_reversed &= m

        # print m_reversed
        return self.iloc[m_reversed]

    def _substitute_group1(self):
        msk = self["group1"] == "1"
        grp = self["group1"].copy()
        grp[msk] = self["starting_obsid"][msk]
        self["group1"] = grp

    def select_fnmatch_by_groups(self, recipe_fnmatch, groups=None):

        if isinstance(recipe_fnmatch, str):
            recipe_fnmatch_list = [recipe_fnmatch]
        else:
            recipe_fnmatch_list = recipe_fnmatch

        p_match = get_multi_fnmatch_pattern(recipe_fnmatch_list)

        selected = []
        for i, row in self.iterrows():
            for recipe_name in row["recipe"].split("|"):
                if p_match(recipe_name):
                    obsids = map(int, row["obsids"])
                    frames = row["frametypes"]
                    _ = (recipe_name, obsids, frames, row)
                    selected.append(_)
        # from collections import OrderedDict
        # dict_by_group = OrderedDict(_)

        if groups is None:
            pass  # selected = [s1[1] for s1 in selected]
        else:
            groups = map(str, groups)
            selected = [s1 for s1 in selected if s1[-1]["group1"] in groups]

        return selected