class SearchService:
    def __init__(self, search_repo):
        self.search_repo = search_repo

    def search(self, db, query: str):
        groups, endpoints = self.search_repo.search_all(db, query or "")
        return {"groups": groups, "endpoints": endpoints}