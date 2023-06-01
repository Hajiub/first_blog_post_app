from project.models import Post, User

post_id = 1  # Replace with the desired post_id

# Query the post with the given post_id
post = Post.query.get(post_id)

if post:
    # Access the comments associated with the post using the 'comments' attribute
    comments = post.comments

    # Iterate over the comments and print the user who added each comment
    for comment in comments:
        user = User.query.get(comment.user_id)
        if user:
            print(f"Comment by user {user.username}: {comment.content}")
        else:
            print(f"Comment with invalid user_id: {comment.content}")
else:
    print("Post not found.")
