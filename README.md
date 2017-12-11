ALLISON WANDERER FINAL PROJECT 364

My app lets you enter a web of Twitter followers! You are able to see the most recent followers of a desired Twitter user and then see those follower's most recent followers. On top of seeing the followers, you see their name, handle, description, and location

First, you register and/or log in with your email address
From there, you are welcomed to the home page
On this page you can click to search for a Twitter user to see their most recent followers. You can also upload a new profile picture for our site. With the profile picture, you can also check if your profile picture already exists in our internal system or not.

When you go to search for a Twitter handle, you press submit and you then get a list of that person's 20 most recent followers and certain information(name, handle, user description, and where they are from)
Each of the follower's handles are linked which when clicked on takes you to a page of their most recent followers! (same format) Those follower's handles are also linked which when clicked on takes you to their actual Twitter profile page. 

You get an email when you enter a Twitter handle to search for their followers. 


DEPLOYED APP: http://ec2-54-146-241-213.compute-1.amazonaws.com/

Email is sometimes shaky as we discussed, so I included a screenshot as proof

Things that need to be installed: 
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from threading import Thread
from werkzeug import secure_filename
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
import tweepy
from werkzeug.security import generate_password_hash, check_password_hash
import time 
from werkzeug.utils import secure_filename
from flask import send_from_directory, jsonify
import os.path

run it by running si464_final.py and viewing your localhost:5000 page
(python si364_final.py runserver)