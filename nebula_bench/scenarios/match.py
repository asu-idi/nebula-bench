# -*- encoding: utf-8 -*-
from nebula_bench.common.base import BaseScenario


class BaseMatchScenario(BaseScenario):
    abstract = True
    nGQL = "MATCH ()<-[e]-() RETURN e LIMIT 300;"
    csv_path = "social_network/dynamic/person_knows_person.csv"
    csv_index = [0]


class MatchAllEdge(BaseMatchScenario):
    abstract = False
    nGQL = "MATCH ()<-[e]-() RETURN e LIMIT 300;"


class MatchVertex(BaseMatchScenario):
    abstract = False
    nGQL = "MATCH (v) WHERE id(v) == {}  RETURN v;"
