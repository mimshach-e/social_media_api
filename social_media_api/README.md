


# API Documentation: Posts and Comments

## Base URL
`/api/`

## Authentication
Most endpoints require authentication. Include your authentication token in the header of your requests:
```
Authorization: Token your_token_here
```

## Endpoints

### Posts

#### List Posts
- **URL**: `/posts/`
- **Method**: GET
- **Auth required**: No
- **Permissions**: None
- **URL Params**: 
  - `page=[integer]` (optional)
  - `search=[string]` (optional)
  - `title=[string]` (optional)
- **Success Response**: 
  - Code: 200
  - Content: 
    ```json
    {
      "count": 123,
      "next": "http://api.example.org/posts/?page=4",
      "previous": "http://api.example.org/posts/?page=2",
      "results": [
        {
          "id": 1,
          "author": {
            "id": 1,
            "username": "john_doe"
          },
          "title": "Sample Post",
          "content": "This is a sample post content.",
          "created_at": "2024-09-19T10:00:00Z",
          "updated_at": "2024-09-19T10:00:00Z",
          "comments": []
        },
        // ... more posts
      ]
    }
    ```

#### Create Post
- **URL**: `/posts/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: IsAuthenticated
- **Data constraints**:
  ```json
  {
    "title": "[1 to 200 chars]",
    "content": "[1 to 1000 chars]"
  }
  ```
- **Success Response**:
  - Code: 201
  - Content: `{<post_object>}`

#### Retrieve Post
- **URL**: `/posts/<id>/`
- **Method**: GET
- **Auth required**: No
- **URL Params**: None
- **Success Response**:
  - Code: 200
  - Content: `{<post_object>}`

#### Update Post
- **URL**: `/posts/<id>/`
- **Method**: PUT/PATCH
- **Auth required**: Yes
- **Permissions**: IsAuthorOrReadOnly
- **Data constraints**: Same as POST
- **Success Response**:
  - Code: 200
  - Content: `{<updated_post_object>}`

#### Delete Post
- **URL**: `/posts/<id>/`
- **Method**: DELETE
- **Auth required**: Yes
- **Permissions**: IsAuthorOrReadOnly
- **Success Response**:
  - Code: 204

### Comments

#### List Comments for a Post
- **URL**: `/posts/<post_id>/comments/`
- **Method**: GET
- **Auth required**: No
- **Permissions**: None
- **URL Params**: 
  - `page=[integer]` (optional)
- **Success Response**: 
  - Code: 200
  - Content: List of comment objects

#### Create Comment
- **URL**: `/posts/<post_id>/comments/`
- **Method**: POST
- **Auth required**: Yes
- **Permissions**: IsAuthenticated
- **Data constraints**:
  ```json
  {
    "content": "[1 to 500 chars]"
  }
  ```
- **Success Response**:
  - Code: 201
  - Content: `{<comment_object>}`

#### Retrieve Comment
- **URL**: `/posts/<post_id>/comments/<id>/`
- **Method**: GET
- **Auth required**: No
- **Success Response**:
  - Code: 200
  - Content: `{<comment_object>}`

#### Update Comment
- **URL**: `/posts/<post_id>/comments/<id>/`
- **Method**: PUT/PATCH
- **Auth required**: Yes
- **Permissions**: IsAuthorOrReadOnly
- **Data constraints**: Same as POST
- **Success Response**:
  - Code: 200
  - Content: `{<updated_comment_object>}`

#### Delete Comment
- **URL**: `/posts/<post_id>/comments/<id>/`
- **Method**: DELETE
- **Auth required**: Yes
- **Permissions**: IsAuthorOrReadOnly
- **Success Response**:
  - Code: 204

## Error Responses

- **Condition**: If a request is made with invalid data or to a non-existent resource.
- **Code**: 400 BAD REQUEST
- **Content**: `{ "error": "Error message here" }`

- **Condition**: If a request is made without proper authentication.
- **Code**: 401 UNAUTHORIZED
- **Content**: `{ "detail": "Authentication credentials were not provided." }`

- **Condition**: If a request is made without proper permissions.
- **Code**: 403 FORBIDDEN
- **Content**: `{ "detail": "You do not have permission to perform this action." }`

- **Condition**: If a request is made to a non-existent resource.
- **Code**: 404 NOT FOUND
- **Content**: `{ "detail": "Not found." }`


## 2. Implementing User Follows and Feed Functionality
## Step 1: Update the User Model to Handle Follows
We've modified the CustomUser model in `accounts/models.py` to include a following field. This is a many-to-many relationship to itself, allowing users to follow other users.
After making this change, you'll need to create and apply migrations:
`python manage.py makemigrations accounts`
`python manage.py migrate`

## Step 2: Create API Endpoints for Managing Follows
We've added two new views in `accounts/views.py`: `follow_user` and `unfollow_user`. These views handle the logic for following and unfollowing users. They include permission checks to ensure only authenticated users can perform these actions.

## Step 3: Implement the Feed Functionality
We've created a FeedView in `posts/views.py`. This view returns posts from users that the current user follows, ordered by creation date (most recent first).

## Step 4: Define URL Patterns for New Features
We've added new URL patterns in both `accounts/urls.py` and `posts/urls.py` to route requests to our new views.

## Step 5: Test Follow and Feed Features
To test these new features, you can use Postman or a similar tool. Here are some example API calls:

# Follow a user:
URL: /api/follow/<int:user_id>/
Method: POST
Authentication: Required
Description: Allows the authenticated user to follow another user specified by user_id.
(Assumes you're following a user with ID 2)

# Unfollow a user:
URL: /api/unfollow/<int:user_id>/
Method: POST
Authentication: Required
Description: Allows the authenticated user to unfollow a previously followed user specified by user_id.

# Get your feed:
URL: /api/feed/
Method: GET
Authentication: Required
Description: Returns a list of posts from users that the authenticated user follows, ordered by creation date (newest first).

NB: Proper authentication (e.g., JWT token) are included in the headers of these requests.



# Social Media API Documentation: Likes and Notifications Functionality

## Overview

This document outlines the likes and notifications system implemented in our Social Media API. These features enhance user engagement by allowing users to like posts, comment on content, and receive notifications for various interactions. The notifications system has been enhanced to prominently showcase unread notifications and provide functionality to mark notifications as read.

## Models

### Like Model

The Like model represents a user's like on a post. Key features:
- Links a user to a post they've liked
- Ensures a user can only like a post once
- Stores the timestamp of when the like was created

### Notification Model

The Notification model stores various types of notifications. Key features:
- Identifies the recipient of the notification
- Identifies the actor (user who triggered the notification)
- Describes the action with a verb (e.g., "liked", "commented")
- Uses a generic relation to link to any model (e.g., a post or comment)
- Includes a timestamp and a read status

## Core Functionalities

### Liking a Post

Users can like posts through the API. The system:
- Creates a new Like instance
- Ensures a user can't like the same post multiple times
- Generates a notification for the post author

### Commenting on a Post

Users can comment on posts. The system:
- Creates a new Comment instance
- Generates a notification for the post author (if the commenter is not the author)

### Viewing Notifications

Users can retrieve their notifications through the API. The system:
- Returns a list of notifications for the authenticated user
- Orders notifications by timestamp (newest first)

## Unread Notifications
The API now highlights unread notifications by:

Providing an unread count in the response
Maintaining an is_read status for each notification

## API Endpoints

1. **Like a Post**
   - Endpoint: `/api/posts/<post_id>/like/`
   - Method: POST
   - Authentication: Required
   - Description: Allows a user to like a specific post

2. **Create a Comment**
   - Endpoint: `/api/comments/`
   - Method: POST
   - Authentication: Required
   - Description: Allows a user to comment on a post

3. **Fetch Notifications**
   - Endpoint: `/api/notifications/`
   - Method: GET
   - Authentication: Required
   - Description: Retrieves the authenticated user's notifications
   - Response: Includes an unread_count and a list of notifications

4. **Mark All Notifications as Read**
   - Endpoint: `/api/notifications/mark_all_read/`
   - Method: POST
   - Authentication: Required
   - Description: Marks all of the user's unread notifications as read

5. **Mark Single Notification as Read**
   - Endpoint: `/api/notifications/<notification_id>/mark_as_read/`
   - Method: POST
   - Authentication: Required
   - Description: Marks a specific notification as read

# Usage

1. To get notifications with unread count:
   - Send a GET request to `/api/notifications/`
   - The response will include unread_count and results (list of notifications)
2. To mark all notifications as read:
   - Send a POST request to `/api/notifications/mark_all_read/`
3. To mark a specific notification as read:
   - Send a POST request to `/api/notifications/<notification_id>/mark_as_read/`

## Notification Triggers

Notifications are created for the following actions:
1. When a user likes another user's post
2. When a user comments on another user's post
3. When a user follows another user

Each notification includes:
- Recipient (usually the post author)
- Actor (user who performed the action)
- Verb (description of the action)
- Target (the post that was liked or commented on)

## Permissions

The API implements the following permission classes:
- `IsAuthenticatedOrReadOnly`: Allows authenticated users to perform write operations, while allowing anyone to perform read operations.
- `IsAuthorOrReadOnly`: A custom permission that only allows the author of an object (e.g., a comment) to modify or delete it.

## Pagination

Comment listings use pagination to manage large sets of data efficiently. This helps in reducing load times and improving overall performance.

## Best Practices

1. Always authenticate before attempting to like a post or create a comment.
2. Handle potential errors, such as trying to like a post that doesn't exist.
3. When fetching notifications, be prepared to handle pagination if implemented.
4. Regularly fetch the notifications to get the updated unread count.
5. After a user views their notifications, consider marking them as read to keep the unread count accurate.
6. Provide users with options to mark individual notifications as read or to mark all as read at once.

