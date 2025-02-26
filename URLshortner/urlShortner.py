"""
#  URL Shortener (Base62 Encoding)
Key Concept: Convert long URLs into short ones using Base62 encoding.
Use Case: URL shortening (bit.ly, tinyurl).
"""

import random
import string

class URLShortener:
    def __init__(self):
        self.url_map = {}  # Long to short URL mapping
        self.short_map = {}  # Short to long URL mapping
        self.base_url = "https://short.ly/"  # Base domain

    def _generate_short_code(self):
        """Generates a unique 6-character short URL code."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def shorten(self, long_url):
        """Shortens a URL and returns the short version."""
        if long_url in self.url_map:
            return self.base_url + self.url_map[long_url]

        short_code = self._generate_short_code()
        while short_code in self.short_map:  # Ensure uniqueness
            short_code = self._generate_short_code()

        self.url_map[long_url] = short_code
        self.short_map[short_code] = long_url
        return self.base_url + short_code

    def expand(self, short_url):
        """Expands a short URL back to the original."""
        short_code = short_url.replace(self.base_url, "")
        return self.short_map.get(short_code, "URL not found")

# Usage
shortener = URLShortener()
short_url = shortener.shorten("https://sonam-portfolio-three.vercel.app/")
print("Short URL:", short_url)
print("Expanded URL:", shortener.expand(short_url))
