import hashlib
import base64

class URLShortener:
    def __init__(self):
        self.url_map = {}  # Long to short URL mapping
        self.short_map = {}  # Short to long URL mapping
        self.base_url = "https://short.ly/"  # Base domain


    def _generate_short_code(self, long_url):
        """Generates a unique 6-character short URL code."""
        # Generate hash for the URL
        hash_object = hashlib.md5(long_url.encode())
        # Encode hash as base64, take first 8 chars
        short_code = base64.urlsafe_b64encode(hash_object.digest())[:8].decode()
        return short_code


    def shorten(self, long_url):
        """Shortens a URL and returns the short version."""
        if long_url in self.url_map:
            return self.base_url + self.url_map[long_url]

        short_code = self._generate_short_code(long_url)
        # while short_code in self.short_map:  # Ensure uniqueness
        #     short_code = self._generate_short_code(long_url)

        self.url_map[long_url] = short_code
        self.short_map[short_code] = long_url
        return self.base_url + short_code


    def expand(self, short_url):
        """Expands a short URL back to the original."""
        short_code = short_url.replace(self.base_url, "")
        return self.short_map.get(short_code, "URL not found")
        
        
    def retrieve_url_from_short_url(short_url):
        # Example: http://short.en/z-tkkp -> extract 'z-tkkp'
        short_code = short_url.rstrip('/').split('/')[-1]
        # Fetch original URL from mapping
        return url_mapping.get(short_code, "Not found")





# Example usage
if __name__ == "__main__":
    shortener = URLShortener()
    short_url = shortener.shorten("https://sonam-portfolio-three.vercel.app/")
    print("Short URL:", short_url)
    print("Expanded URL:", shortener.expand(short_url))
