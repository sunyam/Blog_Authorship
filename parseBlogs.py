from bs4 import BeautifulSoup
import os

# Path to the main dataset directory:
blogs_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/blogs'

def blog_to_dict(path_to_blog):
    
    file_name = path_to_blog.split('/')[-1]
    # Remove .xml
    file_name = file_name[:-4]
    
    id, gender, age, industry, sunsign = file_name.split('.')
    # Will ignore industry and sunsign in this project

    blog_dict = {}
    blog_dict["Age"] = age
    blog_dict["Gender"] = gender
    blog_dict["Id"] = id
    # Posts is going to be a list of tuples: [(date1, post1), (date2, post2)....]
    blog_dict["Posts"] = []

    with open(path_to_blog, 'rb') as f:
        blog_content = f.read()

        # Need to clean the content
        blog_content = blog_content.replace("&nbsp;", " ").replace("<Blog>", "").replace("</Blog>", "")

        # Strip off the unnecessary whitespaces
        blog_content = blog_content.strip()

        for A in blog_content.split("<date>")[1:]:
#            date = A.split("</date>")[0].strip()
            # Date not needed for this project
            
            post = A.split("</date>")[1].replace("<post>", "").replace("</post>", "").strip()
            post = BeautifulSoup(post, "lxml").get_text()
            
            blog_dict["Posts"].append(post)

    return blog_dict


def process_blogs():

    for blog in os.listdir(blogs_path)[1:]:
        path_to_blog = blogs_path + '/' + blog
        # Convert blog to Dictionary
        blog_dict = blog_to_dict(path_to_blog)
        all_blogs_data.append(blog_dict)

    print str(len(all_blogs_data)) + " blogs parsed.\n"
    print "\n\n Beginning the For Loop now:\n"

    ####################################################
        # Writing all blog posts in .txt files for word2vec (gensim) to be able to process them
    i = 1
    for blog_dict in all_blogs_data:
        all_posts = "\n".join(blog_dict['Posts'])
        
        with open('/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/txt_blogs/'+str(blog_dict['Id'])+'.txt', 'wb') as f:
            f.write(all_posts.encode('utf8'))
    
        i += 1

    print "We have written " + str(i) + " blogs."
    ####################################################


# 'all_blogs_data' is a list of dictionaries where each dictionary represents a blog, each blog has various 'keys': Gender, Age, Posts, Dates etc.
all_blogs_data = []

process_blogs()