# Dwayne
A simple email-based tool, for asynchronous stand-up meetings and workflow analysis.   
**DISCLAIMER:** The project is still a work-in-progress, and there hasn't been a definite first release yet.

[comment]: # (README template https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)





## Motivation
**TL;DR** This is an email-based alternative to [Geekbot](https://geekbot.io/). It's a tool used for asynchronous stand-up meetings over email, that can also be used to quantify your workflow.   
It requires reading through your inbox archive in the [mbox](https://en.wikipedia.org/wiki/Mbox) format, which is the default format used by Thunderbird.

Shortly before I completed my last internship, Geekbot was introduced for stand-up meetings in our Slack. I liked the idea, but the main drawbacks is my love-and-hate relationship with Slack, as well as... it wasn't free for personal use.   
I set out to [cook my own dogfood](https://en.wikipedia.org/wiki/Eating_your_own_dog_food), using my weapon-of-choice, Python, and *the best* method of communicating through the internet. Email.

<figure>
    <img src="/resources/images/exhibit_a.png" style='height: 80%; width: 80%; object-fit: contain'/>  
</figure>

As a long-time lover of good-old Python 2.7, it was an opportunity to finally bite the bullet. This was my first project that was developed and tested using Python 3 *exclusively*.


### Description 
The tool is supposed to run on the *Master side* (the Supervisor, PM, or just yourself, if you wish to record your own standups).

The *Client Side* (team members), can send back emails to an address specified by the Master Side, where they respond to three questions, specified by the configuration file. The default questions are.
```
What did you get involved in since the last time?

What are you working on now, and what's next?

Any obstacles impeding your progress?
```

Whenever Master Side runs the tool, it searches through a specific mailbox, to find emails that have a specific keyword/activator in their subject line. Then, `Dwayne` collects these emails, parses the `text/plain` part of the *latest reply* only, and extracts the answers provided to these questions.

The results are stored in a database, and can be accessed through SQL queries, or through a web interface dashboard, made with Flask **(under development)**.


The schema of the `standups` table is the following. This first barebones version uses the nine first basic columns, while the extras will be implemented later to help with providing analytics and deeper insights.

```  
----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------
uid         isodate     mboxdate    sender      recipient   subject     answ1       answ2       answ3       mentions    team        task        hours     
----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------  ----------
```


## Installation and Usage
Step 1: Just `git clone` the repository and edit the `conf.py` file for your project. 

Step 2: Create the database by running `create_db.py`.

Step 3: Periodically use `run_dwayne.py` to collect the latest responses to you database! 

And... that's all! After that, you can welcome your team members (or yourself!) with an message, explaining what's this whole thing about. Feel free to use the `Welcome_to_Dwayne.md` email template in the `resources` folder as an initial explanation, as well as send out weekly something as `Dwayne_Standup.md`.

It should work on any platform that satisfies the requirements, but has only been tested on Linux, so don't hesitate to contact for any issues.



## Requirements
* An `mbox` archive of your inbox. (Thunderbird makes this easy).
* Python 3.x  
* [email_reply_parser](https://github.com/zapier/email-reply-parser)   
* SQLite   
* Flask   


## Future Development
Future plans include : 
* Addition of sample database for experimentation
* Release of the web interface
* Implementation of 'word clouds', and statistics on responses
* Implementation of `@user` style mentions 
* Get quotes on resource usage

### FAQ
* What about messy email threads?   
A large reply/forward/replyall/attachment email chain can get *really* messy. `Dwayne` grabs only the latest reply using [email_reply_parser](https://github.com/zapier/email-reply-parser), and parses just the `text/plain` part.

* Does it only support mbox archive format?   
For the time being, the tool can only crawl an inbox of this format. I think it is the most popular format out there for this kind of purpose, so it shouldn't be an issue. It also allows to just use the local drive backup of your mailbox, and avoid providing the credentials/tokens to your online accounts.

* What's with the name?    
I'm kinda bad at naming things, but 'Dwayne' is simple, memorable, and most importantly, not in use by other software projects. Adding a motivational image of Dwayne 'The Rock' Johnson to the email sent to the team is optional. 


## Contributing.
Feel free to send pull requests or submit an issue for bugs or suggestions.

## License
MIT © [tpaschalis](https://tpaschalis.github.io)

