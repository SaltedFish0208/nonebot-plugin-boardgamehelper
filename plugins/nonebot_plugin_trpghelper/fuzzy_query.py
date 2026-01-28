import heapq

from rapidfuzz import fuzz


class FlattenDataProcesser:
    def __init__(self, faqdict: dict) -> None:
        self.data = faqdict
        self.title_list = self._flatten_dict_for_title()
        self.aliases_list = self._group_by_first_aliases()
        self.keywords_list = self._group_by_first_keywords()

    def _flatten_dict_for_title(self) -> list[tuple]:
        flattened_data = []
        for key in self.data:
            title_tuple = key, self.data[key]["title"]
            flattened_data.append(title_tuple)
        return flattened_data

    def _flatten_dict_for_aliases(self) -> list[tuple]:
        flattened_data = []
        for key in self.data:
            aliases_list = [(key, x) for x in self.data[key]["aliases"]]
            flattened_data.extend(aliases_list)
        return flattened_data

    def _flatten_dict_for_keywords(self) -> list[tuple]:
        flattened_data = []
        for key in self.data:
            aliases_list = [(key, x) for x in self.data[key]["keywords"]]
            flattened_data.extend(aliases_list)
        return flattened_data

    def _group_by_first_aliases(self) -> list[list[tuple]]:
        groups = {}
        result = []
        for t in self._flatten_dict_for_aliases():
            key = t[0]
            if key not in groups:
                groups[key] = []
                result.append(groups[key])
            groups[key].append(t)
        return result

    def _group_by_first_keywords(self) -> list[list[tuple]]:
        groups = {}
        result = []
        for t in self._flatten_dict_for_keywords():
            key = t[0]
            if key not in groups:
                groups[key] = []
                result.append(groups[key])
            groups[key].append(t)
        return result

def fuzzy_score(
        query: str,
        title: tuple,
        aliases: list[tuple],
        ) -> int:
    title_score: float = fuzz.ratio(query.lower(), title[1].lower())
    aliases_score: float = 0.0
    keywords_score: float = 0.0
    aliases_rounds = 0
    for aliases_rounds_tmp, i in enumerate(aliases):
        tmp = fuzz.ratio(query.lower(), i[1].lower())
        aliases_score = aliases_score + tmp
        aliases_rounds = aliases_rounds_tmp
        tmp = fuzz.partial_ratio(query.lower(), i[1].lower())
        keywords_score = keywords_score + tmp
    return int(
        title_score+(aliases_score/aliases_rounds*0.8)
        )

def the_chosen_one(query: str, faqdata: dict) -> tuple[str, int]:
    data = FlattenDataProcesser(faqdata)
    the_chosen = {}
    for x,y in zip(data.title_list, data.aliases_list):
        the_chosen[x[0]] = fuzzy_score(query, x, y)
    return max(
        the_chosen.items(),
        key=lambda item: item[1]
    )

def the_chosen_five(query: str, faqdata:dict) -> list[tuple[str, int]]:
    data = FlattenDataProcesser(faqdata)
    the_chosen = {}
    for x,y in zip(data.title_list, data.aliases_list):
        the_chosen[x[0]] = fuzzy_score(query, x, y)
    return heapq.nlargest(
        5,
        the_chosen,
        key=lambda k: the_chosen[k]
    )
