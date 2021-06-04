# Game_Bot
We are developing a bot for R&amp;D Project, that is made for turn-based games in discord.

# How to install and setup the bot and the database.
- (Optional) Use a VPS to host the bot and database
We assume you have python installed.
- (Optional) Create a virtual environment
- Change directory to the gamebot file and use `pip3 install -r requirements.txt` (Optionally inside the virtual environment).
(Required) 
- Install MYSQL, in our case we have installed Ver 8.0.25 for Linux.
- Create a database like so:

![image](https://user-images.githubusercontent.com/5383805/120824318-a0c52280-c558-11eb-8465-480a2ab3b453.png)
- Now do the following commands: `USE yourdatabasename`and `source directorytogamebot/database/dbscripts/dbtables.sql` where you change 'directorytogamebot' to your directory to the gamebot and use `exit` to close the MYSQL environment.
- Now that you are done with setting up the database, edit `config.json` with your discord bot token and MYSQL user, password, host and the same yourdatabasename as previous steps.
- (Run the virtual environment if you made one and) If everything went correctly, you should be able to run `python3 main.py`. 
(To run a command 'forever', use `nohup python3 main.py &` on linux/vps server)


# How to setup the website using Apache2 and mod_wsgi
This will be a lot more complicated, so I will be giving a brief explanation how it should be done using our files?
Install and enable apache2 and mod_wsgi and then change the apache DocumentRoot to the gamebot directory. And then configure the mod_wsgi 
If you know how to setup a virtual environment using mod_wsgi, which we weren't able to figure out you could use the same virtual environment as explained in how to setup the bot and the database.
Instead we didn't know how to do that, so we globally install the packages. And changing the DocumentRoot directory did not work for us, so we moved the FlaskApp folder to /var/www and added the config file and database folder at /var/www/FlaskApp. I think it was very unfortunate that we weren't able to keep everything in one project.

A pretty handy link on how to deploy a flask application https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
