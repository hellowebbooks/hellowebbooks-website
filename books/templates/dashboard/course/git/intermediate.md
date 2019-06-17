Branching is one of the most useful features of Git. So far, you could imagine your project history as a straight line. Branching allows you to spin off different versions of your project and keep them separate until you want to merge them back together.

<figure class="caption">
<img src="/static/images/course/git/branching.png" alt="" class="no-shadow"/>
</figure>

It’s easy to see the usefulness if you imagine that your project has gotten to a state where you can launch it live. If you want to code a new feature that would take you a few weeks, you can create a separate branch to contain your changes. You can keep your changes separate from the launched, live, working code, and you can commit changes and make your waypoints within your feature branch over time.

Then, you would have your “master” branch (the default name for your main branch) with your working, deployed code, and your “feature” branch that holds your new feature coding progress. That means if you discover a bug in your deployed code, you can fix it and deploy it without having to also deploy your in-progress feature changes.

When you’re ready, Git allows you to merge branches and does it in a fairly smart way. In the previous example, once you’ve fixed the code in the master branch, you can then run `git merge` to bring those changes into your feature branch. And when you finish your feature branch, you can `git merge` that branch into master and deploy it to your customers.

That’s the concept, let’s see it in action!

### Create a new branch with `git checkout -b BRANCHNAME`

Let’s create that "feature" branch:

<figure class="caption">
<img src="/static/images/course/git/git_branch.png" alt="" class="no-shadow"/>
</figure>

We’ll explore more about `git checkout` in a second (it’s how you’ll switch between branches) but adding the `-b` flag will *create* the branch and switch over to it.

### See what branches are available with `git branch`

If you need to remind yourself what branches you’ve created, run the command, `git branch`. I find this particularly useful since I often forget the names of the branches I created.

<figure class="caption">
<img src="/static/images/course/git/git_branch_list.png" alt="" class="no-shadow"/>
</figure>

This is also a handy command to run if you forgot what branch you’re currently on! Also, Git will let you know what branch you’re on when you run `git status`:

<figure class="caption">
<img src="/static/images/course/git/git_status_branch.png" alt="" class="no-shadow"/>
</figure>

### Change what branch you’re on with `git checkout BRANCHNAME`

Now that we can see what branches are available with `git branch`, we can switch between the two with `git checkout BRANCHNAME`.

<figure class="caption">
<img src="/static/images/course/git/git_checkout-1.png" alt="" class="no-shadow"/>
</figure>

### Stash your changes with `git stash` and bring them back with `git stash pop`

Git will whine if you have uncommitted changes in one branch and you try to switch to the other. Git doesn’t want to lose your unsaved progress, and doesn’t want to assume that this progress should be ported over to the other branch.

If you want to switch branches, you need to save your current progress by either committing it, removing your changes, *or* use something like `git stash`. This command tells Git to move your changes into an invisible bucket. It’s like another dimension (or an unofficial, unlisted branch) that Git will use so you don’t lose your progress. The changes will no longer show up when you run `git status` and this will allow you to move back and forth between branches again.

When you want to bring your changes back, you can use `git stash pop`. This works on any branch, not just the original branch those changes were on. This is useful if you started working on some changes but realized you were on the wrong branch. Since Git will prevent you from changing branches with uncommitted changes, you can `git stash` them, change your branch, and then `git stash pop` to bring them back on the correct branch.

### Take your changes from one branch to another with `git merge`

Finished with the changes on your new branch and want to bring them over to the master branch? We can use `git merge` to combine the two branches.

To test this out, make some changes on your "feature" branch, then move back to the “master” branch by running the command `git checkout master`. You can bring *all* the changes you’ve made to the feature branch over to the master branch with `git merge BRANCHNAME` (`git merge feature` if your branch was named “feature”)

<figure class="caption">
<img src="/static/images/course/git/git_merge.png" alt="" class="no-shadow"/>
</figure>

### Oh no, there’s a conflict!

Git is going to try to be as smart as possible when merging one branch with another, but what happens if things don’t merge nicely? If Git doesn’t know how to merge in changes (like if there were changes to a piece of code in *both* branches, and it doesn’t know if it should keep both changes, or pick one or another), it’s going to leave the decision up to you.

When you run `git merge` it’ll let you know if there were any conflicts and will list out the files with those conflicts. In those files, Git will have added `>>>>>` marks where there is a conflict, and will include *both* versions of the conflicted code, so you can manually pick and choose what to keep and what to lose.

<figure class="caption">
<img src="/static/images/course/git/git_merge_fail.png" alt="" class="no-shadow"/>
</figure>

<figure class="caption">
<img src="/static/images/course/git/git_merge_fail_file.png" alt="" class="no-shadow"/>
</figure>

It’s nice that Git allows us to fix these issues so we don’t accidentally lose any of our hard work when working with branches.
