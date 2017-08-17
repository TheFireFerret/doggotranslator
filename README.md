# Doggo word translator (website + discord bot)

Have you ever needed to know what "waterboye" or "subwoofer" (no, not the speaker) meant? Now you can!

## Firebase & Pyrebase
[Firebase](https://firebase.google.com) has a realtime database this app uses to store all translations. The python wrapper for the firebase API I am using is [Pyrebase](https://github.com/thisbejim/Pyrebase).


The translation data is represented as a many-to-many database since our translations can have different words, such as `seal,sea lion <-> water doggo,waterboye`.

A word can only be either english or doggospeak, not both.

Firebase likes flat data, so we will store the data like this:

```
{
	word_ID {
		type: english / pupperspeak
		word: "word"
		translation_ID_1 {
			translation: word_ID
		}
		translation_ID_2 {
			translation: word_ID
		}
		...
	}
	...
}
```


Both the discord bot and the website will share a single python backend on top of firebase.

## Phase One: Website
The home page will be simple search bar that would provide the translations, preferbably done through [React](https://facebook.github.io/react/) to avoid page reloads. A seperate page would have translation additions, deletions, and edits. 

Hosting will be done on AWS, which ~~should~~ support both the website and the bot at once


[use the aws docs for setup](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html) lol

## Phase Two: discord bot
This bot show allow users to request translations as well as add, remove, and edit existing ones. Addition, removal, and edits should be limited to trusted users. Maybe a dedicated discord server to maintain the bot / database?

First the backend needs new api commands for the bot to use.

also how to host bot???

