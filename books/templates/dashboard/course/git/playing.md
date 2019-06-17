First, we need to install Git. It’s easy, I promise you, but for the sake of keeping this guide short, please head over to this very useful guide here for installation: [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

All good?

Let’s start things out by creating a project folder and a file within that folder, and we’ll use this as our Git playground.

<figure class="caption">
<img src="/static/images/course/git/Start.jpg" alt="" class="no-shadow"/>
<figcaption>Create a directory and a file in your command line or in your code editor,
whichever works best for you.</figcaption>
</figure>

### Initialize Git with `git init`

Git will only track the projects you tell it to track, so let’s tell Git to track this project folder with `git init`.

<figure class="caption">
<img src="/static/images/course/git/init.png" alt="" class="no-shadow"/>
</figure>

Git will create a hidden folder where it’ll keep track of things. The only file here that you might touch down the line is the `.git/config` file, but 99% of the time you don’t need to worry about what’s going on in the background. But it’s useful to know about that directory because if you wanted to remove Git and the history of your project, you can delete that folder.

If this is your very first time using Git, it’ll be useful to tell it your preferred username and email. We’re going to tell it, with the `--global` flag, to save this universally on your system so you don’t have to tell it these things again later.

Type these into your terminal:

```
git config --global user.name 'YOUR_PREFERRED_USERNAME'
```

```
git config --global user.email 'YOUR_EMAIL'
```

### See the current status of your project with `git status`

`git status` is probably the command you’ll be running the most! Type it into your terminal:

<figure class="caption">
<img src="/static/images/course/git/Status.png" alt="" class="no-shadow"/>
<figcaption>Git is letting us know that nothing has been committed and that we have one untracked file.</figcaption>
</figure>

`git status` will tell you what files are being tracked and whether there are changes made that haven’t been "checked-in" yet. Here, we can see that Git is running for this directory, but it isn’t currently tracking any files. It wants to be smart and not assume all files in a directory should be tracked, leaving it up to you to tell it what to follow.

### Tell Git to track files with `git add`

We have several different ways to tell Git to track a file:

`git add FILENAME`

*You can explicitly tell it to track current files by specifying the file name.*

`git add FILENAME FILENAME FILENAME FILENAME`

*Want to do multiple files in one command? Just list them out!*

`git add .`

*Tell Git to add all with a dot*

The last command is the command I personally use the most. The dot indicates all files here so everything in this directory will be tracked. This is great for something like a Django project, where there will be at least 10 files created and it would be a typing pain to type them all out for Git to track.

We might not want to add *everything* to Git, but we’ll worry about that a bit later.

Go ahead and create a file in your project directory (*testing.txt* or whatever
you like), and add it to your Git repository (otherwise known as a *repo*):

<figure class="caption">
<img src="/static/images/course/git/git_add.png" alt="" class="no-shadow"/>
</figure>

### What about removing files?

The command `git rm FILENAME` will remove the file both from Git *and* from your computer. You’re deleting the file.

If you want to just remove the file *from Git* but *keep* the file on your computer, you’ll need to pass in the `--cached` flag. So: `git rm --cached FILENAME`.

This isn’t something that should be run often at all, but useful to know just in case.

### Check status again with `git status`

Now that we’ve told Git to track some files, run `git status` again to see what changed. We can see that the file we created earlier is here, and Git is letting us know that it hasn’t been saved yet into our Git history.

<figure class="caption">
<img src="/static/images/course/git/git_status_after_add.png" alt="" class="no-shadow"/>
</figure>

Let’s create our first waymarker in our history — our very first commit!

### Save your current status with `git commit`

Let’s commit our current status into the Git history, and write a message to go along with it:

`git commit -a -m "First commit"`

<figure class="caption">
<img src="/static/images/course/git/git_status_after_add.png" alt="" class="no-shadow"/>
<figcaption>Your numbers might be different but everything else should essentially be the same!</figcaption>
</figure>

The `-m` flag tells Git that you want to include a message, which should be done with pretty much every commit. These messages will be included in Git’s logs and allows future-you to know why you committed at that moment, like, "Fixed homepage bug related to issue #776." Since this is our very first commit, let’s just say that.

_***Note***: If you don’t add a message, Git will open up an editor (using vim by
default, which can be confusing to learn). So remember to always add a message
when committing, even if it’s “WIP” (and if you get stuck in the vim editor,
type :wq to leave.)_

I also added the `-a` flag, which is to indicate that you want to commit all files. By default, if you made another change to your file and did another commit, Git would ask you to explicitly add it again (with `git add`). The `-a` flag is a shortcut that tells it to go ahead and add all files to the commit *that are already being tracked* by Git. Brand new files will still need to be explicitly added with `git add`. For me, at this point, I add `-a -m "Message"` to every commit as a habit since I almost never want to commit without those flags.

Run `git status` again:

<figure class="caption">
<img src="/static/images/course/git/git_status_after_commit.png" alt="" class="no-shadow"/>
<figcaption>Your numbers might be different but everything else should essentially be the same!</figcaption>
</figure>

Voila! Git is telling you everything is normal and nothing has changed since your last commit. Everything is checked in!

### You’re tracking your files! Now what?

Now that you’ve started tracking your project files and have made your first commit, you can keep on working. Remember to do a commit every now and again to save your progress when everything is good. Working for a few weeks and checking in a bunch a files at the end with tons of code changes isn’t as helpful as committing whenever you achieve a milestone (which could be finishing a small feature, or completing a chapter in a tutorial, or finishing up your work for the day.) This is especially good if you’ve tied your Git repo in with GitHub or GitLab, as then your work is often backed up at an external source

I totally understand that it’s easy to get wrapped up in programming and forget where you’re at or what you’ve done since your last commit. I personally do this so often! Committing with a less-than-helpful message like "Oh no, haven’t committed in a while, I’m working on so-and-so feature" is better than not committing your work at all.

### Wait, what changed? See differences with `git diff`

Remember that `git status` is available at all times to see what files have changed since the last time you’ve committed. If you haven’t committed in a while and notice that, after running `git status`, a file has changes that you don’t remember, you can use the command `git diff FILENAME` to see the specific changes in that file.

![A lot of gobbledegook! It’s comparing the before and after of the file and at
the bottom of the output, you can see I added a new line to my
file.](images/git_diff.png)

If you leave off the filename, `git diff` will show you all the changes across all your files. This is a nice way to review your work before making a commit and check it for things that you actually don’t want to check in (like debugging statements and whatnot.)

### Make another commit, and then check history with `git log`

Something you probably won’t use very often but is still very useful is `git log`. This’ll output a list of your commits with their messages and dates so you can see all your history at a glance.

Make a new commit and then run `git log`:

<figure class="caption">
<img src="/static/images/course/git/git_log.png" alt="" class="no-shadow"/>
<figcaption>Our two commits so far! Newest is on top.</figcaption>
</figure>

Nice! To exit this screen, just press "q" to quit. We’ll return back here soon.

### Ack, don’t want to commit those changes? Go back to your last checked-in version with `git checkout`

Say you’re working on a feature, and you fall into a rabbit-hole making changes
on a file and, at the end, decide that you did the wrong thing and want to start
over (I am often guilty of this). Rather than *UNDO*-ing all the way back to your starting point, you can return back to your last committed version of that file with `git checkout FILENAME`.

To see this in action, make some silly changes to a file, and then confirm the changes were made with `git status`. Then run `git checkout` on the file. Tada, you’re back to the last checked-in version!

<figure class="caption">
<img src="/static/images/course/git/git_checkout.png" alt="" class="no-shadow"/>
<figcaption>Tada: After checking out our file, it’s returned back to the state it was in when it was last committed.</figcaption>
</figure>

Remember when you ran `git log` and every commit had a random string assigned to it that looked like `commit 5e4943f93ad5c242a51c1d6a19d6be5d09c938fd`? You can also use `git checkout COMMITHASH` to go back in time to that commit entirely. This is how you can hop back and forth in time to different states of your code, if you like.

### Have files you don’t want to track? Set up your *.gitignore* file

We want to save the history of our code, but there are a lot of other files involved in programming that we don’t want to save or share. For example, the plugins we install or files with sensitive information that we don’t want to publish on GitHub.

We can list out those files and directories in our .*gitignore* file. These aren’t added by Git when we initialize the repository with `git init` — we’ll create the file manually and save it in the right place, and Git will automagically read the file and ignore files and directories that match what’s in our ignore file.

The name of the file is important (make sure to include the "." at the front of “.gitignore”). It should live next to the hidden .git directory.

To test this out, let’s create a dummy file called "ignoreme.txt." First, check that Git sees it with `git status`:

<figure class="caption">
<img src="/static/images/course/git/gitignore.png" alt="" class="no-shadow"/>
</figure>

Next, create a .gitignore file and put it at the root of your project, where your .git directory is. Within the .gitignore file, put "ignoreme.txt" at the top of the file and save. If we run `git status` again, we can see that the .gitignore file was added, but the *ignoreme.txt file* is no where to be found. Git is successfully ignoring that file!

<figure class="caption">
<img src="/static/images/course/git/gitignore_after.png" alt="" class="no-shadow"/>
<figcaption>You can also create the file using your text editor if that’s easier.</figcaption>
</figure>

There’s a great resource on GitHub that lists out sample *.gitignore* files based on your project type (like Python or JavaScript projects), listing out the typical files that people ignore. You can see and copy the templates here: [https://github.com/github/gitignore](https://github.com/github/gitignore)

### Part 1, finished! You now know the basics of Git

The commands we’ve covered here are the commands that I personally run 95% of the time in all of my projects. To reiterate:

* Initialize Git with `git init`

* Add files to track with `git add` (either everything with `git add .` or individual files with `git add FILENAME`)

* Commit your current progress with `git commit` (adding the `-a` flag to commit
all changes and `-m` flag to add a message, so the command is `git commit -a -m
"Commit message!"`)

* See the changes with `git diff` (either in one file with `git diff FILENAME` or all changes with just `git diff`)

* Return to the last-checked-in version with `git checkout` (either just one file with `git checkout FILENAME` or return to a previous commit with `git checkout COMMITHASH`, which you would see after running `git log`)

* If you decide you don’t want Git to track a file, add it to your `.gitignore` file.

Phew! I promise it’ll become second nature with enough practice.
