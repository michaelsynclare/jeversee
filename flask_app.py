


## Jeversee Movie Data Grabber



b = "+" * 50

## If the modules are missing try these commands in the terminal...
#python -m pip install requests
#python -m pip install bs4

## IMPORT THE SCRAPER LIBRARY
import requests

## IMPORT THE FORMATTER AND EXTRACTOR LIBRARY
from bs4 import BeautifulSoup

## IMPORT the RE LIBRARY (aka RegExpressions, aka RegEx module)
import re

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


m = "unavailable" #"**missing**"

absoluteLinkInput = "../jeverseeMovieDataGrabber.py"
absoluteLinkProcess = ".."

linkStyling = "color:#00b300;text-decoration:none"

tryAgain = ""

## Logic limitation: if there are multiple films with the same title and release
## year then you will just see the most popular/recent of them.
## If user includes a year, then the search can be (needs work, maybe parens?) much more accurate.


"""
## THIS IS A GREAT SCRAPE TESTER TO SEE WHAT SOUP GETS FROM A WEBPAGE

## Request and soup-element the content of a specific URL
url_Test = (f"https://www.themoviedb.org/search?language=en-US&query={movTitleRT}")
## The Requests module makes this unique var type: 'requests.models.Response'

response_Test = requests.get(url_Test)
#time.sleep(delay)
## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
soup_TestMovPage = BeautifulSoup(response_Test.content, 'html.parser')

foundTags_TMDB_searchResults = soup_TestMovPage.find('a', attrs={'class':'contributor'})

print(":: foundTags_TMDB_searchResults:",foundTags_TMDB_searchResults.get_text())
"""







def inputMovTitleAndYear():

    global foundTags_RT_results,url_RT_search,movTitleInput,movYear,tryAgain,foundTags_RT_resultsRaw

    ## This makes the terminal output easier to read.
    print("////////////////////////////////////////")
    print("////////////////////////////////////////")
    print(" ")

    while True:

        #region

        ## THIS STARTS A REGION OF MODIFIED STUFF SO I CAN INTEGRATE THE HTML FORM INPUT _________________________________________

        ## HARDWIRE THE INPUT HERE TO DO TERMINAL WORK (also around lines 776, 1080, and 1087)
        #movTitleInput = "splinter"

        ## Capitalize the first letter of each word in the title
        movTitleInput = movTitleInput.title()

        ## THIS ENDS A REGION OF MODIFIED STUFF SO I CAN INTEGRATE THE HTML FORM INPUT _________________________________________

        #endregion


        ## Input parsing letting the customer just use one question to get both values.
        ## Shorthand if-conditional with a nested for-loop.
        ## If any character in the input string is a number, find_al them and assign them as the movYear var.
        if any(character.isdigit() for character in movTitleInput):
            #print(":: yes there are digits here!")

            ## Find any 4 digit numbers from the input and make it a separate var.
            movYear = re.findall(r"\d{4}",movTitleInput)
            #movYear = ''
            #print(":: movYear before if statement:", movYear)
            if movYear == []:
                print(":: movYear if-empty triggered!!!:",movYear)
                movYear = ""
                pass
            else:
                movYear = str(movYear[0])

            #movYear = ''.join(movYear)
            ## This removes the 4 digit numbers from the input once they've been assigned to the movYear var.
            movTitleInput = re.sub(r'\d{4}','',movTitleInput)
            movTitleInput = str(movTitleInput.strip())

            ## Replace any digits that are not years with the written version.
            movTitleInput = movTitleInput.replace('0', 'zero').replace('1', 'one').replace('2', 'two').replace('3', 'three').replace('4', 'four').replace('5', 'five').replace('6', 'six').replace('7', 'seven').replace('8', 'eight').replace('9', 'nine')

            movTitleInput = movTitleInput.replace('()', '')

            ## If a movie title is a year, then just search the year and erase the movYear var. (the 1917 and 2001 logic)
            if movTitleInput == '':
                movTitleInput = movYear
                movYear = ''

            #if movYear == ' []':
                #movYear = 'x'

            '''
            ## I dont understand why I must use re,findall instead of movTitleInput.find_all here,  to avoid an AttributeError.
            ## Matches one (\d) or more (+) digits.
            movYear = re.findall(r'\d+', movTitleInput) #movYear = re.findall(r"\d{4}",movTitleInput)
            ## Convert the single item list into a str.
            movYear = str(movYear[0])
            ## Replace any digits in the movTitle with bitter nothingness.
            movTitleInput = re.sub(r'\d+', '', movTitleInput)
            '''
            print(":: movYear:", movYear)
            print(":: movTitleInput:", movTitleInput)

        else:
            ## Remove the movie year from the query.
            movYear = ""

        ## Replace underscores with dashes. Make sure that spaces aren't inferior to other delimiters for RT search quality.
        movTitleInput = movTitleInput.replace(" ", "-")


        ## Request and soup-element the content of the RT search URL.
        ## Make sure that I do not add movYear to this string or else RT search really messes up. Let the year be processed and compared to results later.
        url_RT_search= (f"https://www.rottentomatoes.com/search?search={movTitleInput}")
        response_1 = requests.get(url_RT_search)
        ## Response.content pulls raw response HTML as bytes more accurately than 'response.text' does.
        soup_RTSearchHTML = BeautifulSoup(response_1.content, 'html.parser')


        """
        ## Response.content pulls raw response HTML as bytes more accurately than response.text
        print(response.text) ## Response .text is Unicode.
        print(response.status_code) ## Checks for and prints the sought-after "success 200" message!
        """

        ## Some neat BS4 soup methods.
        ## The .prettify method prints well-formatted HTML. Not helpful for me since i prefer studying the actual page view-source code.
        #print(soup_RTSearchHTML.prettify())
        ## Prints raw-ish HTML.
        #print(":: soup_RTSearchHTML:",soup_RTSearchHTML)
        ## The .title method pulls the page title.
        #print("\ntitle method:",soup_RTSearchHTML.title())


        ## Search RT and get some possible movie results.
        ## This uses find, not find_all, so you only get the first result that matches.
        if movYear == "":
            ## If a movYear was provided, scrape these certain non-tv tags.
            ## This is where I changed the find to find_all and added the for loop below to tweak RT initial choices.
            foundTags_RT_results = soup_RTSearchHTML.find('search-page-media-row', attrs={'start-year': ''})
            #print(":: foundTags_RT_results without movYear triggered.")

        else:
            ## Only grab the search result links where the releaseyear value exists (tv results dont have it) and also matches the user movYear input.
            foundTags_RT_results = soup_RTSearchHTML.find('search-page-media-row', attrs={'release-year': movYear})
            #print(":: foundTags_RT_results with movYear triggered.")



        ## This grabs raw html tags to use in the "Did you mean to choose..." feature.
        foundTags_RT_resultsRaw = soup_RTSearchHTML.find_all('search-page-media-row', attrs={'start-year': ''})
        #print(":: foundTags_RT_resultsRaw:,",foundTags_RT_resultsRaw)



        break

        """
        ## If no tags are found and the user gave a year, tell the user and ask again.
        if foundTags_RT_results == None and movYear != "":
            print("\nNothing found with that year, try again! (1) \n")
            ## TryAgain is an advanced logic that makes the user give better input instead of just making RT's best guess based
            ## mostly on recency and popularity. It also requires more html looping on the input page before sending to the jvs page.
            tryAgain = "\nThis should be TRY AGAIN, but we pushed forward! (1)"
            break
        ## If no tags are found and the user did not give a year, tell the user and ask again.
        elif foundTags_RT_results == None:
            print("\nNothing found, try again! (2) \n")
            tryAgain = "\nThis should be TRY AGAIN, but we pushed forward! (2)"
            break
        ## If no tags are found and the user did not give a year, tell the user and ask again.
        elif not foundTags_RT_results:
            print("\nNothing found, try again! (3) \n")
            tryAgain = "\nThis should be TRY AGAIN, but we pushed forward! (3)"
            break

        ## If a good RT movie result is found, then process it further.
        else:
            ## Break gets you out of the loop and continues to the code below and then left one indent level.
            break
        """


    #print("\n:: foundTags_RT_results:\n", foundTags_RT_results)
    print(":: url_RT_search:",url_RT_search,"\n")


    ## This was a temp fix that might be needed again later.
    #foundTags_RT_resultsRaw = foundTags_RT_results


    """
    ## Here Im able to adjust RT's initial movie choice. I'm currently skipping results with no images.
    ## I should also consider skipping results with no tomato scores for example.
    iter = 0
    counter = 0
    for x in foundTags_RT_results:
        x.get_text()
        #print(":: all RT results before selection:",x)
        src = x.find('img')
        ## Grabbing attrs and turning specific values into new vars.
        attributes_8 = src.attrs
        ## Set the img tag's src attr as a var.
        srcLinks = attributes_8['src']

        ## Remove the options with no thumbnail image. Junky movies basically.

        if "gif" not in srcLinks:
            print(":: no gif result (a good RT result):",x)
            foundTags_RT_results = x
            ## This if condition ensures that only the first no gif result is chosen.
            counter = counter + 1
            if counter == 1:
                break
        else:
            print(":: skipped because gif found:",x)
            pass

        iter = iter + 1
        if iter == 5:
            break
        """

    #print(":: foundTags_RT_results...:",foundTags_RT_results)

    ## Move forward to the next func.
    #print(":: About to process the input()")

    print(":: movTitleInput:",movTitleInput)

    if movTitleInput == "":
        print("movTitleInput was empty!")
        movTitleInput = "try again"
        inputMovTitleAndYear()
    elif movTitleInput == None:
        print("movTitleInput had no results!")
        movTitleInput = "no results"
        inputMovTitleAndYear()
    else:
        print("movTitleInput was NOT empty.")
        processTheInput()

    #processTheInput()



def processTheInput():

    global html_content,foundTags_RT_results,movTitleInput

    ## I dont need many global vars here because the script ends within this function right?
    ## Do any var values need to be called out of this function? TEST




    ## Grabbing attrs and turning specific values into new vars.
    ## .attrs is a bs4 mechanism that creates a dictionary of attrs and values.

    print(":: movTitleInput and movYear BEFORE the nothing found attributes_1 error:",movTitleInput,movYear)
    '''
    attributes_1 = foundTags_RT_results.attrs

    '''
    try:
        attributes_1 = foundTags_RT_results.attrs
    #print(":: attributes_1:",(attributes_1))
    except Exception as e:
        print(f"Error processing input! ERROR: {e}")
        movTitleInput = "cheese"
        render_html()
        #pass


    ## If either attribute version of release-year score exists, scrape it and assign it to a var.
    if 'release-year' in attributes_1:
        releaseYear = attributes_1['release-year']
    elif 'releaseyear' in attributes_1:
        releaseYear = attributes_1['releaseyear']
    else:
        pass

    #print(":: releaseYear:",releaseYear)

    ## Cast seems to always exist, so I don't need the if statement, I can just scrape and assign it to a var.
    cast = attributes_1['cast']
    cast = cast.replace(",", ", ")



    ## If either attribute version of tomatometer score exists, scrape it and assign it to a var.
    if 'tomatometer-score' in attributes_1:
        rtScore = attributes_1['tomatometer-score']
        if rtScore == '':
            rtScore = 0
        #print(":: rtScore A:",rtScore)
    elif 'tomatometerscore' in attributes_1:
        rtScore = attributes_1['tomatometerscore']
        if rtScore == '':
            rtScore = 0
        #print(":: rtScore B:",rtScore)
    else:
        #print(":: rtScore C:",rtScore)
        pass

    #print(":: rtScore D:",rtScore)

    ## Finishing the tomatometer score with colors and a % sign.
    #print(":: rtScore type:",type(rtScore))
    if int(rtScore) >= 80:
        rtScore = f"<span style=\"color:green\">{str(rtScore)+'%'}</span>"
    elif 40 <= int(rtScore) < 80:
        rtScore = f"<span style=\"color:yellow\">{str(rtScore)+'%'}</span>"
    elif 0 < int(rtScore) < 40:
        rtScore = f"<span style=\"color:red\">{str(rtScore)+'%'}</span>"
    else:
        rtScore = m
        pass

    #print(":: pcScore type:",type(pcScore))
    rtScore = str(rtScore)





    ## If the attr values are missing or incomplete, then change the value to 'missing'.
    if rtScore == "":
        rtScore = m
    if rtScore == "%":
        rtScore = m
    if cast == "":
        cast = m
    if releaseYear == "":
        releaseYear = m


    ## Make this score a complete html line. Can this be moved up about 15 lines? TEST
    rtScore = f"<strong>{rtScore}</strong> - Rotten Tomatoes Score"




    ## Scraping the unchosen RT options for the 'Did you mean to choose?' feature.
    ## Define an empty list to append the unselected html tag block results to.
    i = 0
    unselectedRTresultsList = []
    for x in foundTags_RT_resultsRaw:
        ## For each item, scrape the anchor title text and strip the whitespace away.
        src = x.find('a', slot='title')
        ## The method strip() removes all whitespace from the left and right.
        src = src.get_text().strip()
        ## For each item, scrape the releaseyear value.
        movieConfirm_rl = x.get('release-year')

        ## Ignore the tv results and process the confirmed movies.
        if movieConfirm_rl == None:
            pass
            print(":: This is not a movie, so skip this result.")
        ## Don't include the movie itself in the unselection options list.
        elif movieConfirm_rl == releaseYear:
            pass
            #print("\n:: The years match, so skip this result for did-you-mean.",x)
        ## Format the results into full JVS html links and add them to the movie list.
        else:
            x = f"<a style=\"{linkStyling}\" href=\"{absoluteLinkProcess}/jeverseeMovieDataGrabber.py?movTitleInput={src.replace(' ','+')} ({movieConfirm_rl})\">{src} ({movieConfirm_rl})</a>"
            unselectedRTresultsList.append(x)
            #print(":: Good ELSE result.",x)
            i = i + 1
            ## Provide only the first 2 other selection choices.
            if i == 2:
                break


        #print(":: movieConfirm_rl:",movieConfirm_rl)
        #print(":: all RT result anchor tags before selection:",src)

    ## Reformat the list using the join method. This removes the list brackets.
    unselectedRTresultsList = (" or ".join(unselectedRTresultsList))


    #print("\n:: unselectedRTresultsList:",unselectedRTresultsList,"\n")

    if unselectedRTresultsList == "":
        pass
    else:
        unselectedRTresultsList = f"Did you mean to choose: "+unselectedRTresultsList+" ?"





    ## This is the moment of actual RT mov search result selection.
    ## Grab the first RT link from the RT search found tags to "narrow down the scraping". Narrowing works.
    sources = foundTags_RT_results.find('img')
    ## Grabbing attrs and turning specific values into new vars.
    attributes_2 = sources.attrs
    ## Set the img tag's src attr as a var.
    thumbImage = attributes_2['src']


    ## Split the thumbImage (the one with v2 in it) into a thumb URL str and larger image URL str.
    if "v2" in thumbImage:
        ## Split that var into a two-substring list using 'v2/' as a delimiter.
        largeImage = re.split(r'v2/', thumbImage)
        ## The str() casting function turns the spilt list back into a single str by the list index identified.
        largeImage = str(largeImage[1])
        #print("\n::thumbImage",thumbImage,"\n")
        #print("\n::largeImage",largeImage,"\n")
    else:
        ## If the attr values missing, then change the value to 'missing'.
        largeImage = m
        print("::largeImage is missing:",largeImage)
        pass


    ## The method .get_text() extracts ALL text within the tag, including the nested tags too.
    ## Grab the title text from the first search result a tag, remove the punctuation and remove the whitespace.
    linkLabel = foundTags_RT_results.get_text()
    linkLabel = (linkLabel.replace('&','and').replace('á','a').replace('Gonzalez','Gonzales').replace(':','').replace("'", "").strip())



    ## Grab only the first anchor tag link from the chosen movie html code.
    value = foundTags_RT_results.find('a')
    ## If it exists, aka if it "is True".
    if value:
        #print(":: yes it is true, and here it is...",value)
        ## Grab the href attr's value from that link tag.
        linkUrl = (value.get('href'))
        #print(":: linkUrl:",linkUrl)
    else:
        print(":: ERROR - RT is having trouble finding this!")

    ## Take the chosen URL and extract the more accurate title for further movTitle processing.
    movTitle = linkUrl.split('/m/')
    #print(":: movTitle:",movTitle)
    ## Choose the text after the /m/ divider.
    movTitle = str(movTitle[1])


    ## This is where we stop scraping the results and establish the RT mov page to start scraping from.
    ## Now scrape the chosen RT movie profile page to get more content. (using the linkURL instead of a new URL)
    response_2 = requests.get(linkUrl)
    soup_RottenTomMovPageHTML = BeautifulSoup(response_2.content, 'html.parser')

    ## Grab the first popcorn-meter tag, and scrape only the text.
    foundTags_RT_PopCornMeter = soup_RottenTomMovPageHTML.find('rt-text', slot='audienceScore')
    #print(f":: foundTags_RT_PopCornMeter: {foundTags_RT_PopCornMeter}")
    pcScore = foundTags_RT_PopCornMeter.get_text()
    ## Remove the percent sign.
    pcScore = pcScore.replace('%','')
    if not pcScore:
        pcScore = m
        print(":: no pcScore available on RT!")
    else:
        #pcScore = int(pcScore)
        #print(":: pcScore type:",type(pcScore))
        if int(pcScore) >= 80:
            pcScore = f"<span style=\"color:green\">{str(pcScore)+'%'}</span>"
        elif 40 <= int(pcScore) < 80:
            pcScore = f"<span style=\"color:yellow\">{str(pcScore)+'%'}</span>"
        elif int(pcScore) < 40:
            pcScore = f"<span style=\"color:red\">{str(pcScore)+'%'}</span>"
        else:
            pass

        #print(":: pcScore type:",type(pcScore))
        pcScore = str(pcScore)

    ## Make this score a complete html line.
    pcScore = f"<strong>{pcScore}</strong> - Popcorn Meter"



    ## Grab the similar movies tags from the RT movie page.
    foundTags_rtSimilarMovies = soup_RottenTomMovPageHTML.find_all('tile-poster-card', slot='tile')
    #print(foundTags_rtSimilarMovies)

    ## Set an empty list to append looped items from the find_all.
    RTsimilarMoviesList = []
    ## A for loop that narrows the find_all code blocks and converts them into full URLs and adds them into a list.
    for x in foundTags_rtSimilarMovies:
        ## Narrow the find_all to a find the individual item's code block.
        g = x.find('sr-text')
        t = str(g)
        t = t.replace('<sr-text>', '').replace('</sr-text>', '')
        ## There's something very redundant here but It fixed an intermittent issue of <sr-text> showing up in the text.
        g = str(g)
        g = g.replace('<sr-text>', '').replace('</sr-text>', '')
        #print("\n:: g----->:",g)
        #t = g.get_text()

        ## A search approach that converts the number input into written. This helps the original RT search approach - that may improve at some point.
        RTdirectorMoviesNoDigits = t.replace('0', 'zero').replace('1', 'one').replace('2', 'two').replace('3', 'three').replace('4', 'four').replace('5', 'five').replace('6', 'six').replace('7', 'seven').replace('8', 'eight').replace('9', 'nine')
        ## Dont select items that have "None" value.
        if g == None:
            print(":: g----(None)->:",g)

            pass
        else:
            #print("\n:: t----->:",t)
            ## Convert the title text into JVS links.
            x = f"<a style=\"{linkStyling}\" href=\"{absoluteLinkProcess}/jeverseeMovieDataGrabber.py?movTitleInput={RTdirectorMoviesNoDigits.replace(' ','+').replace('&','and')}\">{t}</a>"
            ## Add these selected items to the list.
            RTsimilarMoviesList.append(x)


    #print("\n:: RTsimilarMoviesList: (list)", RTsimilarMoviesList)

    ## If the var exists (is true), remove the last item in this list because it's always a None value.
    if RTsimilarMoviesList:
        del RTsimilarMoviesList[-1]
    else:
        pass
    ## Convert the list into a joined string using the join method. This removes the list brackets.
    RTsimilarMoviesList = (", ".join(RTsimilarMoviesList))

    #print("\n:: RTsimilarMoviesList: (str)", RTsimilarMoviesList)

    ## If the attr values are missing, then change the value to 'missing'.
    if RTsimilarMoviesList == "":
        RTsimilarMoviesList = m

    """
    ## Good example of narrowing down.
    foundTags_TMDB_searchResults = foundTags_TMDB_searchResults.find('a', attrs={'class':'result'})
    TMDBMovPageUrl = ("https://www.themoviedb.org"+foundTags_TMDB_searchResults.get('sr-text'))
    """




    ## Grab the first twitter image tag. This scrape provides a backup for a missing largeImage.
    foundTags_RT_largerImage = soup_RottenTomMovPageHTML.find('meta', attrs={'name':'twitter:image'})
    attributes_8 = foundTags_RT_largerImage.attrs
    #print(":: attributes_8:",attributes_8,"\n")
    foundTags_RT_largerImageNarrow = attributes_8['content']
    #print(f":: foundTags_RT_largerImage: {foundTags_RT_largerImage}\n")
    #print(":: foundTags_RT_largerImageNarrow:",foundTags_RT_largerImageNarrow,"\n")
    ## At this point the twitter image is not a backup, it just replaced the RT scrape.
    largeImage = foundTags_RT_largerImageNarrow
    #else:
        #pass



    ## Grab the director page from the RT movie page.
    foundTags_RTdirectorCode = soup_RottenTomMovPageHTML.find('rt-link', attrs={'data-qa':'item-value'})
    #print("\n:: foundTags_RTdirectorCode:", foundTags_RTdirectorCode)

    ## Grabbing the director code block attrs and turning specific values into new vars.
    attributes_7 = foundTags_RTdirectorCode.attrs
    #print(":: attributes_7:", attributes_7)
    ## Scrape the RT dir code block for the RT dir url.
    RTdirectorlink = attributes_7['href']
    RTdirectorlink = f"https://www.rottentomatoes.com{RTdirectorlink}"
    #print("\n:: RTdirectorlink:", RTdirectorlink,"\n")
    ## If the attr values missing, then change the value to 'missing'.
    if RTdirectorlink == "":
        RTdirectorlink = m


    ## RT Directors movies collection.
    ## The Requests module makes this unique var type: 'requests.models.Response'
    response_rtDir = requests.get(RTdirectorlink)
    ## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
    soup_rtDir_Page = BeautifulSoup(response_rtDir.content, 'html.parser')
    #print(":: soup_rtDir_Page:", soup_rtDir_Page.get_text())

    ## Scrape the RT dir page for all their directed films listed.
    foundTags_RTdirectorMovies = soup_rtDir_Page.find_all('filmography-card')

    ## Set an empty list to append looped items from the find_all.
    RTdirectorMoviesList = []
    ## A for loop to process all of the instances of the RT dir's directed films.
    for x in foundTags_RTdirectorMovies:
        ## Grab the text of one specific instance.
        t = x.get_text()
        string = t
        ## Scrape any 4 digit numbers from the dir movie list items and make them a separate var.
        foundYear = re.findall(r"\d{4}",string)
        #print(":: RT foundYear for dir collection movies:",foundYear)
        foundYear = str(foundYear)
        foundYear = foundYear.replace('[', '').replace(']', '').replace("'", "")
        ## This removes any films from the same year as the current movie.
        if foundYear != releaseYear:
            #print(":: foundYear == releaseYear:",t)
            q = t
        ## Some movie seemed to cause an issue so this is a temp fix. Was it Weapons?
        else:
            q = t
        #print("\n:: whole section of code:",t.strip())
        #print(":: RT foundYear for dir collection movies:",foundYear)
        ## If the word 'Director' is in the text of the current instance, select that code block.
        if "Director" in q:
            ## Find the narrowed code inside that code block and grab their title text.
            z = x.find('rt-text', slot='title')
            z = z.get_text()
            #print("\n:: director found!:",z)
            ## TEMP FIX FOR DIGITS IN RELATED MOVIES (solution code: "python replace digits with written numbers")
            #RTdirectorMoviesNoDigits = re.sub(r'\d+', '', z)



            ## A search approach that converts the number input into written. This helps the original RT search approach - that may improve at some point.
            RTdirectorMoviesNoDigits = z.replace('0', 'zero').replace('1', 'one').replace('2', 'two').replace('3', 'three').replace('4', 'four').replace('5', 'five').replace('6', 'six').replace('7', 'seven').replace('8', 'eight').replace('9', 'nine')

            ## Put that title text inside a JVS URL link and link label.
            x = f"<a style=\"{linkStyling}\" href=\"{absoluteLinkProcess}/jeverseeMovieDataGrabber.py?movTitleInput={RTdirectorMoviesNoDigits.replace(' ','+')+"+"+foundYear}\">{z}</a>"
            RTdirectorMoviesList.append(x)

        else:
            ## Do not append these instances into the list, because they are not selected.
            #print("\n:: they were not a director in this movie:")
            pass


    ## Reformat the list using the join method. This removes the list brackets.
    RTdirectorMoviesList = (", ".join(RTdirectorMoviesList))
    ## If the dir movie list var is None or empty, then change the value to 'missing'.
    if RTdirectorMoviesList == None or RTdirectorMoviesList == '':
        RTdirectorMoviesList = m
        print(":: RTdirectorMoviesList:", RTdirectorMoviesList)
    else:
        pass

    ## This find_all and for-loop/if-statement gets all of the streaming options shown on the chosen RT page.
    foundTags_RT_streamers = soup_RottenTomMovPageHTML.find_all('span', slot='license')
    #print(":: Streaming options:",foundTags_RT_streamers,"\n") ## Keep this print statement for new streamer checks.

    ## Set these streamer option var values to initial empty, for later html use or non-use.
    showTimes = fandango = disneyPlus = hulu = amcPlus = netflix = max = prime = paramountPlus = peacock = appleTv = starz = error56 = ""
    showTimesHtmlLink = fandangoHtmlLink = disneyPlusHtmlLink = huluHtmlLink = amcPlusHtmlLink = netflixHtmlLink = maxHtmlLink = primeHtmlLink = paramountPlusHtmlLink = peacockHtmlLink = appleTvHtmlLink = starzTvHtmlLink = ""


    ## Removing numbers from the mov titles to help the streamer results be more effective.
    ## THIS IS TEMP IF IM GOING TO REVAMP THE INTIAL RT SEARCH FOR BETTER YEAR ACCURACY.
    movTitleNoNumbers = re.sub(r'\d+', '', movTitle)


    #print(":: foundTags_RT_streamers:",foundTags_RT_streamers)

    ## Set streamer vars and add hrefs.
    for x in foundTags_RT_streamers:
        if x.get_text() == "In Theaters":
            showTimes = (f"Showtimes for {movTitle.replace("_", "+").capitalize()}: https://www.google.com/search?q=showtimes+{movTitle}+near+me\n")
            showTimesHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.google.com/search?q=showtimes+{movTitle.replace("_", "+")}+near+me\">Local Theater Showings?</a><br>"
        elif x.get_text() == "Fandango at Home":
            fandango = (f"Fandango: https://athome.fandango.com/content/browse/search?searchString={movTitle}\n")
            fandangoHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://athome.fandango.com/content/browse/search?searchString={movTitle}\">Fandango</a><br>"
        elif x.get_text() == "Disney+":
            disneyPlus = (f"Disney+: https://www.disneyplus.com/browse/search\n")
            disneyPlusHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.disneyplus.com/browse/search\">Disney+</a><br>"
        elif x.get_text() == "Hulu":
            hulu = (f"Hulu: https://www.hulu.com/content?tab=movies\n")
            huluHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.hulu.com/content?tab=movies\">Hulu</a><br>"
        elif x.get_text() == "AMC+":
            amcPlus = (f"AMC+: https://www.amcplus.com\n")
            amcPlusHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.amcplus.com\">AMC+</a><br>"
        elif x.get_text() == "Netflix":
            netflix = (f"Netflix: https://www.netflix.com/search?q={movTitleNoNumbers.replace("_", "+")}\n")
            netflixHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.netflix.com/search?q={movTitleNoNumbers.replace("_", "+")}\">Netflix</a><br>"
        elif x.get_text() == "HBO Max":
            max = (f"HBO Max: https://play.hbomax.com/search/result?q={movTitle}\n")
            maxHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://play.hbomax.com/search/result?q={movTitle.replace("_", " ")}\">HBO Max</a><br>"
        elif x.get_text() == "Prime Video":
            prime = (f"Prime Video: https://www.amazon.com/gp/aw/s/ref=nb_sb_noss_1?rh=i%3Ainstant-video&k={movTitle.replace("_", " ")}\n")
            primeHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.amazon.com/gp/aw/s/ref=nb_sb_noss_1?rh=i%3Ainstant-video&k={movTitle}\">Prime Video</a><br>"
        elif x.get_text() == "Paramount+":
            paramountPlus = (f"Paramount+: https://www.paramountplus.com/search/\n")
            paramountPlusHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.paramountplus.com/search/\">Paramount+</a><br>"
        elif x.get_text() == "Peacock":
            peacock = (f"Peacock: https://www.peacocktv.com/watch/search\n")
            peacockHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.peacocktv.com/watch/search\">Peacock</a><br>"
        elif x.get_text() == "Apple TV+" or x.get_text() == "Apple TV":
            appleTv = (f"Apple TV: https://tv.apple.com/us/search?term={movTitle}\n")
            appleTvHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://tv.apple.com/us/search?term={movTitle}\">Apple TV+</a><br>"
        elif x.get_text() == "Starz":
            starz = (f"Starz: https://www.starz.com/us/en/search?keyword={movTitle.replace("_","%20")}\n")
            starzTvHtmlLink = f"<a style=\"{linkStyling}\" href=\"https://www.starz.com/us/en/search?keyword={movTitle.replace("_","%20")}\">Starz</a><br>"
        else:
            error56 = (":: ERROR 56 - a new streamer must be added?\n")
        ## This diagnostic shows you the simple text of the streaming option like "Max" for example.
        #print(x.get_text())



    ## LTRBX STUFF STARTS HERE !!!!! MOST OF THIS CAN BE COMMENTED OUT, THEN TRASHED

    ## Sloppy way to maintain the verified RT and LTR movTitle vars so the scraped diagnostic lines remain accurate.
    movTitleRT = movTitle.replace("-", "_")
    movTitleLTR = movTitle.replace("_", "-")

    ## Request and soup-element the content of the LTRBX film url. This is the first guess URL.
    url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR}/")
    ## The Requests module makes this unique var type: 'requests.models.Response'
    response_1 = requests.get(url_LTRBX_movPageGuess)
    ## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
    soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')

    ## RT/LTRBX agreement logic starts here.
    #print("\n:: RT and LTRBX movie agreement DIAGNOSTICS")
    #print(f":: RT selection is: https://www.rottentomatoes.com/m/{movTitleRT}")
    #print(f":: LTRBXD selection is: https://letterboxd.com/film/{movTitleLTR}")

    ## This checkpoint makes sure that if Letterbox cant find the movie, that we remove the year (and any dashes?) and try again.
    foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
    #print(":: foundTags_LTRBX_pageTitle:\n",foundTags_LTRBX_pageTitle,"\n")

    ## Logic tries and overload vars. Probably can lose these.
    ltrboxLogicTries = f"1! {releaseYear}"
    requestsOverload = ""

    ## Use releaseYear to provide a prev and next year to catch inconsistencies between RT and LTRBX.
    releaseYear = int(releaseYear)
    prevYear = releaseYear-1
    nextYear = releaseYear+1
    releaseYear = str(releaseYear)
    prevYear = str(prevYear)
    nextYear = str(nextYear)


    ## Begin comparing RT release years (with mistake years added) to the guessed LTRBX url.
    if releaseYear not in foundTags_LTRBX_pageTitle:
        #print(":: releaseYear was not found!")

        if prevYear not in foundTags_LTRBX_pageTitle:
            #print(":: prevYear was not found either!")

            if nextYear not in foundTags_LTRBX_pageTitle:
                #print(":: nextYear was not found either!")

                ltrboxLogicTries = "2!"
                #print(":: Letterboxd DOES NOT agree, try a 2nd time! // .. add the RT release year")
                ## Replace any spaces with dashes.
                movTitleLTR = movTitleLTR.lstrip('-') + "-" + releaseYear
                url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR.replace("--", "-")}/")
                #time.sleep(delay2)
                response_1 = requests.get(url_LTRBX_movPageGuess)
                soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')
                foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
                #print(":: 2nd try - RT: "+movTitleRT)
                print(":: 2nd try - LTRBX: "+url_LTRBX_movPageGuess)
                #print(":: delay:",delay2)
                #print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle,"\n")

            else:
                #print(":: nextYear was found!")
                pass
        else:
            #print(":: prevYear was found!")
            pass
    else:
        #print(":: releaseYear was found!")
        pass





    ## This checkpoint makes sure that if Letterbox cant find the movie, that we try the user input with dashes, and try again.


    if releaseYear not in foundTags_LTRBX_pageTitle:
        #print(":: releaseYear was not found!")

        if prevYear not in foundTags_LTRBX_pageTitle:
            #print(":: prevYear was not found either!")

            if nextYear not in foundTags_LTRBX_pageTitle:
                #print(":: nextYear was not found either!")

                ltrboxLogicTries = "3!"
                #print(":: Letterboxd DOES NOT agree, try a 3rd time.// ..remove the year, all numbers really, and dashes.")
                ## Remove any digits from the movTitle var so that Letterbox can try again.
                movTitleLTR = re.sub(r'\d+', '', movTitleLTR) ## Always use r (raw) with regex so you dont have to escape anything.
                ## Remove any dashes, but put them back if needed so the next checkpoint might work.
                url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR.replace("-", "")}/")
                #time.sleep(delay)
                response_1 = requests.get(url_LTRBX_movPageGuess)
                soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')
                foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
                #print(":: 3rd try - RT: "+movTitleRT)
                print(":: 3rd try - LTRBX: "+url_LTRBX_movPageGuess)
                #print(":: delay:",delay)
                #print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle,"\n")

            else:
                #print(":: nextYear was found!")
                pass
        else:
            #print(":: prevYear was found!")
            pass
    else:
        #print(":: releaseYear was found!")
        pass


    ## This checkpoint makes sure that if Letterbox cant find the movie, that we add a "the-" and try again.


    if releaseYear not in foundTags_LTRBX_pageTitle:
        #print(":: releaseYear was not found!")

        if prevYear not in foundTags_LTRBX_pageTitle:
            #print(":: prevYear was not found either!")

            if nextYear not in foundTags_LTRBX_pageTitle:
                #print(":: nextYear was not found either!")

                ltrboxLogicTries = "4!"
                #print(":: Letterboxd DOES NOT agree, try a 4th time! // ..add a \"the-\".")
                ## Add the to the movTitle var so that Letterbox can try again.
                movTitleLTR = "the-" + movTitleRT.replace("_", "-")
                ## Replace any spaces with dashes.
                movTitleLTR = movTitleLTR.replace(" ", "-")
                url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR}/")
                #time.sleep(delay2)
                response_1 = requests.get(url_LTRBX_movPageGuess)
                soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')
                foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
                #print(":: 4th try - RT: "+movTitleRT)
                print(":: 4th try - LTRBX: "+url_LTRBX_movPageGuess)
                #print(":: delay:",delay2)
                #print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle,"\n")

            else:
                #print(":: nextYear was found!")
                pass
        else:
            #print(":: prevYear was found!")
            pass
    else:
        #print(":: releaseYear was found!")
        pass


    ## This checkpoint makes sure that if Letterbox cant find the movie, that we remove numbers but keep dashes and try again.


    if releaseYear not in foundTags_LTRBX_pageTitle:
        #print(":: releaseYear was not found!")

        if prevYear not in foundTags_LTRBX_pageTitle:
            #print(":: prevYear was not found either!")

            if nextYear not in foundTags_LTRBX_pageTitle:
                #print(":: nextYear was not found either!")

                ltrboxLogicTries = "5!"
                #print(":: Letterboxd DOES NOT agree, try a 5th time! // ..remove RT code numbers.")
                ## Add the to the movTitle var so that Letterbox can try again.
                movTitleLTR = re.sub(r'\d+', '', movTitleLTR) ## Always use r (raw) with regex so you dont have to escape anything.
                ## Replace any spaces with dashes.
                movTitleLTR = movTitleLTR.replace(" ", "-").replace("--", "-")
                ## Trim the first 4 characters (the-) from the title.
                movTitleLTR = movTitleLTR[4:]
                url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR}/")
                #time.sleep(delay)
                response_1 = requests.get(url_LTRBX_movPageGuess)
                soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')
                foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
                #print(":: 5th try - RT: "+movTitleRT)
                print(":: 5th try - LTRBX: "+url_LTRBX_movPageGuess)
                #print(":: delay:",delay)
                #print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle,"\n")

            else:
                #print(":: nextYear was found!")
                pass
        else:
            #print(":: prevYear was found!")
            pass
    else:
        #print(":: releaseYear was found!")
        pass





    ## This checkpoint makes sure that if Letterbox cant find the movie, that we add the release year to the url and try again.


    if releaseYear not in foundTags_LTRBX_pageTitle:
        #print(":: releaseYear was not found!")

        if prevYear not in foundTags_LTRBX_pageTitle:
            #print(":: prevYear was not found either!")

            if nextYear not in foundTags_LTRBX_pageTitle:
                #print(":: nextYear was not found either!")

                ltrboxLogicTries = "6!"
                #print(":: Letterboxd DOES NOT agree, try a 6th time. // ..try the user input with dashes added.")
                ## Replace any spaces with dashes.
                movTitleLTR = movTitleInput.replace(" ", "-").lower()
                url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR}/")
                #time.sleep(delay2)
                response_1 = requests.get(url_LTRBX_movPageGuess)
                soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')
                foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
                #print(":: 6th try - RT: "+movTitleRT)
                print(":: 6th try - LTRBX: "+url_LTRBX_movPageGuess)
                #print(":: delay:",delay2)
                #print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle,"\n")

            else:
                #print(":: nextYear was found!")
                pass
        else:
            #print(":: prevYear was found!")
            pass
    else:
        #print(":: releaseYear was found!")
        pass


    if releaseYear not in foundTags_LTRBX_pageTitle:
        #print(":: releaseYear was not found!")

        if prevYear not in foundTags_LTRBX_pageTitle:
            #print(":: prevYear was not found either!")

            if nextYear not in foundTags_LTRBX_pageTitle:
                #print(":: nextYear was not found either!")

                ltrboxLogicTries = "7!"
                #print(":: Letterboxd DOES NOT agree, try a 7th time. // ..try RT with '-and-' replace by a dash.")
                ## Replace any spaces with dashes.
                movTitleLTR = movTitleRT.replace("_", "-").replace("-and-", "-").lower()
                url_LTRBX_movPageGuess = (f"https://letterboxd.com/film/{movTitleLTR}/")
                #time.sleep(delay)
                response_1 = requests.get(url_LTRBX_movPageGuess)
                soup_LttrboxdMovPage = BeautifulSoup(response_1.content, 'html.parser')
                foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))
                #print(":: 7th try - RT: "+movTitleRT)
                print(":: 7th try - LTRBX: "+url_LTRBX_movPageGuess)
                #print(":: delay:",delay)
                #print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle,"\n")

            else:
                #print(":: nextYear was found!")
                pass
        else:
            #print(":: prevYear was found!")
            pass
    else:
        #print(":: releaseYear was found!")
        pass


    ## This FINAL checkpoint makes sure that if Letterbox cant find the movie, that we give up.
    foundTags_LTRBX_pageTitle = str(soup_LttrboxdMovPage.find('title'))

    ## Remove the title tags from either end of the string.
    foundTags_LTRBX_pageTitle = foundTags_LTRBX_pageTitle[7:]
    foundTags_LTRBX_pageTitle = foundTags_LTRBX_pageTitle[:-8]

    if "Access denied" in foundTags_LTRBX_pageTitle:
        print(":: Cloudflare says wait 60 seconds! \n")
        ltrboxLogicTries = "8! but cloudflare."
        requestsOverload = "CLOUDFLARE!"
        LTRguessSearchLink = f"https://letterboxd.com/search/{movTitleLTR}/"
        print(LTRguessSearchLink)

    elif releaseYear not in foundTags_LTRBX_pageTitle:

        if prevYear not in foundTags_LTRBX_pageTitle:

            if nextYear not in foundTags_LTRBX_pageTitle:

                ltrboxLogicTries = "FAILED after 8!"
                print(":: foundTags_LTRBX_pageTitle:",foundTags_LTRBX_pageTitle)
                print(":: Letterboxd DOES NOT agree. Letterboxd can't find this!! :(\n")
                LTRguessSearchLink = f"https://letterboxd.com/search/{movTitleLTR}/"
                print(LTRguessSearchLink)
                movTitleLTR = m

            else:
                print(":: Letterboxd and RT AGREE! (using the nextYear) \n")
                requestsOverload = ""
                #print(":: "+movTitle)
                #print(":: "+url_LTRBX_movPageGuess)
                LTRguessSearchLink = ""
                pass

        else:
            print(":: Letterboxd and RT AGREE! (using the prevYear)\n")
            requestsOverload = ""
            #print(":: "+movTitle)
            #print(":: "+url_LTRBX_movPageGuess)
            LTRguessSearchLink = ""
            pass

    else:
        print(":: Letterboxd and RT AGREE! (using the releaseYear)\n")
        requestsOverload = ""
        #print(":: "+movTitle)
        print(":: "+url_LTRBX_movPageGuess)
        LTRguessSearchLink = ""
        pass


    ## Compare RT year to LTR title tag result.
    print(":: Compare -> RT:",releaseYear,"..."+prevYear+","+nextYear, "LTRBX:"+foundTags_LTRBX_pageTitle+"\n\n")


    ## Divide the final choice from the search guess, so it can be the backup link if mov page not found.
    url_LTRBX_movPage = url_LTRBX_movPageGuess



    ## The TMDB logic starts here.
    ## Request and soup-element the TMDB search URL.
    url_TMDB = (f"https://www.themoviedb.org/search/movie?query={linkLabel.replace('_','-').replace(' ','-').replace('&','and')}&language=en-US")
    print(":: url_TMDB search:", url_TMDB)
    ## The Requests module makes this unique var type: 'requests.models.Response'
    response_TMDB = requests.get(url_TMDB)
    ## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
    soup_TMDBSearchPage = BeautifulSoup(response_TMDB.content, 'html.parser')
    ## Find all instances of the search result code blocks.
    foundTags_TMDB_searchResults = soup_TMDBSearchPage.find_all('div', attrs={'class':'search_results movie'})
    #print("\n:: foundTags_TMDB_searchResults...:", foundTags_TMDB_searchResults)


    ## A for-loop to process all of the instances of the found code blocks in the results page.
    for q in foundTags_TMDB_searchResults:
        ## The narrowing from a code section to the actual code blocks within that section. Good narrowing approach here.
        resultsTMDB = q.find_all('div', attrs={'class':'details'})
        for x in resultsTMDB:
            #print(":: resultsTMDB x:",x)
            t = x.get_text()
            #print(":: t from get text:",t)
            ## Scrape the mistake years for better result selection.
            prevYear = int(releaseYear) - 1
            nextYear = int(releaseYear) + 1
            #print(":: releaseYear,prevYear,nextYear:",releaseYear,prevYear,nextYear)

            ## If the RT release year is within the instance of the code block, then pull the h2 text from that block.
            if str(releaseYear) in t or str(nextYear) in t or str(prevYear) in t:

                foundTags_TMDB_searchResults = x
                foundTags_TMDB_searchResults = x.find('h2')
                h2Text = foundTags_TMDB_searchResults.get_text()
                ## Replace any garbage punctuation from the TMDB title so it can compare apples to apples with the RT title text.
                h2Text = h2Text.replace(':','').replace('Æ','Ae').replace('&','and').replace("'", "")
                print(":: DATE FOUND...(TMDB h2Text):",h2Text)
                ## If the TMDB title (assumed smaller) is within the (assumed longer) RT title, then select it.
                if h2Text.casefold() == linkLabel.replace('.','').casefold() or h2Text.casefold() in linkLabel.casefold() or linkLabel.casefold() in h2Text.casefold():
                    foundTags_TMDB_searchResults = x
                    print(":: DATE FOUND and title MATCH!:")
                    break
                else:
                    foundTags_TMDB_searchResults = m
                    print(":: DATE FOUND but no title match! (RT linkLabel):",linkLabel)

                #print("\n:: h2 text:",foundTags_TMDB_searchResults)
            elif foundTags_TMDB_searchResults:
                foundTags_TMDB_searchResults = x
                print(":: TMDB COULD NOT MATCH DATE SO IT JUST CHOSE THE FIRST RESULT.")
                #break
            else:
                print(":: NO MATCHING DATE FOUND (PROB ON THE ABOVE RESULT).")
                foundTags_TMDB_searchResults = m
                pass

        """         i = 0
        i = i + 1
        ## The iterator is 5 because the grabbed divs dont appear consistently with the reviews.
        if i > 5:
            break
        """

    #print("\n:: foundTags_TMDB_searchResults:", foundTags_TMDB_searchResults,"\n")
    print(":: RT found it, but can TMDB? url_RT_search:",url_RT_search,"\n")


    ## Good example of narrowing down.
    ## Make full URLs out of the searched results anchor tags and narrowed down hrefs.
    if foundTags_TMDB_searchResults == None:
        foundTags_TMDB_searchResults = m
        #print(":: TMDB is None.")
    if "There are no movies that matched your query." in str(foundTags_TMDB_searchResults):
        foundTags_TMDB_searchResults = m
        #print(":: TMDB found not one thing!")
    ## If TMDB didn't find the movie, then mark all TMDB vars as missing.
    if foundTags_TMDB_searchResults == m:
        TMDBMovPageUrl = m
        TMDB_ytCode = m
        foundTags_TMDB_DescText = m
        foundTags_TMDB_DirUrl = m
        foundTags_TMDB_DirText = m
        threeReviewsTMDB = ''
        TMDB_Money_Str = m
        print(":: TMDB failed.","\n")
    else:
        ## This is the intended code flow where the found tag results get their href links scraped.
        foundTags_TMDB_searchResults = foundTags_TMDB_searchResults.find('a', attrs={'class':'result'})
        #print("\n:: foundTags_TMDB_searchResults BEFORE HREF NARROWING:", foundTags_TMDB_searchResults)


        ## This becomes the final selected URL for the TMDB movie page.
        TMDBMovPageUrl = ("https://www.themoviedb.org"+foundTags_TMDB_searchResults.get('href'))
        #print("\n:: foundTags_TMDB_searchResults NARROWED TO HREF ONLY:", foundTags_TMDB_searchResults)
        ## The TMDB movie has been chosen.
        print(":: TMDBMovPageUrl:", TMDBMovPageUrl)

        TMDBtitle = TMDBMovPageUrl.replace('https://www.themoviedb.org/movie/','').replace('?language=en-US','')

        ## The Requests module makes this unique var type: 'requests.models.Response'
        response_TMDB_2 = requests.get(TMDBMovPageUrl)
        ## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
        soup_TMDB_MovPage = BeautifulSoup(response_TMDB_2.content, 'html.parser')



        ## Scrape the social media image from the TMDB mov page.
        foundTags_TMDB_ogImage = soup_TMDB_MovPage.find('meta', attrs={'property':'og:image'})
        #print(":: foundTags_TMDB_ogImage:",foundTags_TMDB_ogImage)
        if foundTags_TMDB_ogImage == None:
            foundTags_TMDB_ogImage = m
            TMDB_ogImage = m
        else:
            TMDB_ogImage = foundTags_TMDB_ogImage.get('content')
            #print(":: TMDB_ogImage:",TMDB_ogImage)


            #print(":: largeImage from TMDB:", largeImage)
            ## If RT only gave us a "missing image gif", then replace it with the TMDB graphic
            if "gif" in largeImage:
                largeImage = TMDB_ogImage
                print(":: TMDB has replaced the missing RT largeImage.")


        ## Find all instances of code blocks that contain director credited movies.
        #foundTags_TMDB_Dir = soup_TMDB_MovPage.find('ol', attrs={'class':'people no_image'})
        foundTags_TMDB_Dir = soup_TMDB_MovPage.find_all('li', attrs={'class':'profile'})
        print(":: foundTags_TMDB_Dir:",foundTags_TMDB_Dir)
        for x in foundTags_TMDB_Dir:
            #print("\n:: all li items:",x)
            if "Director" in x.get_text():
                foundTags_TMDB_Dir = x
                #print("\n:: foundTags_TMDB_Dir X:",x,"\n")
            else:
                #print("\n:: non-selected li items:",x)
                pass



        #print(":: foundTags_TMDB_Dir:",foundTags_TMDB_Dir)

        ## If TMDB dir was not found, then mark TMDB dir as missing.
        if foundTags_TMDB_Dir == None:
            foundTags_TMDB_Dir = m
            foundTags_TMDB_DirUrl = m
            foundTags_TMDB_DirText = m
        elif foundTags_TMDB_Dir == []:
            foundTags_TMDB_Dir = m
            foundTags_TMDB_DirUrl = m
            foundTags_TMDB_DirText = m
        else:
            ## Otherwise process the TMDB dir name and URL.
            foundTags_TMDB_DirUrl = foundTags_TMDB_Dir.find('a')
            foundTags_TMDB_DirText = foundTags_TMDB_DirUrl.get_text()
            #print("::: foundTags_TMDB_DirText:",foundTags_TMDB_DirText)

            foundTags_TMDB_DirUrl = str(foundTags_TMDB_DirUrl)
            #foundTags_TMDB_DirText = foundTags_TMDB_Dir.find('href')
            #foundTags_TMDB_DirText = foundTags_TMDB_DirText.get_text()

            ## Turn that TMDB relative link into an absolute link, then color it blue even if already visited.
            foundTags_TMDB_DirUrl = foundTags_TMDB_DirUrl.replace('/person','https://www.themoviedb.org/person')
            foundTags_TMDB_DirUrl = foundTags_TMDB_DirUrl.replace('<a ','<a style="color:#00b300;text-decoration:none;" ')

        ## Scrape the TMDB mov description text.
        foundTags_TMDB_Desc = soup_TMDB_MovPage.find('div', attrs={'class':'overview'})
        foundTags_TMDB_DescText = foundTags_TMDB_Desc.find('p')
        foundTags_TMDB_DescText = foundTags_TMDB_DescText.get_text()

        ## Scrape the trailer code block from TMDB.
        foundTags_TMDB_Trailer = soup_TMDB_MovPage.find('li', attrs={'class':'video none flex items-center ml-1'})
        if foundTags_TMDB_Trailer != None:
            foundTags_TMDB_TrailerUrl = foundTags_TMDB_Trailer.find('a')
            #foundTags_TMDB_DescText = foundTags_TMDB_DescText.get_text()

            ## Grabbing attrs and turning specific values into new vars.
            attributes_TrailerUrl = foundTags_TMDB_TrailerUrl.attrs

            ## Set the img tag's src attr as a var.
            TMDB_ytCode = attributes_TrailerUrl['data-id']
            TMDB_ytCode = TMDB_ytCode+"?"
            ## Prep the TMDB code piece to be an actual functioning YT link.
            TMDB_ytTrailer = "https://www.youtube.com/watch?v="+TMDB_ytCode+"?"
            print(":: foundTags_TMDB_Trailer does not equal None!",foundTags_TMDB_Trailer)
        else:
            TMDB_ytCode = m
            print(":: foundTags_TMDB_Trailer DOES equal None!",foundTags_TMDB_Trailer)
            pass




        ## Scrape the money numbers from TMDB.
        foundTags_TMDB_Money = soup_TMDB_MovPage.find_all('section', attrs={'class':'facts left_column'})
        ## Set an empty list to append looped items from the find_all.
        TMDB_Money_Str = []
        ## Process and format the money string.
        for x in foundTags_TMDB_Money:
            x = x.get_text().strip()
            x = x.replace('\n','<br>')
            x = x.replace('.00','')
            #x = x.replace("']","z")
            TMDB_Money_Str.append(x)
            #print("\n:: foundTags_TMDB_Money:",x)

        TMDB_Money_Str = str(TMDB_Money_Str)
        TMDB_Money_Str = TMDB_Money_Str.replace('Budget','Budget xxxxx')
        TMDB_Money_Str = re.split(r'Budget',TMDB_Money_Str)
        TMDB_Money_Str = TMDB_Money_Str[1]
        TMDB_Money_Str = TMDB_Money_Str.replace('xxxxx','Budget &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        #TMDB_Money_Str = TMDB_Money_Str.replace('xxxxx','<strong>Budget</strong>')
        TMDB_Money_Str = TMDB_Money_Str.replace('Revenue','Revenue &nbsp;&nbsp;&nbsp;')
        #TMDB_Money_Str = TMDB_Money_Str.replace('Revenue','<strong>Revenue</strong>')
        #TMDB_Money_Str = TMDB_Money_Str.replace('.00','.00 zzzzz')
        TMDB_Money_Str = re.split(r"']",TMDB_Money_Str)
        TMDB_Money_Str = TMDB_Money_Str[0]
        #TMDB_Money_Str = TMDB_Money_Str.replace('zzzzz','.00')
        TMDB_Money_Str = str(TMDB_Money_Str)
        #TMDB_Money_Str = TMDB_Money_Str.replace('\nRevenue','<br>Revenue')

        ## If statements to display consistent "- unavailable" values when either of the 2 numbers are missing.
        if "Budget &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -" in TMDB_Money_Str:
            TMDB_Money_Str = TMDB_Money_Str.replace('Budget &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -',f'Budget &nbsp;&nbsp; - &nbsp; {m}')
            #TMDB_Money_Str = TMDB_Money_Str.replace('-','q',1)
            #print("\n:: TMDB_Money_Str 1:",TMDB_Money_Str)

        if "<br>Revenue &nbsp;&nbsp;&nbsp; -" in TMDB_Money_Str:
            #TMDB_Money_Str = TMDB_Money_Str.replace('-','')
            TMDB_Money_Str = TMDB_Money_Str.replace('<br>Revenue &nbsp;&nbsp;&nbsp; -',f'<br>Revenue &nbsp; - &nbsp;&nbsp; {m}')
            #print("\n:: TMDB_Money_Str 2:",TMDB_Money_Str)

        else:
            pass
        #print("\n:: TMDB_Money_Str:",TMDB_Money_Str)


        ## General diagnostics for the previous few sections.
        #print(":: url_Test:",url_Test)
        #print(":: foundTags_TMDB_searchResults:",foundTags_TMDB_searchResults)
        #print("\n:: TMDBMovPageUrl:\n",TMDBMovPageUrl)
        #print(":: foundTags_TMDB_Dir:",foundTags_TMDB_Dir)
        #print(":: foundTags_TMDB_DirUrl:\n",foundTags_TMDB_DirUrl)
        #print(":: foundTags_TMDB_DirText:",foundTags_TMDB_DirText)
        #print(":: foundTags_TMDB_DescText:\n",foundTags_TMDB_DescText)
        #print(":: foundTags_TMDB_TrailerUrl:",foundTags_TMDB_TrailerUrl)
        #print(":: TMDB_ytCode:\n", TMDB_ytCode,"\n")



    ## Scrape the tagline code from the LTRBX mov page.
    foundTags_LTRBX_tagline = soup_LttrboxdMovPage.find('h4', attrs={'class':'tagline'})
    #print("::: foundTags_LTRBX_tagline:", foundTags_LTRBX_tagline)
    ## Get text from that tag, and remove the extra whitespace.
    if foundTags_LTRBX_tagline != None:
        tagLine = foundTags_LTRBX_tagline.get_text()
        tagLine = tagLine.strip()
        tagLine = tagLine+" --- "
    else:
        tagLine = ""
        pass



    ## Scrape the desc text from the LTRBX mov page.
    foundTags_LTRBX_descText = soup_LttrboxdMovPage.find('div', attrs={'class':'truncate'})
    ## Get text from that tag.
    if foundTags_LTRBX_descText == None:
        descText = m
    else:
        descText = foundTags_LTRBX_descText.get_text()

    ## Scrape the dir code from the LTRBX mov page.
    foundTags_LTRBX_director  = soup_LttrboxdMovPage.find('a', attrs={'class':'contributor'})

    if foundTags_LTRBX_director  == None:
        dirLink = m
        dirText = m
    else:
        ## Grabbing attrs and turning specific values into new vars.
        attributes_3 = foundTags_LTRBX_director.attrs
        dirLink = attributes_3['href']
        #print(":: dirLink:",dirLink)

        for x in foundTags_LTRBX_director :
            #.get_text() extracts all text within the tag, including nested tags
            dirText = x.get_text()
            #dirText = "<a href=\"https://letterboxd.com\">"+dirText+"</a>"
            #print(a.get('href'))

    ## Insert the LTRBX dir name text into the LTRBX dir collection page url in chrono order.
    dirLink = f"<a style=\"{linkStyling}\" href=\"https://letterboxd.com{dirLink}by/release/\">"+dirText+"</a>"


    """
    ## Scraps from the TMDB dir process.
    foundTags_TMDB_DirUrl = foundTags_TMDB_Dir.find('a')
    foundTags_TMDB_DirUrl = str(foundTags_TMDB_DirUrl)
    foundTags_TMDB_DirUrl = foundTags_TMDB_DirUrl.replace('/person','https://www.themoviedb.org/person')
    """

    ## Scraping the age rating from the RT mov page.
    foundTags_RT_ageRating = soup_RottenTomMovPageHTML.get_text()
    #print(":: foundTags_RT_ageRating:",foundTags_RT_ageRating)

    ## The method split() cuts the str into a list of substring parts using the 'arg text delimiter' identified.
    ageRating = re.split(r'Movie Info',foundTags_RT_ageRating)
    ## The str() function turns the spilt list back into a single str by the list index place identified.
    #print(":: ageRating:",ageRating)
    ageRating = str(ageRating[1])

    ## Make sure the age rating is even available in the Move Info section, before I go cutting the page text up looking for it.
    if "Rating" in ageRating:

        ## Silly duct tape fix for an inconvenient production company name.
        foundTags_RT_ageRating = foundTags_RT_ageRating.replace("Kinberg Genre", "")
        ## The method split() cuts the str into a list of substring parts using the 'arg text delimiter' identified.
        ageRating = re.split(r'Genre',foundTags_RT_ageRating)
        ## The str() function turns the spilt list back into a single str by the list count identified.
        ageRating = str(ageRating[0])
        #print(":: ageRating 715",(ageRating))


        if "Production Co" in ageRating:
            ## The method split() cuts the str into a list of substring parts using the 'arg text delimiter' identified.
            ageRating = re.split(r'Production Co',ageRating)
            ## Convert part of that list into a new str.
            ageRating = str(ageRating[1])
            #print(":: ageRating 3",(ageRating))
            #print(":: ageRating 724:",ageRating[1])

        elif "Director" in ageRating:
            ## The method split() cuts the str into a list of substring parts using the 'arg text delimiter' identified.
            ageRating = re.split(r'Director',ageRating)
            ## Convert part of that list into a new str.
            #print(":: ageRating 731:",ageRating[2])
            ## For some reason RT has the Director text shown twice, so we choose the 3 list item.
            ageRating = str(ageRating[2])

        else:
            pass


        ## The method split() cuts the str into a list of substring parts using the 'arg text delimiter' identified.
        ageRating = re.split(r'Rating',ageRating)
        ## Convert part of that list into a new str.
        #print(":: ageRating 1343:",ageRating)
        ageRating = str(ageRating[1])
        #print(":: ageRating 744:",ageRating[1])

        ## Formatting work on age rating.
        ageRating = ageRating.strip()
        ageRating = ageRating.replace("|", ", ")
        #print(":: ageRating 750:",ageRating[1])

    else:
        #print(":: \nageRating",(ageRating))
        ageRating = m


    #print(":: TMDB_ytCode: (1371)",TMDB_ytCode)

    ## Scrape the YT trailer link from the LTRBX mov page and prep the html embed version of the yt video code.
    foundTags_LTRBX_ytTrailer = soup_LttrboxdMovPage.find('a', attrs={'data-track-category':'Trailer'})
    #print("::: foundTags_LTRBX_ytTrailer:", foundTags_LTRBX_ytTrailer)
    ## Grabbing attrs and turning specific values into new vars.
    print(":: ltrboxLogicTries:",ltrboxLogicTries)

    if foundTags_LTRBX_ytTrailer != None:
        attributes_4 = foundTags_LTRBX_ytTrailer.attrs
        ytTrailerLink = attributes_4['href']
        ytTrailerLink = re.split(r'embed',ytTrailerLink)
        #print(":: ytTrailerLink:",ytTrailerLink)
        ytTrailerLink = str(ytTrailerLink[1])
        ytTrailerLink = re.split(r'rel',ytTrailerLink)
        ytTrailerLink = str(ytTrailerLink[0])
        #ytTrailerLink = "https://www.youtube-nocookie.com/embed"+ytTrailerLink+"autoplay=1&mute=1"
        ytTrailerLink = f"<iframe src=\"https://www.youtube.com/embed/{ytTrailerLink}&autoplay=1\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>"
        #print(":: ytTrailerLink found normally:",ytTrailerLink)

    ## If LTRBX does not provide a YT trailer, try to use the TMDB yt code, or just use the search link.
    elif "8!" in ltrboxLogicTries:

        if TMDB_ytCode != m:
            print(":: yt link replaced with TMDB video!")
            ytTrailerLink = f"<iframe src=\"https://www.youtube.com/embed/{TMDB_ytCode}&autoplay=1\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share\" referrerpolicy=\"strict-origin-when-cross-origin\" allowfullscreen></iframe>"
            #width="560" height="315"
        else:
            ## YT search link prep.
            ytTrailerLink = f"<a style=\"{linkStyling}\" href=\"https://www.youtube.com/results?search_query={linkLabel.replace(' ','+')}+movie+trailer\">{linkLabel} Movie Trailer</a>"
            print(":: yt link embed replaced with search results!")
            #print(":: even TMDB didnt have the movie so they can't provide a video here.")


    else:
        ## YT search link prep.
        ytTrailerLink = f"<a style=\"{linkStyling}\" href=\"https://www.youtube.com/results?search_query={linkLabel.replace(' ','+')}+movie+trailer\">{linkLabel} Movie Trailer</a>"
        print(":: yt link embed replaced with search results!")


        ## If nothing works, then just give up and mark it unavailable.
        #ytTrailerLink = "trailer unavailable"


    ## Scrape the LTRBX reviews from their mov page.
    foundTags_LTRBX_reviews = soup_LttrboxdMovPage.find('div', attrs={'class':'viewing-list'})
    ## Iterator for the for loop range of getting only the first 3 reviews.
    i = 0
    y = 0
    #print(":: foundTags_LTRBX_reviews:",foundTags_LTRBX_reviews)



    ## TEMP FIX HERE!
    allReviewsPageLTRBX = ""



    ## The for-loop for this section in with the printing statements.
    if foundTags_LTRBX_reviews == None:
        print(":: foundTags_LTRBX_reviews are None.")
        threeReviewsLTR = ''
    else:

        ## HTML link: (Reviews from Letterboxd).
        allReviewsPageLTRBX = f"<a style=\"{linkStyling}\" href=\"https://letterboxd.com/film/{movTitleLTR}/reviews/by/activity/\">...more reviews from Letterboxd</a><br><br><br>"
        ## Read-the-rest (LTRBX)
        allReviewsPage_LTRreadRest = f"<a style=\"{linkStyling}\" href=\"https://letterboxd.com/film/{movTitleLTR}/reviews/by/activity/\">... read the rest.</a>"

        threeReviewsLTR = []
        #threeReviewLinksList = []
        for x in foundTags_LTRBX_reviews:
            review = (x.get_text().strip())
            review = re.split(r'Translate',review)
            review = str(review[0])
            ## Add line breaks to make the reviews more readable. But this might be reversed by line 506?
            review = review.replace('       ','\n').replace('     ','\n')
            review = review.replace('\n','<br>')
            review = review.replace('Liked<br>','<br>')
            review = review.replace('Review by ','')
            #review = review.replace('... ',f'{allReviewsPage_LTRreadRest}')
            review = review.replace('I can handle the truth.','.... <br><br>')
            review = re.sub(r'Liked (\d+)<br>', '<br>', review)
            review = re.sub(r'    (\d+)<br>', '<br>', review)
            review = re.sub(r' (\d+)<br>', '<br>', review)

            #print(review)
            #review = re.split(r'?????',review)

            ## This iterator and if statement support the for loop to stop the loop after 3 reviews get processed.
            i = i + 1
            ## This puts the 3 strs into an easy-to-move-and-print list.
            threeReviewsLTR.append(review)
            ## The iterator is 5 because the grabbed divs dont appear consistently with the reviews.
            if i > 5:
                break


    #print("\n:: LTRBX threeReviewsLTR as a list:",threeReviewsLTR)



    ## TEMP FIX!
    allReviewsPageTMDB = ""



    ## If the TMDB movie was found, grab the reviews.
    if TMDBMovPageUrl != m:
        ## If LTR reviews missing, then scrape some TMDB reviews.
        if threeReviewsLTR == '':

            ## Convert the TMDB mov page into its corresponding reviews page.
            TMDB_reviewsPageUrl = TMDBMovPageUrl.replace('?language','/reviews?language')

            ## HTML link: (Reviews from TMDB)
            allReviewsPageTMDB = f"<a style=\"{linkStyling}\" href=\"{TMDB_reviewsPageUrl}\">...more reviews from TMDB</a>"
            ## Read-the-rest (TMDB)
            allReviewsPage_readtheRest = f"<a style=\"{linkStyling}\" href=\"{TMDB_reviewsPageUrl}\">read the rest.</a>"

            ## The Requests module makes this unique var type: 'requests.models.Response'
            response_TMDB_3 = requests.get(TMDB_reviewsPageUrl)
            ## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
            soup_TMDB_reviewsMovPage = BeautifulSoup(response_TMDB_3.content, 'html.parser')
            foundTags_TMDB_reviews = soup_TMDB_reviewsMovPage.find_all('div', attrs={'class':'card'})
            #foundTags_TMDB_reviews = foundTags_TMDB_reviews.get_text()
            #print(":: foundTags_TMDB_reviews:",foundTags_TMDB_reviews)

            ## If TMDB has no reviews, then mark the var 'unavailable'.
            if foundTags_TMDB_reviews == []:
                foundTags_TMDB_reviews = m
                print(":: foundTags_TMDB_reviews is empty:",foundTags_TMDB_reviews)
                pass
            else:
                pass

            ## Create a list for the TMDB reviews.
            ## Define an empty list to append the unselected html tag block results to.
            threeReviewsTMDB = []
            ## If there are no TMDB reviews, then convert that empty list into an empty str.
            if foundTags_TMDB_reviews == m:
                threeReviewsTMDB = ''
                pass
            else:

                ## Format the TMDB individual reviews.
                for x in foundTags_TMDB_reviews:
                    x = x.get_text().strip()
                    #print(":: TMDB reviews before formatting:",x)
                    x = x.replace('\n\n\n\n\n','zzz')
                    x = str(x)
                    x = re.split(r'\n\n',x)
                    ## The str() function turns the spilt list back into a single str by the list count identified.
                    #print(":: TMDB reviews at 1239:\n",x)
                    x = str(x)
                    #print(":: TMDB reviews at 1241:",x)
                    x = re.split(r'zzz',x)
                    #print(":: TMDB reviews at 1243:",x)
                    x = str(x[1])
                    x = x.replace('\n','<br><br>')
                    x = x.replace('\\n',' ')
                    #x = x.replace('<br>Written by ','<br>')
                    x = x.replace('... read the rest.',f'... {allReviewsPage_readtheRest}')
                    #x = x[1:]
                    #x = re.split(r'<br>',x)
                    #secondLine = str(x[1])
                    #print("\n:: TMDB Review:\n",x)
                    ## This iterator and if statement support the for loop to stop the loop after 3 reviews get processed.
                    i = i + 1
                    ## This puts the 3 strs into an easy-to-move-and-print list.
                    threeReviewsTMDB.append(x+"<br><br>")
                    ## The iterator is 1 because the grabbed divs dont appear consistently with the reviews. Also TMDB reviews are super long.
                    if i > 1:
                        break

                #print("\n:: threeReviewsTMDB:",threeReviewsTMDB)
                #print(":: foundTags_TMDB_reviews:",foundTags_TMDB_reviews)

        else:
            ## If TMDB reviews are not needed, then mark the review text as an empty string. Basically erase them.
            threeReviewsTMDB = ''
            pass

    else:
        ## If TMDB reviews are not needed, then mark the "Reviews from" HTML link as an empty string.
        allReviewsPageTMDB = ''
        pass


    ## Scraping RT reviews in case both LTR and TMDB fail to provide them.
    foundTags_RT_reviews = soup_RottenTomMovPageHTML.find_all('span', slot='content')
    i = 0
    threeReviewsRT = []
    ## If the RT reviews exist, process them.
    if foundTags_RT_reviews:
        for x in foundTags_RT_reviews:
            x = x.get_text()
            #print("\n:: RT review:",x)
            threeReviewsRT.append(x+"<br>")
            i = i + 1
            if i == 5:
                break

        ## HTML link: (Reviews from RT)
        allReviewsPageRT = f"<a style=\"{linkStyling}\" href=\"https://www.rottentomatoes.com/m/{movTitleRT}/reviews\">...more reviews from Rotten Tomatoes</a>"

    else:
        foundTags_RT_reviews = m
        threeReviewsRT = m
        pass
    #print("\n:: foundTags_RT_reviews:",foundTags_RT_reviews)
    #print("\n:: threeReviewsRT:",threeReviewsRT)
    #print(":: threeReviews:",threeReviews)


    ## Links to movie profile page on other sites grabbing ++++++++++++++++++++++++++++++++++++++++++++

    ## Scrape the IMDB link from the RT mov page.
    foundTags_LTRBX_imdb = soup_LttrboxdMovPage.find('a', attrs={'data-track-action':'IMDb'})
    ## If the value is missing, then change the value to 'missing'.
    if foundTags_LTRBX_imdb == None:
        imdbLink = m
    else:
        ## Grabbing attrs and turning specific values into new vars.
        attributes_5 = foundTags_LTRBX_imdb.attrs
        imdbLink = attributes_5['href']


    ## Scrape the TMDB link from the RT mov page.
    foundTags_LTRBX_tmdb = soup_LttrboxdMovPage.find('a', attrs={'data-track-action':'TMDB'})
    ## If the attr values missing, then change the value to 'missing'.
    if foundTags_LTRBX_tmdb == None:
        tmdbLink = m
    else:
        ## Grabbing attrs and turning specific values into new vars.
        attributes_6 = foundTags_LTRBX_tmdb.attrs
        tmdbLink = attributes_6['href']


    ## Change the mov title back to the RT chosen value just so the guesses have a chance at working.
    if movTitleRT == m:
        ## This is using the input, but probably should be using the RT chosen title. I just cant find that rn.
        movTitleRT = movTitleInput
    else:
        pass


    ## A few guess links ++++++++++++++++++++++++++++++++++++++++++++

    ## JustWatch does not allow scraping, so only search guessing
    jwSearchResults = f"https://www.justwatch.com/us/search?q={linkLabel}"

    ## These websites don't love spaces so we added %20s. Seems to be working well.
    movTitleRT = movTitleRT.replace(" ", "%20")

    ## Wikipedia link guess.
    #wikiGuessUrl = f"https://en.wikipedia.org/wiki/{movTitle.title()}_({movYear}film)"
    wikiGuessUrl = f"https://en.wikipedia.org/w/index.php?fulltext=1&search={linkLabel+"%20film"}&title=Special%3ASearch&ns0=1"
    #wikiGuessUrl = wikiGuessUrl.replace(" ", "_")
    ## If the attr values missing, then change the value to 'missing'.
    if wikiGuessUrl == "":
        wikiGuessUrl = m

    ## Metacritic does not allow scraping, so only page link guessing
    metaCriticPage = f"https://www.metacritic.com/search/{linkLabel}/"
    ## If the attr values missing, then change the value to 'missing'.
    if metaCriticPage == "":
        metaCriticPage = m

    ## YouTube Music Movie Soundtrack link guess.
    ytMusicSTGuessUrl = f"https://music.youtube.com/search?q={linkLabel}+{releaseYear}+soundtrack"
    ## If the attr values missing, then change the value to 'missing'.
    if ytMusicSTGuessUrl == "":
        ytMusicSTGuessUrl = m

    ## RT photos link guess.
    rtPhotosGuessUrl = f"https://www.rottentomatoes.com/m/{movTitleRT}/pictures"
    ## If the attr values missing, then change the value to 'missing'.
    if rtPhotosGuessUrl == "":
        rtPhotosGuessUrl = m



    ## Change RT title back to missing since we're done with the guessing?
    """
    I think this is not needed since i y-forked movTitle into RT or LTR
    """
    if movTitleRT == movTitleInput:
        movTitle = m
    else:
        pass



    '''
    ## Soundtrack.net was resolving at film-music.com and that's causing security connection issues on some machines and browsers.
    ## A week later and they sold to a new site called https://www.soundtrakd.com/. I can recode this later if I want.

    ## Request and soup-element the content of a specific URL
    url_sndTrakNet = (f"https://www.soundtrack.net/search/index.php?q={movTitle.replace("-", " ")}")
    ## The Requests module makes this unique var type: 'requests.models.Response'
    response_2 = requests.get(url_sndTrakNet)
    ## The bs4 module makes this unique var type: 'bs4.BeautifulSoup'
    soup_SndTrckNetSearch = BeautifulSoup(response_2.content, 'html.parser') ## Pulls raw response HTML as bytes more accurate than text.

    ## Grab the first of a specific tag. (divs with the flex-1 class)
    foundTags_sndTrkNet_result = soup_SndTrckNetSearch.find('div', attrs={'class':'flex-1'})

    print(url_sndTrakNet,"\n",foundTags_sndTrkNet_result)
    ## Grab the first link from the found tags to "narrow down the grabbing".    @ @ @  NARROWING WORKS  @ @ @
    if foundTags_sndTrkNet_result == None:
        pass
    else:
        resultLink = foundTags_sndTrkNet_result.find('a')
        stResult = resultLink['href']
        print(f"\nSoundtrack.net Movie page:\nhttps://www.soundtrack.net{stResult}")
        #print(f":: (pulled from the results on this search page: {url_sndTrakNet.replace(" ", "%20")})")

    '''


    ## Creating a URL for the JVS input page thumbnail image.
    thumbLinkUrl = (f"{absoluteLinkProcess}/jeverseeMovieDataGrabber.py?movTitleInput={linkLabel}%20{releaseYear}")
    ## Assembling the JVS link and the thumbnail image image into a full html line for the txt file storage.
    galleryImageTag = (f"<a href=\"{thumbLinkUrl}\"><img title=\"{linkLabel} {releaseYear}\" width=\"110\" src=\"{largeImage}\"></a>")



    #print(":: threeReviewsTMDB:",threeReviewsTMDB)

    ## If LTRBX search fails, then replace a lot of stuff with TMDB values.
    if "8!" in ltrboxLogicTries:
        filmsSimilar = f"https://www.rottentomatoes.com/m/{movTitleRT}#more-like-this"
        descText = foundTags_TMDB_DescText
        dirLink = foundTags_TMDB_DirUrl
        dirText = foundTags_TMDB_DirText
        tmdbLink = TMDBMovPageUrl
        imdbLink = f"https://www.imdb.com/find/?s=tt&q={linkLabel}"
        url_LTRBX_movPage = f"https://letterboxd.com/search/{linkLabel.replace(' ','+')}"
        #threeReviews = threeReviewsRT
        allReviewsPageLTRBX = ''
        #ytTrailerLink = TMDB_ytTrailer
        print(":: LTRBX cant find the movie, so LTRBX things have been replaced.")
    ## If TMDB never finds the movie, then remove the TMDB reviews HTML link and replace the TMDB link with the TMDB search link.
    if TMDBMovPageUrl == m:
        tmdbLink = url_TMDB
        allReviewsPageTMDB = ''
        TMDBtitle = '?'
        print(":: TMDB cant find the movie, so the TMDB search link has been replaced.")
    ## If RT never provides reviews, then remove the RT reviews HTML link and replace the three reviews var with the TMDB reviews.
    if threeReviewsRT == m:
        threeReviewsRT = ''
        allReviewsPageRT = ''
        print(":: RT gave no reviews, so we're using TMDB reviews.")
    if threeReviewsRT != m:
        threeReviewsTMDB = ''
        allReviewsPageTMDB = ''
        #print("\n:: RT reviews were available, so we're NOT using TMDB reviews.")
    if "CLOUDFLARE!" not in foundTags_LTRBX_pageTitle:
        #allReviewsPageRT = ''
        print(":: No cloudflare so the LTRBX stuff is being used.")

    else:
        ## This provides a simple a LTRBX similar URL as a backup to the similar movies collection.
        filmsSimilar = f"https://letterboxd.com/film/{movTitleLTR}/similar/"


    ## TEMP FIX!
    filmsSimilar = ''


    ## Early diagnostics.
    print(f":: DIAGNOSTICS")
    print(f":: Input movTitleGuess: {movTitleInput}")
    print(f":: Input movYear: {movYear}")
    print(f":: Scraped RT Search results URL:\n {url_RT_search}")
    print(f":: Chosen RT movTitle from URL: {movTitleRT.replace("-", "_")}")
    print(f":: Scraped RT movie page URL:  https://www.rottentomatoes.com/m/{movTitleRT}")
    print(f":: Scraped LTRBX URL... {url_LTRBX_movPage}")
    #print(f":: rtScore... {rtScore}")
    #print(f":: pcScore... {pcScore}")

    #print(f":: allReviewsPageLTRBX...\n {allReviewsPageLTRBX}")
    #print(f":: allReviewsPageRT...\n {allReviewsPageRT}")
    #print(f":: allReviewsPageTMDB...\n {allReviewsPageTMDB}")


    #from platform import python_version
    #print(python_version())  3.12.1 (Dec 17 2025)


    print("\n")



#region

    ###############################################################################################
    ###############################################################################################
    ###############################################################################################
    ###############################################################################################

    ## Terminal report was here. Terminal output (the print statements remain).

    ## paste code back here (currently located around line 2189)

    ###############################################################################################
    ###############################################################################################
    ###############################################################################################
    ###############################################################################################


#endregion


    ## COMMENT THIS OUT TO SEE MORE THAN AGREEMENT DIAGNOSTICS AND TERMINAL OUTPUT
    #exit()

#region

    ## TXT FILE REPORT EXPORT #####################################################################################


    ## A module to help you interact with your operating system.
    import os

    ## Check if the report file already exists, then remove it if so.
    file_path = (f"fileHandlingScrapFiles/jvs/jvs_{linkLabel.replace(" ", "-").replace(":", "")}_{releaseYear}.txt")



    # paste archived txt file code back here (currently located around line 2266)


    #####################################################################################



    ## THIS IS THE QUERY LOGGING SYSTEM
    from datetime import datetime
    from zoneinfo import ZoneInfo

    # Get current time in a specific timezone, e.g., 'America/New_York'
    current_datetime_ny = datetime.now(ZoneInfo('America/New_York'))
    current_datetime_ny = current_datetime_ny.strftime("%m-%d-%Y") #("%m-%d-%Y, %I:%M%p")

    ##
    baseURL = "/home/synclare/mysite/static/"
    ## Open a file in append mode with ('a').
    with open(f"{baseURL}jvs_query_log.txt", "a") as f:
        f.write(f"({movTitleInput.lower().replace("-", " ")}) ___ RT: {movTitleRT.lower().replace("-", " ").title()} ___LTR: {movTitleLTR} ___ TMDB: {TMDBtitle} ______ {current_datetime_ny} \n")



    ## Check on most recent gallery thumb. (other duplicates are fine i guess)
    with open(f"{baseURL}jvs_gallery_log.txt", "r") as f:
        recentLine = ""
        #logImagesGalleryReadOnly = []
        lines = f.readlines()  # Read all lines into a list
        for line in reversed(lines):
            recentLine = line
            #print(":: recentLine:", recentLine)
            break

    ## Open a file in append mode with ('w').
    with open(f"{baseURL}jvs_gallery_log.txt", "w") as f:
        #f.write(f"{requestsOverload} ___ {ltrboxLogicTries} ___ ({movTitleInput.lower().replace("-", " ")}) ___ {movTitleRT.replace("-", " ").title()} ___ {movTitleLTR} ___ {LTRguessSearchLink}  ___ {current_datetime_ny}\n")
        #print(":: current - galleryImageTag:",galleryImageTag,"\n")
        #print("\n:: lines:",lines)

        #lines = str(lines)
        for line in lines:
            #print(".. an existing line:", line)
            if galleryImageTag in str(line):
                #print(".. line that DOES match the current line:",line)
                pass
            else:
                f.write(line)
                #print(".. line that does NOT match the current line:",line)
                pass


    ## Open a file in append mode with ('a').
    with open(f"{baseURL}jvs_gallery_log.txt", "a") as f:
        #print(":: current - galleryImageTag:",galleryImageTag)
        f.write(f"{galleryImageTag} \n")




    ## Report current status.
    print(b)
    with open(f"{baseURL}jvs_query_log.txt", "r") as f:
        print(f"Here's what I read from the jvs_query_log.txt file that you just wrote to:")
        #print(f"Here's what I read from the jvs_query_log.txt file that you just wrote to:\n\n"+f.read())
        lines = f.readlines()  # Read all lines into a list
        for line in reversed(lines):  # Iterate through the list in reverse
            #print(line.strip()) ## There's too much terminal vertical space being used so im hiding this log readout.
            pass

    print("## There's too much terminal vertical space being used so im hiding this log readout.")
    print(b)

    ######################################################################################################

#endregion




#region

    ## Create an exported real HTML page version of the report.



    ## Define the HTML content as a multi-line string
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>{linkLabel} - JeverSee Movie Search Report</title>

<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="/static/styles.css">

</head>

<body>

<a style="{linkStyling}" href=\"{absoluteLinkInput}\">JeverSee Movie Search</a>  > {linkLabel} ({releaseYear})<br><br> {unselectedRTresultsList}<br><br>

<!-- table removed from here-->

<!--
<hr>
<hr>
-->

<div class="container">



        <div class="column1" id="item1">
        <!-- left column -->
            <h2>Reviews</h2>

            <p class="paragraph1">

            {"<br>".join(threeReviewsLTR)}<br>
            {allReviewsPageLTRBX}
            {"<br>".join(threeReviewsRT)}<br>
            {allReviewsPageRT}<br><br><br>
            {"<br>".join(threeReviewsTMDB)}
            {allReviewsPageTMDB}</p><br>

            <!--<br>
            {unselectedRTresultsList}<br><br>
            <a style="{linkStyling}" href="{url_RT_search}">(RT search)</a><br>-->

        </div>

        <div class="column2" id="item2" >
        <!-- middle column -->

            <a href="{linkUrl}"><img width="300" src="{largeImage}"></a><br><br>
            {ytTrailerLink}<br><br>

        </div>
        <div class="column3" id="item3">
        <!-- right column -->

            <h1>{linkLabel}</h1>

            <p class="paragraph2">
            <span style="font-size: 18px;">{releaseYear}</span><br>
            <i>{cast}</i><br>
            Directed by {dirLink}<br><br>
            {tagLine}{descText.strip()}<br><br>

            {rtScore}<br>
            {pcScore}<br>
            Rated <!--MPAA Rating:-->{ageRating}<br><br>
            {TMDB_Money_Str}</p>

            <hr>

            <br>
            <h4>{dirText} Films</h4>
            <p class="paragraph3">
            {RTdirectorMoviesList}<br><br>

            <h4>Similar Films</h4>
            {RTsimilarMoviesList}<br><br>

            <h4>Where to Watch</h4>
            {fandangoHtmlLink}{disneyPlusHtmlLink}{huluHtmlLink}{amcPlusHtmlLink}{netflixHtmlLink}{maxHtmlLink}{primeHtmlLink}{paramountPlusHtmlLink}{peacockHtmlLink}{appleTvHtmlLink}{starzTvHtmlLink}{showTimesHtmlLink}{error56}
            <a style="{linkStyling}" href="{jwSearchResults}">JustWatch streaming report</a><br><br>

            <h4>Learn More</h4>
            <a style="{linkStyling}" href="{linkUrl}">Rotten Tomatoes</a><br>
            <a style="{linkStyling}" href="{tmdbLink}">TMDB</a><br>
            <a style="{linkStyling}" href="{url_LTRBX_movPage}">Letterboxd</a><br>
            <a style="{linkStyling}" href="{imdbLink}">IMDB</a><br>

            <a style="{linkStyling}" href="{wikiGuessUrl}">Wikipedia</a><br>
            <a style="{linkStyling}" href="{metaCriticPage}">Metacritic</a><br>
            <a style="{linkStyling}" href="{ytMusicSTGuessUrl}">Soundtrack on YouTube Music</a><br>
            <a style="{linkStyling}" href="{rtPhotosGuessUrl}">Film Stills from Rotten Tomatoes</a><br>
            <!--<a style="{linkStyling}" href="{filmsSimilar}">Similar to {linkLabel}</a><br>-->
            <br>

            <hr>
            <!--Letterbox Matching Tries: {ltrboxLogicTries}
            <br>
            {requestsOverload}<br>
            {foundTags_LTRBX_pageTitle}<br>
            {tryAgain}<br>
            -->
            </p>


        </div>


</div>


</body>
</html>
'''

    print(b)
    print("HTML Output...\n (## Hidden for now)")
    #print(html_content)
    print(b)


    # Define the file path and name
    file_name = "/home/synclare/mysite/templates/templates_folder_jvs_report_testing.html"

    # Optional: Define a directory. Use os.path.join for cross-platform compatibility.
    # output_directory = "html_output"
    # file_path = os.path.join(output_directory, file_name)

    # Optional: Create the directory if it doesn't exist
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)




    # Open the file in write mode ('w')
    with open(file_name, 'w') as html_file:
        # Write the HTML content to the file
        html_file.write(html_content)



    '''
    ## HTML making starts here.
    ## Check if the html report file already exists, then remove it if so.
    file_path2 = (f"fileHandlingScrapFiles/jvs/html/jvs_{linkLabel.replace(" ", "-").replace(":", "")}_{releaseYear}.html")

    if os.path.exists(file_path2):
        os.remove(f"{file_path2}")
    else:
        pass

    ## Create a new file.
    f = open(f"{file_path2}", "x")


    # Open the file in write mode ('w')
    with open(file_path2, 'w') as f:
        # Write the HTML content to the file
        f.write(html_content)




    print(b)
    print(f"File: '{file_name}' created for '{linkLabel}'.")
    print(f"File: '{file_path2}' created for '{linkLabel}'.")
    print(b)
    '''

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    #print(":: the processing script ran (around line 2050)")

    #print(":: the processing script ran (around line 2052)")

    print(":: Finished :)")

    ## Restart.
    #inputMovTitleAndYear()



    ## Send me an email when folks use this? (never worked)





## Begin. **********   **********   **********   **********   **********



#print(":: the Begin inputMovTitleAndYear FUNC ran!")


#region



# i removed the flask stuff from here

## Imports
from flask import Flask, request, render_template, url_for

# Create an instance of the Flask class
app = Flask(__name__)

## Define a route for the home page ("/")
@app.route('/jeverseeMovieDataGrabber.py')


## Define the function.
def render_html():



    #display_form()
    global movTitleInput,text

    ## This checks to see if the URl has an input value.
    if 'movTitleInput' not in request.args:

        print(".")
        print(" ")
        print(".")
        print(":: flask did NOT find movTitleInput in the URL.\n")
        print("---------------------------------------------------")
    #if request.method == 'GET':

        title = "Jeversee Movie Search"
        baseURL = "/home/synclare/mysite/static/"
        with open(f"{baseURL}jvs_query_log.txt", "r") as f:
            #print(f"Log file so far:<br><br>")
            logFile = []
            lines = f.readlines()  # Read all lines into a list
            for line in reversed(lines):  # Iterate through the list in reverse
                line = line.replace("\n", "<br>")
                line = str(line)
                logFile.append(line)

            #logFile = str(logFile)
            logFile = (" ".join(logFile))

            """
            lines = f.readlines()  # Read all lines into a list
            for line in reversed(lines):  # Iterate through the list in reverse
                print(line.strip())
            """

            with open(f"{baseURL}jvs_gallery_log.txt", "r") as f:
                #print(f"Log image gallery file so far:<br><br>")
                i = 0
                logImagesGallery = []
                lines = f.readlines()  # Read all lines into a list
                for line in reversed(lines):  # Iterate through the list in reverse
                    line = line.replace("\n", " ")
                    line = str(line)
                    logImagesGallery.append(line)
                    i = i + 1
                    if i == 56:
                        break


                #logFile = str(logFile)
                logImagesGallery = (" ".join(logImagesGallery))


                # <p>{logImagesGallery}</p>

                text = (f"""

            <!DOCTYPE html>
            <html>
            <head>
                <title>{title}</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="color:#D3D3D3;font-family: Arial, Helvetica, sans-serif;font-size: 13px;" bgcolor="black">
                <form action = "{absoluteLinkProcess}/jeverseeMovieDataGrabber.py" method = "get">
                    <h1 style="color:#00b300;text-align:center;font-size:44px;">JeverSee this movie?</h1>

                    <p style="text-align:center;"><input style="height: 38px;font-size: 18px;" type = "text" name = "movTitleInput" size="20" />
                    <input style="height:45px;font-size:28px;padding-bottom:4px;background-color:#00b300;color:white;border:none;" type = "submit" value = "&rarr;" />

                    </p>
                    <br>
                    <p>{logImagesGallery}</p><br><br>


                    <!--
                    <p>{logFile}</p>

                    -->
                </form>
            </body>
            </html>

                """)
                return text

    else:

        #print(":: request.args:",request.args)

        ## Accessing data from a GET form submission
        movTitleInput = request.args.get('movTitleInput')
        print(" ")
        print(" ")
        print(" ")
        print(":: flask found movTitleInput in the URL!\n")
        inputMovTitleAndYear()
        return(html_content)
        #return render_template('templates_folder_jvs_report_testing.html')



""" ## Define a route for the home page ("/")
@app1.route('/jeverseeMovieDataGrabber.py')

## Define the function.
def render_html():
    return render_template('templates_folder_jvs_report_testing.html') """



""" ## Define a route for the home page ("/")
@app1.route('/jeverseeMovieDataGrabber.py', methods=['GET', 'POST'])

## Define the function.
def submit_form():
    global movTitleInput
    if request.method == 'GET':
        ## Accessing data from a GET form submission
        movTitleInput = request.args.get('movTitleInput')
        if movTitleInput =="tron":
            return("you searched for tron!"+"<br><a href=\"{absoluteLinkInput}/jvs_input_form.html\">GO BACK</a>")

        else:
            return("You did not search for tron :(")  """

    #else:
        #return("broken!")


## UNCOMMENT THIS FUNC TO DO TERMINAL WORK
#inputMovTitleAndYear()

## COMMENT THIS AREA OUT TO DO TERMINAL WORK

"""
"""

# Run the Flask application
#if __name__ == '__main__':






#endregion




#region

## This region is for previewing a virtual HTML file report.

"""
## Set this var to empty before the input assigns the real value.
html_content = ""

## Flask connection for direct HTML output.


# In your main application file (e.g., app.py)
from flask import Flask


# Create an instance of the Flask class
app2 = Flask(__name__)

# Define a route for the home page ("/")
@app2.route("/jvs_report_testing.html")

def flaskHtml():
    #return "<p>Hello, World!<br>Michael Synclare</p>"
    #title = "Dynamic Title!"

    #testHtml = ("<p> testerino! </p>")
    return html_content
    #return


inputMovTitleAndYear()
print(":: the flask input FUNC ran!")
#flaskHtml()

# Run the Flask application
if __name__ == "__main__":
    app2.run(debug=True) # debug=True enables debug mode for development

    print(":: The Flask code ran!")
else:
    print(":: The Flask code did not ran??")
"""
#endregion



## Right now we are never getting to this point!!!
#inputMovTitleAndYear()
#print(":: the Begin input FUNC ran!")



#print(b)
print("\n\n\n")



'''
SCRAPS

#substring = s[start : end : step]

#foundTagsX = soup_RTSearchHTML.find_all('a') # This works.
#print(foundTagsX)

# This works, dont fuck it up.
foundTags = soup_RottenTomMovPageHTML.find('a', string = re.compile(movTitle))

#print("::",movTitle)
#print("::",foundTags)
# var.get_text() extracts all text within the tag, including nested tags
linkLabel = foundTags.get_text()
linkLabel = (linkLabel.strip())
print(linkLabel)
linkUrl = foundTags.get('href')
print(linkUrl,"\n")

foundTags = foundTags.search("test")
for x in foundTags:
    if foundTags.search("test"):
        print(x)

for result in foundTags :
    if len(result.attrs) == 1 :
        print(result)

##################################################

## Terminal report.

    terminalOutput = (f\'''

{b}
Terminal Output...

{linkLabel}
{releaseYear}
{cast}
{rtScore}% - Rotten Tomatoes Score
{pcScore} - Popcorn Meter

Directed by {dirText}
{dirLink}

Summary:
{tagLine}{descText.strip()}

Age Rating:
{ageRating}

YouTube Trailer:
{ytTrailerLink}

Rotten Tomatoes Movie Page:
{linkUrl}

Letterboxd Movie Page:
{url_LTRBX_movPage}

Streaming Options:
{showTimes}{fandango}{disneyPlus}{hulu}{amcPlus}{netflix}{max}{prime}{paramountPlus}{peacock}{appleTv}{starz}{error56}

JustWatch Movie Streaming search results:
{jwSearchResults}

Films similar to {movTitleRT.capitalize().replace("_"," ")}
{filmsSimilar}

Thumbnail URL:
{thumbImage}

Enlarged Thumbnail URL:
{largeImage}

Reviews from Letterboxd:
## This * asterisk operator unpacks values from iterables like this list.
## Code was: *threeReviews sep='\n'
{threeReviewsLTR}


IMDB page:
{imdbLink}

TMDB page:
{tmdbLink}

Wikipedia page search results:
{wikiGuessUrl}

Metacritic Movie search results:
{metaCriticPage}

YouTube Music - Movie Soundtrack search results:
{ytMusicSTGuessUrl}

{b}

    \''')


    #print(terminalOutput)


##################################################

## Txt file writing and reading.

    if os.path.exists(file_path):
        os.remove(f"{file_path}")
    else:
        pass

    ## Create a new file.
    f = open(f"{file_path}", "x")

    ## Open a file in overwrite mode with ('w').
    with open(f"{file_path}", "w") as f:
        f.write(f\'''

JeverSee Txt File Movie Report//

{linkLabel}
{releaseYear}
{cast}
{rtScore}% - Rotten Tomatoes Score
{pcScore} - Popcorn Meter
Directed by {dirText}
{dirLink}

Summary: {tagLine}{descText.strip()}

Age Rating: {ageRating}
YouTube Trailer: {ytTrailerLink}

Rotten Tomatoes Movie Page: {linkUrl}
Letterboxd Movie Page: {url_LTRBX_movPage}

Streaming Options:
{showTimes}{fandangoHtmlLink}{disneyPlus}{hulu}{amcPlus}{netflix}{max}{prime}{paramountPlus}{peacock}{appleTv}{error56}
JustWatch Movie Streaming search results: {jwSearchResults}

Films similar to {movTitleRT.capitalize().replace("_"," ")} {filmsSimilar}

Thumbnail URL: {thumbImage}

Enlarged Thumbnail URL: {largeImage}

Reviews from Letterboxd:
{"\n".join(threeReviewsLTR)}


IMDB page: {imdbLink}
TMDB page: {tmdbLink}
Wikipedia page search results: {wikiGuessUrl}
Metacritic Movie search results: {metaCriticPage}
YouTube Music - Movie Soundtrack search results: {ytMusicSTGuessUrl}


    \''')



    ## Read the report it just wrote to txt.
    print(b)
    with open(f"{file_path}", "r") as f:
        #print(f"Here's what I read from that JVS Movie Report:\n\n"+f.read())
        print("## There's too much vertical terminal space being used so im hiding the txt report read for now.")
    print(b)



'''

print("\n\n\n")