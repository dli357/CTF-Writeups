Joe - Writeup

>Disclaimer: This was solved after the competition ended, though no help was given either way.

From the get-go, this problem seemed interesting. When you first visit the website located at joe.web.ctfcompetition.com, you get this screen:

>Hello there!
>We don't know each other yet, so let me introduce myself.
>I'm Joe, your "intelligent" conversation partner.
>If you don't like my name, you can change it any time.
>I can do a lot of useful things, such as small talk and ...
>Well, that's basically the only thing for now, but I'm constantly learning new things, so stay tuned.
>My memory is time limited, but it's persistent accross browser sessions if you log in.
>If you encounter any problems while talking with me, I can forward bug reports to my administrator who will take a look promptly.
>If you are the administrator, please proceed to the admin page.

Clearly, just from reading this text, you take notice of three major functions:

You can ask it to make small talk, which simply causes him to tell jokes or say other things. This seemed the least consequential of the three functions. You can log in to preserve your session, and you can also rename him.

Additionally, we can see a link to a page for an admin, but when we visit it, it just says:

>Sorry, you're either not listed as admin user, or you don't have your FLAG cookie set to the secret value.

Clearly, we're after the admin's flag; if we can use stored XSS, or cross-site scripting, to steal the admin's cookie, we'll be able to access the flag!

Thus, I began to look for places on the website that were vulnerable to XSS. Remember the function that allowed you to rename Joe earlier? If you refresh the page, you'll notice that Joe responds with:
>Hello there, it's Joe again.
>Please log in so that I can remember you and your preferences between browser sessions.

We notice that he repeats his name. What happens if we change his name?
>Hello there, it's ABCDETESTTESTtesttest again.

Hmmm... What if we take it further? Here, I tried to embed script tags into the name, since it would load when you refreshed the page. And I was successful! Using alert(), we were able to inject XSS.

Here, I ran into a roadblock. What would allow us to show this XSS to the admin? If I delete my session cookie or log in as another user, the name resets.

The answer was in the login process. Using Chrome developer tools, I managed to catch the entire login proces, and I found an interesting link that included a session ID. By sending that link to the administrator through the bug report function, I was able to capture his cookie and get the flag!
