from gemeaux import App, Handler, Response
import requests
import os
from markdownify import markdownify
from md2gemini import md2gemini

API_KEY = os.getenv("GHOST_CONTENT_API_KEY")
API_URL = os.getenv("GHOST_CONTENT_API_URL")



all_posts = requests.get(f"{API_URL}/posts/?key={API_KEY}&include=tags&limit=all").json()
print(f"loaded {len(all_posts['posts'])} ghost blogposts")

class GeminiResponse(Response):
    """
    Gemini response
    This reponse is the content of a gemini document.
    """
    def __init__(self, content):
        self.content = content
        self.mimetype = "text/gemini"
        self.status = 20 # success

    def __meta__(self):
        meta = f"{self.status} {self.mimetype}"
        return bytes(meta, encoding="utf-8")

    def __body__(self):
        return self.content

class GhostHandler(Handler):
    def get_response(self, url, path):
        # / -> list all posts
        # /<slug> -> post content

        # path cleanup
        if path.startswith(url):
            path = path[len(url) :]
        if path.startswith("/"):  # Should be a relative path
            path = path[1:]

        # TODO dir listing

        # find post w/ slug matching path
        matching_post = next((x for x in all_posts["posts"] if x["slug"]==path), None)
        if matching_post:
            document = md2gemini(markdownify(matching_post["html"]))
            return GeminiResponse(document)


        raise FileNotFoundError("Path not found")

if __name__ == "__main__":
    urls = {
        "": GhostHandler()
    }
    app = App(urls)
    app.run()
