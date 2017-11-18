'''
Created on Jun 17, 2014

@author: Tyler Luce
'''

import praw
import os
import wikia
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

# Set up and connect to reddit
reddit = praw.Reddit('20xxBot')
print(reddit.user.me())

subredditName = os.environ.get('SUBREDDIT')
subreddit = reddit.subreddit(subredditName)
print("Connecting to r/" + subredditName)
botSig = "\n\n^(*The purpose of this bot is to help provide info on Super Smash Bros. lingo.  If you have any suggestions, problems, or bug reports, please message kirby_freak.  Have a wonderful day!*)"
defineErrorMessage1 = "I'm sorry, I wasn't able to find that term in my database, most likely due to the term not being in my database, a misspelling, or the desired term not coming right after \"define\". "
defineErrorMessage1a = "I've searched the Smash Bros Wiki for you and have included below this message a wiki excerpt and link that might be relevant to the term you asked me. "
defineErrorMessage1b = "I also searched the Smash Bros Wiki, but I could not find what you requested there either. "
defineErrorMessage2 = "If you'd like for the term you asked for to be added to my database, please message kirby_freak or submit the suggestion [here](https://docs.google.com/forms/d/15-tOeDclMP9o69z8OONi0lEY-FPP0XJkWs6LmNLrrC0/viewform?usp=send_form) and he'll look into it! "
defineErrorMessage3 = "A list of terms that 20xxbot recognizes is listed [here](https://docs.google.com/document/d/1dbEVlN6Vqvq9I6nXSpXWslsDuMG7yKFIGcXATlUqwT0/edit?usp=sharing)."

defineErrorMessage = defineErrorMessage1 + defineErrorMessage1b + defineErrorMessage2 + defineErrorMessage3
defineErrorMessageWiki = defineErrorMessage1 + defineErrorMessage1a + defineErrorMessage2 + defineErrorMessage3

noCommandErrorMessage = "I'm sorry, but I couldn't find a valid command after you called for me.  The commands I currently recognize are \"define [term]\", \"help\", and \"info\". "

helpMessage = "I currently have 3 commands: define, help, and info. Define lets you ask me to define a Smash Bros term. Help is what you just used to get info on how to use me. Info is "
helpMessage += "how you ask me for background information on me. To use any one of them, type my name followed by the command.  Example: \"20xxbot info\".  Define has an additional "
helpMessage += "parameter in order to let you ask for specific terms, and so is used as followed: \"20xxbot define [term]\". I can also only recognize one command per comment."

infoMessage = "Hello!  I'm a bot made by kirby_freak, and my goal is to help /r/smashbros users by letting them ask me to define Smash Bros. terms. I was started as a final project for one of "
infoMessage += "kirby_freak's Computer Science classes, and began my work on the /r/smashbros sub on Sunday, June 21st, 2015 very early in the morning.  I am written in Python, "
infoMessage += "and I am hosted on a Raspberry Pi 2 Model B sitting in kirby_freak's basement. If you'd like more info on how I work, feel free to message kirby_freak.  If you'd like "
infoMessage += "information on how to use me, please type \"20xxbot help\" in a comment.  Have a great day!"
reimportFiles = 100

while True:

    if (reimportFiles == 100):
        reimportFiles = 0
        
        ### TERMS NOT FOUND DICTIONARY ###
        #print "Setting up the unfound term dictionary"
        # Get ready to set up the unfound term dictionary
        #unfoundTerms = {}
        #if os.path.exists("UnfoundTerms.txt"):
        #    unfoundFile = open('UnfoundTerms.txt', 'r')
        #else:
        #    unfoundFile = open('UnfoundTerms.txt', 'a+')
        # Set up the unfound term dictionary
        #foundUnfoundKey = False
        #unfoundKey = ''
        #for line in unfoundFile:
        #    line = line.strip('\n')
        #    if foundUnfoundKey == False:
        #        unfoundKey = line
        #        foundUnfoundKey = True
        #    else:
        #        unfoundTerms[unfoundKey] = int(line)
        #        foundUnfoundKey = False
        #unfoundFile.close()
        #print "Finished setting up the unfound term dictionary"
        
        ### CHECKED COMMENTS LIST ###
        print("Setting up the checked comments list")
        # Get ready to set up the checked comments list
        checkedComments = []
        if os.path.exists("CheckedComments.txt"):
            checkFile = open('CheckedComments.txt', 'r')
        else:
            checkFile = open('CheckedComments.txt', 'a+')
        # Set up the checked comments list
        for line in checkFile:
            line = line.strip('\n')
            checkedComments.append(line)
        checkFile.close()
        print("Finished setting up the checked comments list")
        
        # Clean up Checked Comments list
        checkedCommentsCopy = list(checkedComments)
        checkedCommentsCopy.reverse()
        checkedComments = []
        commentNum = 0
        checkFile = open('CheckedComments.txt', 'w').close()
        
        for comment in checkedCommentsCopy:
            checkedComments.append(comment)
            checkFile = open('CheckedComments.txt', 'a')
            checkFile.write(comment + '\n')
            checkFile.close()
            commentNum += 1
            if commentNum == 1200:
                break
        
        
        ### TECH DICTIONARY ###
        # Get ready to set up the tech dictionary
        print("Setting up the tech dictionary")
        dictFile = open('TechList.txt', 'r')
        techDict = {}
        readingName = False
        readyToAdd = False
        techName = ''
        techDescription = ''
        # Set up the tech dictionary
        for line in dictFile:
            line = line.strip('\n') #Remove newline characters from the line
            if line == '&':
                readingName = True
                # If there is a key-value pair ready to be set, do it and get ready to read in another pair
                if readyToAdd:
                    #print techName
                    techDict[techName] = techDescription
                    techName = ''
                    techDescription = ''
                    readyToAdd = False
            # If the & line was just read in, this line is the technique's name
            elif readingName == True:
                techName = line
                readingName = False
            # If the line isn't a & line and wasn't just read in, then start adding the technique's descriptions
            else:
                techDescription += line + ' '
                readyToAdd = True
        # Add in the last technique key-value pair and close the file
        techDict[techName] = techDescription
        dictFile.close()
        print(techDict.keys())
        print("Tech dictionary is set up")
        
        ### TECH KEYWORD DICTIONARY ###
        # Get ready to set up the tech keyword dictionary 
        print("Setting up the tech keyword dictionary")
        keywordFile = open('KeywordList.txt', 'r')
        keywordDict = {}
        startNewKeyword = True
        keywordKey = ''
        keywordValue = ''
        #Set up the tech keyword dictionary (the dictionary has a key-value pair style of "keyword variation : actual keyword")
        for line in keywordFile:
            line = line.strip('\n') #Remove newline characters from the line
            if line == '&':
                startNewKeyword = True
            # If a new keyword is being added, set it to the new keywordValue and add it to the dictionary with itself as a key
            elif startNewKeyword == True:
                keywordKey = line
                keywordValue = line
                keywordDict[keywordKey] = keywordValue
                startNewKeyword = False
            # Add a variation of the keyword as a key with the actual keyword as a value
            else:
                keywordKey = line
                keywordDict[keywordKey] = keywordValue
        dictFile.close()
        print(keywordDict.keys())
        print("Tech keyword dictionary is set up")
    
    # Get recent comments from the subreddit
    print("Getting new comments from /r/"+subredditName+"... ")
    try:
        comment_generator = subreddit.comments(limit = 1000)
    except:
        print("!! Exception thrown when getting new comments!!")
    
    print("Checking comments for calls (loop " + str(reimportFiles) + ")")
    
    # Loop through all the new comments
    skipComment = False
    try:
        for comment in comment_generator:
            # Check if the comment has been checked before.  If it has, skip it.
            for checked in checkedComments:
                if checked == comment.id:
                    skipComment = True
                    break
            if skipComment:
                continue
            sliced_comment = comment.body.split()
            
            # Variables for checking keywords
            botKeyword = False
            defineKeyword = False
            techKeyword = False
            techKeywordCheckedFor = False
            commentCommandError = True
            techAskedFor = ''
            
            # Loop through every word in the comment
            for word in sliced_comment: 
                loweredWord = word.lower()
                # Check if the user is calling for the 20xxbot
                if loweredWord == "20xxbot":
                    botKeyword = True
                    print("")
                    print("Found keyword '20xxbot'")
                # If there are more words, check if next is a keyword, else inform user how to correctly call the bot
                elif botKeyword == True:
                    # If a keyword that is supposed to follow "20xxbot" has not been found yet, check if it's the current word.  If not, then the syntax is wrong.
                    if defineKeyword == False:
                        if loweredWord == "define":
                            defineKeyword = True
                            commentCommandError = False
                            print("Found keyword 'define'")
                        elif loweredWord == "help":
                            commentCommandError = False
                            print("Found keyword 'help'")
                            replyText = str(helpMessage) + str(botSig)
                            try:
                                comment.reply(replyText)
                            except:
                                print("!! Exception thrown when replying to comment!!")
                            print("Replied to the comment with info on how to use me")
                            break
                        elif loweredWord == "info":
                            infoKeyword = True
                            commentCommandError = False
                            print("Found keyword 'info'")
                            replyText = str(infoMessage) + str(botSig)
                            try:
                                comment.reply(replyText)
                            except:
                                print("!! Exception thrown when replying to comment!!")
                            print("Replied to the comment with background info on me")
                            break
                        else:
                            botKeyword = False
                            print("No valid keywords found after 20xxBot was called")
                        
                    # if define keyword was found previously but no tech keyword has been checked for, check for one (the words after will not be checked)
                    elif techKeywordCheckedFor == False and defineKeyword == True:
                        techKeywordCheckedFor = True
                        print("Checking for valid tech keywords")
                        # Loop through all the valid keywords and see if they're in the comment
                        for key in keywordDict.keys():
                            sliced_key = key.split()
                            # Only check if the key is there if there enough words in the comment remaning for it to fit
                            if len(sliced_comment) >= sliced_comment.index(word) + len(sliced_key):
                                techKeywordValid = True
                                # Check each following word to see if they match the keyword words.  If they don't, the keyword isn't there
                                for i in range(0, len(sliced_key)):
                                    if sliced_comment[sliced_comment.index(word) + i].lower() != sliced_key[i]:
                                        techKeywordValid = False
                                        break
                                # If the techKeyword was found, use it to get the keyword from the tech keyword dictionary that the tech dictionary will recognize
                                if techKeywordValid == True:
                                    techAskedFor = keywordDict.get(key)
                                    techKeyword = True
                                    print("Found " + key + ", a valid keyword.  Registered " + techAskedFor + " to be defined.")
                                    replyText = str(techDict.get(techAskedFor)) + str(botSig)
                                    try:
                                        comment.reply(replyText)
                                    except:
                                        print("!! Exception thrown when replying to comment!!")
                                    print("Replied to the comment with the definition of " + techAskedFor + '\n')
                                    break
                            #else:
                                #print "Comment was not long enough to contain a tech keyword following define"  
                        # If the techKeyword could not be found, save the asked term that wasn't in the database
                        if techKeywordValid == False:                       
                            print("Getting missing term...")
                            missingTerm = ""
                            for i in range(0, len(sliced_comment) - sliced_comment.index(word)):
                                missingTerm += sliced_comment[sliced_comment.index(word) + i].lower() + " "
                    # If a tech keyword has been checked for, stop checking the comment
                    else:
                        break
                # Make sure the bot only replies to comments that have called it
                else:
                    commentCommandError = False
            # Term could not be found in database, respond appropriately
            if defineKeyword == True and techKeyword == False:
                wikiSearchSuccesful = True
                try:
                    wikiSearchResult = wikia.search("smashbros", missingTerm, results=10)[0]
                    wikiSearchSummary = wikia.summary("smashbros", wikiSearchResult, chars=500, redirect=True)
                    wikiSearchURL = wikia.page("smashbros", title=wikiSearchResult, pageid=None, redirect=True, preload=False).url
                    #Make links that end with ) work
                    if wikiSearchURL[len(wikiSearchURL)-1] == ')':
                        print("Fixing wiki link")
                        wikiSearchURL = wikiSearchURL[:len(wikiSearchURL)-1] + '\\' + wikiSearchURL[len(wikiSearchURL)-1:]
                        #print wikiSearchURL
                except:
                    print("!! Exception thrown when searching the Wiki!!")
                    wikiSearchSuccesful = False
                    print(wikiSearchSuccesful)
                try:
                    if wikiSearchSuccesful == True:
                        URLMessage = "\n\nYou can find more info at this [SmashPedia](%s) link. " % wikiSearchURL
                        comment.reply(defineErrorMessageWiki + "\n\n" + wikiSearchSummary + URLMessage + botSig)
                        print("Did not find a valid tech keyword. \nCommented with instructions containing correct syntax and a possible summary.")
                    else:
                        comment.reply(defineErrorMessage + botSig)
                        print("Did not find a valid tech keyword. \nCommented with instructions containing correct syntax.")
                except:
                    print("!! Exception thrown when replying to comment!!")
                # Add unfound term to the dictionary
                #if unfoundTerms.has_key(techAskedFor):
                #    unfoundTerms[techAskedFor] += 1
                #    unfoundFile = open('UnfoundTerms.txt', 'w')
                #    for key in unfoundTerms:
                #        unfoundFile.write(key + '\n')
                #        unfoundFile.write(str(unfoundTerms[key]) + '\n')
                #    unfoundFile.close()
                #else:
                #    unfoundTerms[techAskedFor] = 1
                #    unfoundFile = open('UnfoundTerms.txt', 'a')
                #    print techAskedFor
                #    unfoundFile.write(techAskedFor + '\n')
                #    unfoundFile.write("1\n")
                #    unfoundFile.close()
                print("")
            if commentCommandError == True:
                # comment.reply(noCommandErrorMessage + botSig)
                print("20xxbot was called but no valid commands were given.  Did not respond to user.")
                
            # Add comment to the checkedComment list and to the text document
            checkFile = open('CheckedComments.txt', 'a')
            checkFile.write(comment.id + '\n')
            checkFile.close()
            checkedComments.append(comment.id)
            print("Added comment to not be checked again.")
    except:
        print("!! Exception thrown while looping through comments!!")
    
    print("")
    reimportFiles += 1
