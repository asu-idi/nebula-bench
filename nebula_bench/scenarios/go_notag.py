# -*- encoding: utf-8 -*-
from nebula_bench.common.base import BaseScenario


class BaseGoScenario(BaseScenario):
    abstract = True
    nGQL = "GO 1 STEP FROM {} OVER KNOWS YIELD properties($$).firstName"
    csv_path = "social_network/dynamic/person.csv"
    csv_index = [0]


class Go1Step_NoTag(BaseGoScenario):
    abstract = False
    nGQL = "GO 1 STEP FROM {} OVER KNOWS YIELD properties($$).firstName"


class Go2Step_NoTag(BaseGoScenario):
    abstract = False
    nGQL = "GO 2 STEP FROM {} OVER KNOWS YIELD properties($$).firstName"


class Go3Step_NoTag(BaseGoScenario):
    abstract = False
    nGQL = "GO 3 STEP FROM {} OVER KNOWS YIELD properties($$).firstName"
