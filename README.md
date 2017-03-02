AvatureCheck

A python program to check a list of new leads or candidates to see if they exist in Avature.

3/2/17  - Gerald
I've merged the addConfig with the main branch as addConfig is working propperly it will be the master.

Other features that I plan on adding are:

  * UI both cli and gui, along with command line arguments
  * Optional prechecking and storing of terms to reduce load on Avature severs
  * Add multiple attempts to load a page.  Currently it only tries to get a page once and if that fails it goes to the next.
  * Multi-value checking logic allowing to check for term A OR term b, or check for term A AND term B. Eventually allowing for combinations.
  * Improved setup for testing. This is more of a personal thing as right now I'm just adding print statements and I'm looking for a better way.
  * Setup program installer to allow it to install and run on machines where Python is not used often
