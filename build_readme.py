import os
import pathlib
import json
import requests
from dateutil import parser


def send_request(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except Exception as exc:
        print('Generated an exception: %s' % exc)
        return -1, exc

    return 0, res.text


def string_2_markdown(data):
    temp_data = data
    temp_data = temp_data.replace('[', '\[')
    temp_data = temp_data.replace(']', '\]')
    return temp_data


def parse_blog_content(post_dict):
    posts_output = ''
    for post in post_dict['items']:
        post_title = string_2_markdown(post['title'])
        post_url = post['url']
        post_date = parser.parse(post['updated'])
        posts_output += '* [' + post_title +'](' + post_url + ') - ' + post_date.strftime("%Y-%m-%d") + '\n'

    return posts_output


def gen_blog_content():
    blog_basic_url = 'https://www.googleapis.com/blogger/v3/blogs/'
    blog_post_id = os.environ.get("BLOG_POST_ID", "")
    blog_api_key = os.environ.get("BLOG_API_KEY", "")

    query_url = blog_basic_url + blog_post_id + '/posts?key=' + blog_api_key

    ret, content = send_request(query_url)

    if ret == 0:
        try:
            return parse_blog_content(json.loads(content))

        except Exception as exc:
            print('Generated an exception: %s' % exc)

    return 'Service Temporarily Unavailable'


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.resolve()
    readme_path = root / "README.md"
    readme_basic_path = root / "README-basic.md"

    output = ""
    with open(readme_basic_path, 'r', encoding='utf-8') as f:
        output = f.read().replace('{blog content}', gen_blog_content())

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(output)
