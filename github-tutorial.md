# How to Add Empty Folders to a GitHub Repo

### 1. Open a terminal window and change directories to where you want to add the 360i repo
```
sam@framework:~$
cd src
```

I use a base directory called "src" for my repos. If you don't have a directory that you want to use, you'll have to create one to use using the mkdir command, and then use cd to navigate to that directory.
```
mkdir src
```

### 2. Go to CDISC GitHub and click on the 360i repo. 

Click on the green <> Code button in the upper right corner of the repo. Select the icon to copy the https url. Now we'll clone that repo which will basically download the contents of the repo to your harddrive.
```
git clone https://github.com/cdisc-org/360i.git
```

If you get a message asking for a user name and password, and it does not allow you to clone the repo, then you may need a token to use for authentication. This happens with 2FA enabled. I can walk you through creating one in GitHub (or try Google). You then add that token (a long string of numbers and letters), to the repo URL. It'll look something like this (but your token will be different):
```
git clone https://ghp_9IZWTev5vpLotsOfLettersAndNumbers@github.com/cdisc-org/360i.git
```

### 3. Change to the 360i directory
```
cd 360i
```

Then list the contents of the directory to see what was downloaded.
```
ls -l
```

You'll see the contents of the repo listed.

### 4. Create a branch to work in
You can skip this step if you'd like, but sometime you'll need to learn to do this. It's a better method when multiple people are collaborating on content. If I want to create a branch called "folder_structure" and start to work in it, here's what I do
```
git checkout -b folder_structure
```

You'll get a message that says "Switched to a new branch 'folder_structure'"

### 5. Git status
Git status is a great command to use to understand the current state of your local repo. There's no reason you need to do it now, but it's not a bad habit to build.
```
git status
```

### 6. Create a folder
Now create your first new folder called DHT.
```
mkdir DHT
```

List the directory to see your new folder.
```
ls -l
```

### 7. Add the .gitkeep file
You need to add an empty .gitkeep file into the directory for Git to acknowledge the empty directory. Otherwise, it will ignore the directory until there's a file in it.
```
touch DHT/.gitkeep
```

Then list the contents of the directory to ensure the file was created.
```
ls -la DHT
```

You should see the .gitkeep file in the DHT directory.

### 8. Add changes to be committed
Next you need to add the changes to be committed.
```
git add .
```

You can check the results with `git status` to show that it's listed under "changes to be committed".

### 9. Commit the changes
Commit the changes and add a short message to name the changes.
```
git commit -m "adds DHT folder"
```

### 10. Push the changes to GitHub
Now you'll push the committed changes to the GitHub repo. Again, you may need your GitHub token to do this. The example I'll show will include a (fake) token.

Here's a template for the command:
```
git push https://<GITHUB_ACCESS_TOKEN>@github.com/<GITHUB_USERNAME>/<REPOSITORY_NAME>.git
```

Here's an example of the command you will run:
```
git push https://ghp_9IZWTev5vpLotsOfLettersAndNumbers@github.com/cdisc-org/360i.git
```

You should get a message stating that it uploaded the new content and created the new branch

### 11. Go to GitHub and create a Pull Request
Go to the 360i repo in your browser. You should see a message stating it received your recent push with a button "Compare & pull request". Click that button. This will take you to another screen where you should see another green button "Create pull request". Click that button.

Now it may allow you to merge that Pull Request (PR). If so, just click on the green button "Merge pull request" then click on another green button "Confirm merge". Now your done and if you go back to the main repo page you'll see your new folder.

Depending on your permissions, it may ask me to review and confirm the merge. We do that for most repos to add a review process and to limit who can commit changes to the main branch. If so, just ping me on slack or we can hop on a call.

### 12. Repeat
Actually, you can do this with all your folders in one shot. If you want to add more folder you can repeat the process starting with step 6.
