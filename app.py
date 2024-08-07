from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('storage/blog_data.json') as user_file:
        blog_posts = json.load(user_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_id = int(request.form.get('id'))
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        
        new_post = {
            "id" : post_id,
            "auhtor" : author,
            "title" : title,
            "content" : content
        }
        
        with open('storage/blog_data.json', 'r') as user_file:
            blog_posts = json.load(user_file)
            
        blog_posts.append(new_post)
        
        with open('storage/blog_data.json', 'w') as user_file:
            json.dump(blog_posts, user_file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open('storage/blog_data.json', 'r') as user_file:
        blog_posts = json.load(user_file)
    
    for post in blog_posts[:]:
        if post["id"] == post_id:
            blog_posts.remove(post)
    
    with open('storage/blog_data.json', 'w') as user_file:
        json.dump(blog_posts, user_file, indent=4)
    
    return redirect(url_for('index'))

@app.route('/update/<int:update_id>', methods=['GET', 'POST'])
def update(update_id):
    post = fetch_post_by_id(update_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        with open('storage/blog_data.json', 'r') as user_file:
            blog_posts = json.load(user_file)
        
        for index, p in enumerate(blog_posts):
            if p["id"] == update_id:
                blog_posts[index] = {
                    "id": update_id,
                    "author": author,
                    "title": title,
                    "content": content
                }
                break
        
        with open('storage/blog_data.json', 'w') as user_file:
            json.dump(blog_posts, user_file, indent=4)
        
        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    with open('storage/blog_data.json', 'r') as user_file:
        blog_posts = json.load(user_file)
    
    for post in blog_posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break
    
    with open('storage/blog_data.json', 'w') as user_file:
        json.dump(blog_posts, user_file, indent=4)
    
    return redirect(url_for('index'))

def fetch_post_by_id(post_id):
    try:
        with open('storage/blog_data.json', 'r') as user_file:
            blog_posts = json.load(user_file)

        post_id = int(post_id)
        
        for post in blog_posts:
            if post["id"] == post_id:
                return post
        
        print(f"Post with ID {post_id} not found.")
        return None

    except Exception as e:
        print(f"Error fetching post by ID: {e}")
        return None


if __name__ == '__main__':
    app.run()