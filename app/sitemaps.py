from django.contrib.sitemaps import Sitemap
from django.urls import get_resolver, reverse, URLPattern, URLResolver

class StaticViewSitemap(Sitemap):
    def items(self):
        # Recursively retrieve named URL patterns, filtering out Django's built-in URLs and those with arguments
        return self._get_named_urls(get_resolver().url_patterns)

    def _get_named_urls(self, url_patterns):
        items = []
        for pattern in url_patterns:
            if isinstance(pattern, URLPattern) and pattern.name:
                # Check if the URL belongs to your app and does not require arguments
                if self._is_custom_url(pattern) and not pattern.pattern.converters:
                    items.append(pattern.name)
            elif isinstance(pattern, URLResolver):
                # If it's an included URL resolver, recursively search it
                items.extend(self._get_named_urls(pattern.url_patterns))
        return items

    def _is_custom_url(self, pattern):
        # Filter out URLs that don't belong to your custom apps
        module_name = pattern.callback.__module__
        return 'website' in module_name

    def location(self, item):
        # Reverse the URL using its name
        return reverse(item)
