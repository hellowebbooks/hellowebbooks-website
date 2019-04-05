## My command didn’t work!

Make sure that you’re in the correct directory for what you want to run. Often, I’ll try to copy a file but forget what directory it is in. Run `ls` (the command to "list" all files in a directory) to confirm that you’re in the right directory with the file you need.

## I’m stuck and I don’t know how to get back to the command line!

Certain commands will replace your current command line window with another interface. Or, maybe you’ve started writing out some giant command (`mv thisfile.txt to/another/file/folder/wait/not/that/one`) and you don’t want to backspace allllll the way back to the start of the line.

Control-C (pressing both buttons at once) is your friend in situations like this. It’s basically an escape/start over command that works in most situations to start over. (This is sometimes written as `^C`, because shortcuts are handy)

<figure class="caption">
<img src="/static/images/course/cmd/ctrl.jpg" alt="" class="no-shadow"/>
</figure>

(That didn’t work? Try pressing "q", “ESC”, or “Control-D.” I know this sounds very unspecific but that’s what I do when I get into a weird screen that I don’t know how to get out of — I mash all the escape commands I can remember. Learn from me, a developer with multiple years of experience!)

## I can’t see files that start with a dot!

When you’re looking in your current directory with `ls`, it’s actually showing only *visible files.* Add the flag `-a` ("all") to your command to see every file, including *hidden* files that start with a “.”

<figure class="caption">
<img src="/static/images/course/cmd/emptydir.jpg" alt="" class="no-shadow"/>
<figcaption>Woah, there are a lot more files in this directory than what it
seemed.</figcaption>
</figure>

Sneaky hidden files! Here’s where the command line shines: It’s really easy to add the `-a` flag to see all files in a directory, whereas in Finder, it’s a lot more difficult to see those hidden files.

What’s even sneakier, is adding a `-l` to the command will show you the files as a list, including the timestamps, and owner information, and other useful things. But because it’s a list, instead of having three or four or five colours, it’s always just one list of file names

<figure class="caption">
<img src="/static/images/course/cmd/lsla.jpg" alt="" class="no-shadow"/>
</figure>
