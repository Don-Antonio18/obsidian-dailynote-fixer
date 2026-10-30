Like a lot of us, I use daily notes with the format YYYY-MM-DD. The problem I had was that, unlike in apps like Day One, I couldn't know what my journal entry was even about apart from the date. I tried just appending a title after the date, like "YYYY-MM-DD Title" but that made the little dot disappear from the calendar view that showed when entries were made. I didn't like that, so I did some research for solutions.

I found that some people add a title PROPERTY to their daily notes, so that when they create a base for their journal entries, they can easily see the title. Now, that was all well and good, but renaming dozens of files is daunting. I figured that this was a perfect use for AI.

I got Claude to create a python script that parses through the daily notes folder and:
1 - spliced custom appended titles from journal entry dates
2 - Add a title property to each note if it didn't already exist
3 - adds the spliced titles to the title property

Voila, now all my notes show up in the calendar view, and I can use a base to see a table of all my entries with the title.

Here is the code. You can simply copy paste it into a code editor, choose a name for the file, and run it with the path of your folders in string format ("") with the --apply concatenator. Running it without --apply shows u a dry preview of the potential changes, similar a dry run of the mo system cleaner.