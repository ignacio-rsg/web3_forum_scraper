import csv, requests, sources
#from os import _AddedDllDirectory
from bs4 import BeautifulSoup
from operator import itemgetter


#Function to parse forums
def scrape(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        td_tags = soup.find_all("td")
        
        #item
        item=[]
        
        #list of items
        items_list=[]
        
        for td in td_tags:
            anchors = td.find(class_="title raw-link raw-topic-link")
            title=""
            href=""
            views = td.find(class_="views")
            replies = td.find(class_="posts")
            
            if anchors != None:
                title = anchors.get_text()
                href = td.find("a")["href"]    
            
                if title != "":
                    item.append(title)
                    item.append(href)
                    
            if replies != None:
                item.append(int(replies.get_text()))
                
            if views != None:
                item.append(int(views.get_text()))
                items_list.append(item)
                item=[]
                
        return items_list
    except:
        return f"{url} seems to be down" 


#function to find the top proposals in defi
def hot_in_defi():
    defi_ecosystem = sources.governance_urls
    all_posts_and_views = []
    for k,v in defi_ecosystem.items():
        data = scrape(v)
        recent_5 = list(data)[:5]
        all_posts_and_views.extend(recent_5)
        
    getcount_views= key=itemgetter(3)
    list(map(getcount_views, all_posts_and_views))
    top_views = sorted(all_posts_and_views, key=getcount_views,reverse=True)
    
    getcount_posts= key=itemgetter(2)
    list(map(getcount_posts, all_posts_and_views))
    top_posts = sorted(all_posts_and_views, key=getcount_posts,reverse=True)
    #print([[top_views[0],top_views[1],top_views[2],top_views[3],top_views[4]],[top_posts[0],top_posts[1],top_posts[2],top_posts[3],top_posts[4]]])
    return [[top_views[0],top_views[1],top_views[2],top_views[3],top_views[4]],[top_posts[0],top_posts[1],top_posts[2],top_posts[3],top_posts[4]]]
    

def parse_defi():
    defi_ecosystem = sources.governance_urls
    all_posts_and_views = []
    
    #Scraping 
    for k,v in defi_ecosystem.items():
        data = scrape(v)
        all_posts_and_views.extend(data)
        
    #file creation
    with open('defi_db.csv', 'w',encoding='utf-8' , newline="") as file:
        writer = csv.writer(file)
        for item in all_posts_and_views:
            writer.writerow([item[0]])
            
    return 0


#checks for new posts and if you provide a valid arg returns latest 3 posts
def check_for_posts(arg="all"):
    
    defi_ecosystem = sources.governance_urls
    old_all_posts = []
    all_posts = []
    new_unseen_posts = []
        
    #read file (previous scrape)
    with open('defi_db.csv', encoding='utf-8' , newline="") as file:
        reader = csv.reader(file)
        
        #saving file into variable_old_all_posts
        for row in reader:
            old_all_posts.append(row[0])
            
    #no args provided, scraping whole defi
    if arg == "all":
        #getting projects names
        for k,v in defi_ecosystem.items():
            #scraping individual projects
            data = scrape(v)
            #saving scrapes in all_posts
            all_posts.extend(data)
        #parsing scraped items
        for item in all_posts:
            if item[0] in old_all_posts:
                #if item is in the old_all_post(meaning viewed) do nothing..
                pass
            else:
                #making list of new unseen posts to return.
                new_unseen_posts.append(item)
        if len(new_unseen_posts) == 0:
            return "No new posts available.."
        else:
            #add new entries to the file
            with open('defi_db.csv','a', encoding='utf-8' , newline="") as file:
                writer = csv.writer(file)
                for item in new_unseen_posts:
                    writer.writerow([item[0]])
            return new_unseen_posts
    else:
        for k in sources.governance_urls:
            if k == str(arg).lower(): 
                itemslist = scrape(sources.in_gov_scope(k))
                #created a list of unwanted words to rule out welcome posts with guidelines..
                unwanted_words=['welcome','please','before posting']
                if any(word in itemslist[0][0].lower() for word in unwanted_words):
                    x = 1
                    data_to_return=[]
                    while x < 4:
                        data_to_return.append(itemslist[x])
                        x+=1
                    return data_to_return
                else:
                    x = 0
                    data_to_return=[]
                    while x < 3:
                        data_to_return.append(itemslist[x])
                        x+=1
                    return data_to_return
        else:
            return "Wrong value provided/unsupported project"
                




def new_unchecked_posts(arg="all"):
    if arg == "all":   
        data=check_for_posts()
        if type(data) == str:
            return data
        else: 
            return data
    else:
        data=check_for_posts(arg)
        if type(data) == str:
            return data
        else:
            data_to_return=[]
            for item in arg:
                #message item to chat 
                data_to_return.append(item)
            return data_to_return






###scrape post url
def scrape_post(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    #### GET DATE FROM POST
    date_ = soup.div.find(class_="crawler-post-infos")
    date = ((date_.get_text()).strip()).split("\n")[0]

    #### GET POST CONTENT
    content_ = soup.div.find(class_="post")
    content = content_.get_text()
    data = content.split("\n")
    p_content = []
    for item in data:
        p_content.append(item)
        
    ###### GET POST TITLE
    title= soup.h1.get_text().strip()
    
    return [title,date,p_content]



