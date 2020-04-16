from time import perf_counter
import concurrent.futures

from SearchEngine.backend.classes.Article import Article
from SearchEngine.backend.classes.SearchStruct import SearchStruct


def index_files(art_count=1000) -> SearchStruct:
    """
    indexes (maximum) @art_count articles from database
    :return: SearchStruct to preform searches by queries
    """
    tstart = perf_counter()
    articles = articles_from_dbArticles(art_count)
    print(f"{len(articles)} articles processed")
    SS = SearchStruct(articles)
    tend = perf_counter()
    print(f"indexing process took {tend - tstart} seconds")
    return SS


def articles_from_dbArticles(art_count=1000) -> list:
    """
    prepares articles for indexing, using concurrency for faster indexing
    :param art_count: (maximum) number of articles from db to be indexed
    :return: processed articles, ready to be processed by Search Struct
    """
    from search.models import Article as dbArticle
    dbArticles = dbArticle.objects.all() if dbArticle.objects.count() <= art_count else dbArticle.objects.all()[:art_count]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        articles = list(executor.map(lambda a: Article(title=a.title, text=a.content, id=a.id), dbArticles))
    return articles
