from bs4 import BeautifulSoup
import os

# Path to the main dataset directory:
blogs_path = '/Users/sunyambagga/Desktop/MinorProjects/7th_Sem/blogs'

# 'all_blogs_data' is a list of dictionaries where each dictionary represents a blog, each blog has various 'keys': Gender, Age, Posts, Dates etc.

all_blogs_data = []

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





def blog_to_sframe():
    i = 1
    for blog in os.listdir(blogs_path)[1:]:
        i += 1
        path_to_blog = blogs_path + '/' + blog
        print path_to_blog
        # Convert blog to Dictionary
        blog_dict = blog_to_dict(path_to_blog)
        print "\n\n"
        if i == 3:
            break