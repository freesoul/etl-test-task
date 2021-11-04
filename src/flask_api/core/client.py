import elasticsearch


class CommunesClient:
    def __init__(self, es_host: str):
        self.es_host = es_host
        self.es = elasticsearch.Elasticsearch(
            [
                {"host": es_host},
            ],
            timeout=300,
        )
        self.error = None

    def getCommunes(self, commune: str = None, include_rents: bool = True):
        self.error = None
        if not self._check_exists():
            return False

        # Retrieve communes indexed by their name
        filters = []
        if commune:
            filters.append({"match_phrase": {"commune": commune}})
        query_body = {
            "bool": {
                "must": filters,
            },
        }
        search_result = self.es.search(index="communes", query=query_body, size=2000)
        try:
            communes = {result["_source"]["commune"]: result["_source"] for result in search_result["hits"]["hits"]}
        except KeyError:
            communes = {}

        # Retrieve the rental prices and merge them.
        if len(communes) > 0 and include_rents:
            filters = []
            if commune:
                filters.append({"match_phrase": {"commune": commune}})
            query_body = {
                "bool": {
                    "must": filters,
                },
            }
            search_result = self.es.search(index="communes_rentals", query=query_body, size=2000)
            try:
                communes_rentals = [result["_source"] for result in search_result["hits"]["hits"]]
            except KeyError:
                communes_rentals = []

            for commune_rental in communes_rentals:
                if commune_rental["commune"] not in communes.keys():
                    continue
                if "price_rents" not in communes[commune_rental["commune"]]:
                    communes[commune_rental["commune"]]["price_rents"] = {}
                communes[commune_rental["commune"]]["price_rents"][commune_rental["year"]] = {
                    k: v for k, v in commune_rental.items() if k != "year" and k != "commune"
                }
        return list(communes.values())

    def _check_exists(self):
        existing_indices = list(self.es.indices.get_alias("*").keys())
        for name in ["communes", "communes_rentals"]:
            if name not in existing_indices:
                self.error = "Indexes do not exist. Call the download-and-insert route."
                return False
        return True

    def getError(self):
        return self.error


if __name__ == "__main__":

    client = CommunesClient("localhost")

    result = client.getCommunes(commune="Wormeldange")

    print(result)