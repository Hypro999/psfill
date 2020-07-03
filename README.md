# psfill
In order to fill out your PS I or PS II preferences, you have to use the BITS PS department's [portal](http://psd.bits-pilani.ac.in).

There you'll find this absolutely *beautiful* UI (note the sarcasm in my voice here) where you have to slowly drag and drop
hundred of tiles to get the ordering you want. No filters, no sorting tools, nothing. Everything has to be done manually.
This is slow, painful, and completely pointless.

Let's make something here clear: The portal's UI is absolutely stupid and damn painful to use.
Who ever made this portal is a **complete** idiot. Let's just leave it at that (but seriously, what the heck were they thinking?!).

I didn't want to put up with that BS so I took the time to analyze the portal and then build this tool where you can simply create
a text file with the order you want, specify your username, password and what cities you can provide your own accommodation in,
and then run this script and be done with it.

### Dependencies
You'll need Python 3 to run the script and Pip for Python 3 to install some dependencies for this script. If you don't already have
them, then you will have to refer to other sources on the internet for how to download and install them.

1. Clone this repo. If you have git then use: `git clone https://github.com/Hypro999/psfill.git` If you don't then you can
simply [download](https://github.com/Hypro999/psfill/archive/master.zip) a zip file for this code and then extract it.

2. Install the required libraries. Since this code uses the [requests library](https://github.com/psf/requests) and
[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) we will need to install them and their dependencies.
This is pretty easy, just run `pip install -r requirements.txt` from inside the repo (folder). For people already
comfortable with Python, you can use a virtualenvironment since even if you have the libraries, the versions might differ.

### Configuration
1. Create a new folder for storing your configurations inside this repo called `.config`.

2. Create a file called `credentials.txt` inside this configuration folder and in it, add your credentials like so:
```
username: mybitsemailid
password: mypsdportalpassword
```
If you want to specify which cities you can provide acco for, then you can specify them as comma separated values
under a `acco` field. For example:
```
acco: Hyderabad
```
or
```
acco: Hyderabad, Bangalore
```
Mind the case though. The city names mirror the ones provided in the PS portal. So keep that in mind since they themselves
weren't too consistent for some entries.

3. Now specify your preference order in the a file named `stations.txt` inside the configuration folder. To generate a default
file (alphabetically ordered), you can run `python main.py -g`. Now you can easily reorder these to your liking (e.g. in vim you
can use stuff like `d5j` to take a block of stations and thenmove them to the wherever you want. In other text editors you can
select multiple lines using the shift key or your mouse. You get the idea).

### Usage
1. Complete the steps listed under `Configuration`.

2. Now all we have to do is run the script with `python main.py`.

3. Login to the portal and just make sure that everything looks alright. Don't blame me if something goes wrong, use
this script at your own risk (though it should be pretty safe to use, I've tested it quite a bit and am using it for
myself).

Note: This tool hasn't been dockerized since that would be pretty unnecessary/overkill for a simple tool like this
which has only a few dependencies and can easily be run cross-platform.

### Contribution
Want to contribute and make this script better? Awesome! Just open a PR or an issue and we can talk about it. I'd
be really happy to merge good changes into this codebase.
