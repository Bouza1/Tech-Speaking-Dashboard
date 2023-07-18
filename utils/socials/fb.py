import facebook
import json

# page_id = "107998422360738"
# token = "EAALfLopwdeYBAHjhlsZBaLeoOFzhfYZByZCC7tmNIGh9327ZAKq259Lp11D4Y3R1zrKsWUhd8oDOg1RxyiYN2Vf4achOJBXAXm6n2dB3x5Qanafixp56VeQyCKHTO2ZBxeq4OmDPVGnmdLZCsrlJttC7RBiAWevj0ZCr1nAThkePAWW8hZBZBHSPA5kGWesR7OZAEZD"

def post_2_fb(token, page_id, article):
    graph = facebook.GraphAPI(token)
    livelink = "https://techspeaking.s4820791.repl.co/news/article/" + str(article['id'])
    message = graph.put_object(parent_object =page_id, connection_name="feed", message=article['title'] + "\n \n" + "this ia test", link=livelink)
    if message:
        return json.dumps(message, indent=4)
    else:
        return False
