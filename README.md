# BotAds <img src="https://github.com/user-attachments/assets/9ade5d54-c48c-41f6-93a1-bd3b646f7dfe" height="30"/> <br>VKBot <img src="https://github.com/user-attachments/assets/7158974e-bfe5-4142-8ad9-21e6ecf7827d" height="30"/>
#### BotAds is an automated bot designed for the social network VKontakte, developed using Python. Its primary goal is to streamline and automate the process of posting advertisements in VKontakte communities.

## Features
### BotAds offers the following functionalities:
1. Automatic Response to Messages: Upon receiving a message from a customer in VKontakte, the bot automatically responds.
2. Payment and Creation of Ad Posts: Customers can pay for advertising, create ad posts, and specify the desired publication date.
3. Automatic Posting of Ads: The bot schedules and publishes ad posts at the specified time and records them in a database.
4. Removal of Ads Upon Expiry: After the ad post's storage period expires, it is removed from both the database and the VKontakte community.

## Technologies Used
### The development of BotAds involved the use of several libraries and APIs:
* vkbottle: For interacting with VKontakte messages. <img src="https://github.com/user-attachments/assets/7117ada0-a0e2-4277-9bde-2a920b88868f" height="25"/>
* vk_api: For posting and deleting posts within VKontakte. <img src="https://github.com/user-attachments/assets/1fe51a19-4acb-49c1-ba86-9b5d635366d5" height="25"/>
* yoomoney: For processing payments for ad posts. <img src="https://github.com/user-attachments/assets/09054f9b-f24a-4f32-9856-c56a57676894" height="25"/>
* json: For storing information about posts in JSON format. <img src="https://github.com/user-attachments/assets/4d7b3f49-b744-41d8-b457-f0f0440ae011" height="25"/>
* sqlite3: For storing partial user data in a local SQLite database. <img src="https://github.com/user-attachments/assets/31890aed-d67e-4f2e-8e73-2d7c30b1a141" height="25"/>

