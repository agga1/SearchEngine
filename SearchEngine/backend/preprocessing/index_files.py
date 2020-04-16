from time import perf_counter

from SearchEngine.backend.classes.Article import Article
from SearchEngine.backend.classes.SearchStruct import SearchStruct


def index_files(art_count=1000) -> SearchStruct:
    """
    Converts input data (1 txt file) to SearchStruct
    :param art_count: only first max_count articles will be processed
    """
    tstart = perf_counter()
    articles = articles_from_dbArticles(art_count)
    print(f"{len(articles)} articles processed")
    SS = SearchStruct(articles)
    tend = perf_counter()
    print(f"indexing process took {tend-tstart} seconds")
    return SS


def articles_from_dbArticles(art_count=1000) -> list:
    from search.models import Article as dbArticle
    articles = []
    cnt = 0
    for art in dbArticle.objects.all():
        articles.append(Article(title=art.title, text=art.content, id=art.id))
        cnt+=1
        if art_count <=cnt:
            break
    return articles
