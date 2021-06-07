# These are just some things which I planned to do, however, due to time constraints, I've been unable to

## Better WebScraping

If you type in "/tier Chansey RB", you'll notice that it shows an analysis in UU tier despite it actually having no analysis. This is because, during webscraping, the tiers
are received without any serperator (Hence, I've had to link the Tier.txt file), however, tiers here will come in the form OUUbers which contain UU within them and hence this 
error occurs. I need fixes to this and either of better scraping or better validation within the program should work.

## Better Input Validation

Pokemon which have no current analysis, for example "/sets Caterpie RB", return "The Pokemon you entered is incorrect" when infact that is not the case. 
This isn't on my top list of priorities, however, an easy validation would be to compare the first element within the input to check whether it is a valid Pokemon or not.
This gives me guarentee that in the try except statement at the end, that if there is an error, it is due to there being nothing to export, or rather, no analysis and the 
correct statement can be given.

These are just a few of the bugs I've found out, I'm sure after some more testing, I'll find out more bugs.
