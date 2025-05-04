from django.contrib.sitemaps import Sitemap

from women.models import Women


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Women.published.all()

    def lastmod(self, item):
        return item.time_update
