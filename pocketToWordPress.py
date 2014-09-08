import ConfigParser
import pocket
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

Config = ConfigParser.ConfigParser()
Config.read('./setting.ini')

POCKET_CONSUME_KEY = Config.get('pocket', 'POCKET_CONSUME_KEY')
POCKET_ACCESS_TOKEN = Config.get('pocket', 'POCKET_ACCESS_TOKEN')

WP_XMLRPC_URL = Config.get('wordpress', 'WP_XMLRPC_URL')
WP_USER = Config.get('wordpress', 'WP_USER')
WP_PASSWORD = Config.get('wordpress', 'WP_PASSWORD')

def main():
    pocket_instance = pocket.Pocket(POCKET_CONSUME_KEY, POCKET_ACCESS_TOKEN)
    response, headers = pocket_instance.get(favorite=1,
                                            state='archive',
                                            detailType='complete')
    items = response['list'].items()
    print 'pocket list getted'
    wp = Client(WP_XMLRPC_URL, WP_USER, WP_PASSWORD)
    print wp.call(GetUserInfo())
    print 'wordpress connected'

    for key,values in items[:3]:
        post = WordPressPost()
        post.title = values['resolved_title']
        post.link = values['given_url']
        url = values['given_url']
        url = 'Read More:<a href="%s">%s</a>' % (url, url)
        if values.has_key('excerpt'):
            post.content = url  + "\n\r" + values['excerpt'] + "\n\r" + url
        else:
            post.content = url

        if values.has_key('tags'):
            tags = values['tags'].keys()
            post.terms_names = {
                'post_tag': tags,
                'category': ['Pocket']
                }
        else:
            post.terms_names = {
                'category': ['Pocket']
            }

        print key
        post.post_status = 'publish'
        wp.call(NewPost(post))


if __name__ == '__main__':
        main()
