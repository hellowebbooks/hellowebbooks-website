## What is `sudo`?

You might have seen this excellent xkcd comic:

<figure class="caption">
<img src="/static/images/course/cmd/sandwich.png" alt="" class="no-shadow"/>
<figcaption>https://imgs.xkcd.com/comics/sandwich.png</figcaption>
</figure>

`sudo` is the special secret "I’m the boss and do what I say" command (and is short for “**su**peruser **do”**). For most commands that affect your computer in a big way (for example, deleting *all* your files, or installing a new program), your computer will require you to put “sudo” in front of it, then require your computer’s password, to really make sure that you are aware of what you’re doing.

As a beginner, you’re not going to need to use `sudo` very much, but as you continue along in your programming career, you’re going to see references to this command.

## Making, moving, and deleting full directories

We’ve been working with individual files so far, but not full directories. The commands we’ve learned so far — `touch` (create) `mv` (move) or `cp` (copy) for example — won’t just work for directories.

### Creating directories with mkdir

`mkdir` ("**m** a **k** e **dir** ectory") is the command you will use to create a new directory. Try making an empty directory named “test” in your current location with `mkdir test`:

<figure class="caption">
<img src="/static/images/course/cmd/mkdir.jpg" alt="" class="no-shadow"/>
<figcaption>Run `ls` after creating your directory to confirm it was made.</figcaption>
</figure>

<figure class="caption">
<img src="/static/images/course/cmd/emptydir.jpg" alt="" class="no-shadow"/>
<figcaption>`cd` into your new test directory and, after running `ls`, you can see that it’s empty.</figcaption>
</figure>

### Moving directories with mv

This one is just the same as before! Move your new test directory into another other directory with the command `mv NAMEOFFILE NAMEOFDIRECTORY` (exactly the same as before):

<figure class="caption">
<img src="/static/images/course/cmd/mvmusic.jpg" alt="" class="no-shadow"/>
</figure>

Yay, nothing new to remember here. Let’s move it back into our home directory, which would be `mv test ../`. Make sure you’re "in" the directory where you moved your *test* folder. Also, note that you can move things backwards using the same `../` notation we learned above for traversing our hard drive!

Let's move our *hello.txt* into our new directory so it’s no longer empty. Go
back to your home directory (`cd ..`) and then move the test directory into your
currect folder with a “`.`” — so, `mv Music/test/ .`

Try it out! We’ll talk more about the single dot in a few pages.

<figure class="caption">
<img src="/static/images/course/cmd/movefun.jpg" alt="" class="no-shadow"/>
</figure>

Cool, now we have our test directory with our test file in it! What happens if we try to delete the whole thing?

### Deleting directories with rm -r

What’s that `-r` thing? New concept alert!

Every command we’ve learned so far has options (or "flags") we can add along to the command. We’ll explore using a flag for the first time by deleting our test directory.

First off, try to use our delete command (`rm THINGTODELETE`) with your test directory. What happens?

<figure class="caption">
<img src="/static/images/course/cmd/rmdir.jpg" alt="" class="no-shadow"/>
</figure>

Can’t delete the directory because it’s a directory! What to do?

When we add `-r` to our command, we’re telling it to delete *recursively* — so, delete not only the directory but also everything inside it. Without the `-r` flag, the delete fails because the command line doesn’t know if you want to delete *everything* in the folder. With `-r`, you’re basically saying, "Have at it, delete EVERYTHING" in the directory.

(Fun fact! You might have seen scary things about the command `rm -rf /`. You know the `-r` flag, and you can chain together many different flags — so here, the `-f` flag is added too, which means "force." The thing that the command is deleting is `/`, which is the top level directory of your entire hard drive (which is, usually, your entire computer). So, in english, this command is “Force remove everything, including directories and all the files, for my entire hard drive.” Scary! Back in the day, you could mess up your computer with just six characters in your command line. Now (yay!), computer makes have become wise to this and this command will *not* work. No need to worry about accidentally typing it and wiping your hard-drive!)

## How do I move things *into* my current directory?

### Indicating the current directory with .

Once you’ve gotten comfortable with traversing your hard drive using only commands, you might want to "enter" a directory and then move a file into that directory. So far, we’ve only covered moving things from the directory that we’re in, but we can also move things from elsewhere into our current “location”!

For example, this command: `mv ../test.txt .`. In english, this is saying "Move test.txt, which is the previous directory, into this current directory." That single dot at the end means “current location.” Pretty cool!

## Using wildcards

When specifying a file, you don’t have to be limited to just one — you can use the `*` wildcard to grab multiple files. That sounds confusing. It’s easier explained with an example! Say you wanted to move all .txt files in a directory into another directory. This would be the command you’d use: `mv *.txt NEWDIRNAME`:

<figure class="caption">
<img src="/static/images/course/cmd/wildcard.jpg" alt="" class="no-shadow"/>
</figure>

Nifty!
