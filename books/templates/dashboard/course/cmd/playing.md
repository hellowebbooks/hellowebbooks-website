## The blank, scary command line

<figure class="caption">
<img src="/static/images/course/cmd/prompt.jpg" alt="" class="no-shadow"/>
<figcaption>Your username and computer name, and then $ shows you where you start typing.</figcaption>
</figure>

Back to this blank page with all its hidden power and possibilities!

In the example above, you see my username "limedaring", and my computer name, “Orion,” so what you see will be different and will show your own personal values.

The `$` is the prompt. In a lot of programming tutorials, you might see commands that you need to type into your command line looking like this:

```

$ yourcommandtotypein

```  

These tutorials use that `$` to show you that you’re in the command line and this is the place where you’ll be typing, ignoring your own personal username and computer name.

## Listing files in our current directory

### ls

The first command we’ll learn is `ls`, which is short for "list." You will notice that commands are shortened to be as short as possible, which’ll be helpful when you’re comfortable using these commands and are typing them in over and over. Less characters to type!

Type in `ls` and press enter, and see what happens:

<figure class="caption">
<img src="/static/images/course/cmd/home.jpg" alt="" class="no-shadow"/>
</figure>

Oh hey, that might look familiar! Open up a new Finder window and click on your username in the left sidebar. It’s all the same files/folders!

<figure class="caption">
<img src="/static/images/course/cmd/same.jpg" alt="" class="no-shadow"/>
</figure>

The command line always starts us in our user directory. And just like how you can click on a folder in Finder to see what’s in the folder, you can navigate in and out of folders (which we’ll refer as "directories" here on out) using your command line.

## Changing directories

### cd

In Finder, I can click on "Music" see to see the contents of that folder. And in the command line, I can use the command `cd` (“change directory”) to “open” up that directory.

<figure class="caption">
<img src="/static/images/course/cmd/iTunes.jpg" alt="" class="no-shadow"/>
<figcaption>Clicked on Music, I can see the contents of the folder.</figcaption>
</figure>

<figure class="caption">
<img src="/static/images/course/cmd/cdmusic.jpg" alt="" class="no-shadow"/>
<figcaption>I `cd`'d into Music. Compared to Finder. Looks kind of boring compared to Finder!</figcaption>
</figure>


In the command line screenshot, I `cd`'d into Music. Use your imagination — you
just *stepped* into the directory. The command line updated to show that you’re
currently “in” the Music directory. And here, you can use `ls` to see the
directory's contents, just like in Finder.

<figure class="caption">
<img src="/static/images/course/cmd/Itunes2.jpg" alt="" class="no-shadow"/>
<figcaption>There’s that iTunes folder!</figcaption>
</figure>

In your Finder window, you could click around anywhere and see the contents of those folders. Finder is, essentially, cd-ing and ls-ing behind the scenes, and displaying the results in a much prettier graphical representation, rather than just using text.

We can use `cd` and `ls` again to check out the iTunes directory:

<figure class="caption">
<img src="/static/images/course/cmd/itunes3.jpg" alt="" class="no-shadow"/>
</figure>

Wait, we’re only stepping forward. How can we go back to where we were before?

## Changing directories to go back to where we came

### cd ..

In the command line, we can’t just click and go anywhere. It’s not even obvious how to go back to our main user directory! For that, we’ll use `cd ..` to step back:

<figure class="caption">
<img src="/static/images/course/cmd/cdup.jpg" alt="" class="no-shadow"/>
</figure>

We can even chain the dots with a slash to step back multiple steps:

<figure class="caption">
<img src="/static/images/course/cmd/cdupup.jpg" alt="" class="no-shadow"/>
</figure>

Hey, we’re back in that home directory! I like to use `ls` to double check where I am by checking out the contents of the directory.

Go back too much? Use `ls` to see what’s in the directory you’re in, and then use `cd` to head back to where you want to go:

<figure class="caption">
<img src="/static/images/course/cmd/backfar.jpg" alt="" class="no-shadow"/>
<figcaption>We went "back" too far, now we’re in the directory that contains our main user
directory.</figcaption>
</figure>

<figure class="caption">
<img src="/static/images/course/cmd/backhome.jpg" alt="" class="no-shadow"/>
<figcaption>`cd` into your user directory (using your own username) to get back into your main home directory.</figcaption>
</figure>

Fun fact! You can `cd` into any folder that you want from Finder by dragging the folder into the command line! This one is a little bit hard to illustrate without a gif (TODO: See here for one!) You just type `cd` into your command line  (don’t forget a space after `cd`), then click and hold on a folder in your Finder, and drag it over to where you would type the destination. Your computer will put the path to that folder into your command line for easy `cd`ing!

<figure class="caption">
<img src="/static/images/course/cmd/clickdrag.jpg" alt="" class="no-shadow"/>
<figcaption>Drag that folder into your command line input area to get the
path!</figcaption>
</figure>

# Making, moving, and deleting files

Here’s where things start to get fun. We can use the command line to create, move, and delete files on our hard drive!

## Creating files

### touch

`touch` will allow you to create files from nothing. Just add the name and type
of file you want after the `touch` command. Let’s make a new file, *hello.txt*.
Wherever you want (perhaps in your home directory), type `touch hello.txt`.

There isn’t going to be any success message or anything, so do `ls` to see the contents of the directory that you’re in to confirm that the file was made. Tada!

<figure class="caption">
<img src="/static/images/course/cmd/hellotxt.jpg" alt="" class="no-shadow"/>
</figure>

And you can see the file in Finder as well:

<figure class="caption">
<img src="/static/images/course/cmd/findernew.jpg" alt="" class="no-shadow"/>
</figure>

Maybe we don’t want it in the home directory. Instead of clicking/dragging it in Finder, let’s move it to another directory in the command line.

## Moving files

### mv

The command to move is `mv`, which looks obvious enough. There are a few other things we need to add to the command so the computer knows what file you want to move and where you want to move it.

To move the file into, say, the Music folder in my home folder, I would type `mv NAMEOFFILE WHERETOMOVEIT` — so, `mv hello.txt Music` to move the *hello.txt* file into the Music folder:

Note that, again, you won’t get a success message or anything reassuring, so you can `ls` on the directory that you’re on to confirm that it disappeared, then `cd` into the directory you moved your file into and `ls` again to confirm that the file now appears in this new directory:

<figure class="caption">
<img src="/static/images/course/cmd/nowinmusic.jpg" alt="" class="no-shadow"/>
</figure>

The `../` thing we learned about changing directories backwards, also works to move the file back up a directory too:

<figure class="caption">
<img src="/static/images/course/cmd/moveback.jpg" alt="" class="no-shadow"/>
</figure>

Next, let’s learn how to make copies from the command line.

## Copying files

### cp

Another command that looks just like what it does! To copy, you do `cp NAMEOFFILE NEWNAMEOFCOPIEDFILE`. So to copy our *hello.txt* and name the copied file, *goodbye.txt*, we would run this command: `cp hello.txt goodbye.txt`

<figure class="caption">
<img src="/static/images/course/cmd/copied.jpg" alt="" class="no-shadow"/>
</figure>

*Remember, no response **usually** means success! `ls` the files in your directory to confirm that the new file has appeared.*

(FYI, if you’re looking to copy directories, not individual files, hold your horses — we’ll get to that in a bit!)

Kind of silly to have two empty files, right? Let’s learn how to delete files.

## Deleting files

### rm

This part is kind of understandably scary. When you delete files using the command line, there is no Trash Can or Recycling Bin for them to live in that you can use to reverse an accidental deletion. They’re just gone (eep).

(This is where a system like *git,* a version control system to track changes in files, would comes in handy. It’s highly recommended to use with any programming projects so you can save updates and restore from backup if you need to. Stay tuned for a guide for how to work with git!)

We know our *goodbye.txt* file is useless, since it’s a copy of our original file (and empty to boot). Let’s remove it by using `rm FILENAME` (so, `rm goodbye.txt`):

<figure class="caption">
<img src="/static/images/course/cmd/goodbye.jpg" alt="" class="no-shadow"/>
<figcaption>Again, no success message, so we’ll check the directories files to confirm
that goodbye.txt disappeared.</figcaption>
</figure>
