# ABC Insurance Assistant

## Introduction
This is a version zero insurance focused chatbot designed to demonstrate some of the functionality of the Rasa 
conversational AI platform.

The ABC Insurance Assistant has two existing customers in memory. 
* Jane Brown, whose policy number is 99999999 and has a claim registered against claim id AB1234.
* John Brown, whose policy number is 11111111 and has a claim registered against claim id AB4321.

The current stage of development is limited and not much has been done to prevent the bot becoming confused.  
It should however be able to follow predefined tasks such as issuing a new business quote or retrieve the status of a claim.

When the bot is activated it will require a greeting such as "Hello" for it to come to life.  If at any point 
in the conversational journey you want to reset the bot issue another greeting.

## Run the Bot
Before training your bot make sure you have installed all of the requirements from the requirements.txt file:

```
pip3 install -r requirements.txt
```
To run the bot locally you must first train your bot by opening a terminal window in the project directory. In the terminal window enter:

```
rasa train
```
When you're training successfully completes you will have a model artifact. Before you can start interacting with your bot the Action Server also needs to be running. The action server handles custom processing of messages. Starting the action server requires opening a new terminal window in your project directory. In the window enter:
```
rasa run actions
```
You will see a listing of the different actions that are a part of the server. You will need to keep this terminal window open.

Finally, the last piece is to start a Duckling server. The Duckling server will help the bot robustly extract numbers from the user messages. Open one more terminal window in your project root and enter:
```
docker run -p 8000:8000 rasa/duckling
```
Similar to the Action Server keep this running while you interact with your bot.

Now you can talk with the bot! In a terminal window enter:
```
rasa shell
```
This command will allow you to talk with the bot. If you want more more detail about what's happening with your bot you can add --debug to the command to display all of the debugging information.







