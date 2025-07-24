Let’s design an in-memory file sharing app:

##  ✅ Functional Requirements:
-  Users can register
-  Users can follow other users
-  Users can upload files
-  Users can send files to one or more users (via sharing)
-  Users can view their received/shared files
-  Users can see their followers and followings

##  🏗️ High-Level Design:
Entities:

```
User
├── id
├── name
├── followers: Set[User]
├── following: Set[User]
├── uploaded_files: List[File]
├── received_files: List[File]

File
├── id
├── name
├── content
├── owner: User
├── shared_with: Set[User]

```

##  ✅ Supported Commands:
-  `REGISTER <username>`
-  `FOLLOW <follower_username> <followee_username>`
-  `UPLOAD <username> <filename> <file_content>`
-  `SHARE <sender_username> <receiver_username_1> [<receiver_username_2> ...] <filename>`
-  `SHOW_FILES <username>` → uploaded + received files
-  `SHOW_FOLLOWERS <username>`
-  `SHOW_FOLLOWING <username>`

