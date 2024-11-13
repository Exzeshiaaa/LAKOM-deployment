# https://github.com/kevinzg/facebook-scraper
import facebook_scraper as fs

import locale

from datetime import datetime

def scrape(link):
    """
    Download comments for a public Facebook post.
    """

    locale.setlocale(locale.LC_ALL, 'en_US')

    # get the post (this gives a generator)
    gen = fs.get_posts(
        post_urls=[link],
    )

    # take 1st element of the generator which is the post we requested
    post = next(gen)

    date = "None"
    if post.get("time"):
        date = post.get("time").strftime('%d %b %Y')

    status = "Unavailable"
    if post.get("available"):
        status = "Available"

    return {
        "Link to Disinformative Content" : post.get("post_url"),
        'Date of Submission' : datetime.now().strftime('%d %b %Y'),
        "Summary" : post.get("text"),
        "Date Posted" : date,
        "Likes" : post.get("likes"),
        "Comments" : post.get("comments"),  # not included
        "Shares" : post.get("shares"),  # not included
        "Account Name" : post.get("username"),
        "Account URL" : post.get("user_url"), # not included
        "Platform" : "Facebook",
        "Status of the Post" : status,
    }
# https://www.facebook.com/ActionAviationChairman/posts/i-am-proud-to-finally-announce-that-i-joined-oceangate-expeditions-for-their-rms/674126021392828/
# https://www.facebook.com/story.php?story_fbid=2257188721032235&id=119240841493711

if __name__ == "__main__":
    print(scrape('https://www.facebook.com/ActionAviationChairman/posts/i-am-proud-to-finally-announce-that-i-joined-oceangate-expeditions-for-their-rms/674126021392828/'))