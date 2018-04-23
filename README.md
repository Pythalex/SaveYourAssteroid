# LudumDare41-Compo
My game for the LudumDare 41 - Compo

My first LD/jam

Pythalex - April 2018


### Concept
Here's my game Save Your Assteroid. You're a space pilot, while tracking some imperial/bad guy/shady ship as a spy, 
your tailing is compromised as you enter in an asteroid field. 
Beware, because your enemy might use this opportunity to get rid of you.

Your goal ? Try to survive as much as you can by avoiding coming rocks. You can collide with your enemy to make him 
crash on an asteroid, slow his movements by picking slower malus. 
Who knows, maybe you'll come out of it alive ...

----------

## Real note:

This game is mainly built to be played with 2 local players. You can play with 1-4 players at the same time. 
Save Your Assteroid is basically a top-scrolling game where you must avoid obstacles coming from the top. You can 
move in all directions. As you advance in the asteroid field, you get points. When you've lost, you can see the 
score of all players and the final ranking.

### Game code structure
I created a UML diagram for this:

[![LD41-_UML-2.png](https://s14.postimg.cc/wf93njhox/LD41-_UML-2.png)](https://postimg.cc/image/kq53zkqq5/)

This game could be written both in OOP or PP, I just find class diagrams really cool to read.

As for this program, I chose to use full OOP instead of OOP-PP mix for better readability.

### How to run it

This game is made with pygame for python 3, so if you don't have it you'll need to install it. You can easily install pygame from pip with `pip3 install pygame` or `python -m pip install pygame`, depending on your setup.

Once you have installed pygame, download the 'Ready to launch' package. In the SaveYourAssteroid folder :
`python game.py`

note: python needs to be python 3 for your setup.

### Some screenshots

![screen04.png](https://s14.postimg.cc/sexth88kx/screen04.png)


![screen01.png](https://s14.postimg.cc/iue6ubw3l/screen01.png)


![screen02.png](https://s14.postimg.cc/fnjnapjdd/screen02.png)


![screen03.png](https://s14.postimg.cc/8kbrv3lnl/screen03.png)