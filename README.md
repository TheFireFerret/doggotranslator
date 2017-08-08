# Doggo word translator (website + discord bot)

Have you ever needed to know what "waterboye" or "subwoofer" (no, not the speaker) meant? Now you can!

## Firebase & Pyrebase
[Firebase](https://firebase.google.com) has a realtime database this app uses to store all translations. The python wrapper for the firebase API I am using is [Pyrebase](https://github.com/thisbejim/Pyrebase).


The translation data is represented as a many-to-many database since our translations can have different words, such as `seal,sea lion <-> water doggo,waterboye`.

A word can only be either english or doggospeak, not both.

*random translation given lol?*

The data will be stored like this:

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

There are not going to be too many words, so I don't need to worry about this data organization scaling too much. The longest operation will be the initial search for the word, since it could be either in english or pupperspeak. We could seperate these commends, but a single translation command is easier for the user, especially in something like a discord bot.

Both the discord bot and the website will share a single python backend on top of firebase.

## Phase One: Website
The home page will be simple search bar that would provide the translations, preferbably done through [React](https://facebook.github.io/react/) to avoid page reloads. A seperate page would have translation additions, deletions, and edits. 

Hosting will be done on AWS, which should support both the website and the bot at once, for very cheap.

~~post how to setup here once done~~

http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html lol
