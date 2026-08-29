# Guest_access

> Sumber: https://docs.moodle.org/502/en/Guest_access

The Guest access facility allows users with the [Guest role](Guest_role.md "Guest role") to view the contents of a course. This might be used, for example, if a Moodle site serves as a website where certain courses contain publicly available information, or else with a commercial Moodle site where courses with guest access can offers a "taster" of the kind of courses which may be purchased. (Note that the guest cannot participate in any activities; they can only view content.)

## Course settings for guest access

1.  From Course navigation, click 'Participants', and then from the dropdown, click 'Enrolment method\> Guest access'. With other themes, click *Administration \> Course administration \> Users \> Enrolment methods* and then Guest access.
2.  Enable guest access by clicking on the "eye" icon or by choosing it in the 'Add method' dropdown menu.
3.  If you wish to set a password, then click the configure icon and type in your password here.

## Admin settings for guest access

- In *Administration \> Site administration \> Plugins \> Enrolments \> Manage enrol plugins*, ensure Guest access is enabled (has its eye open.) This enables Guest access.
- In *Administration \> Site administration \> Plugins \> Authentication \> Manage authentication* set the Guest login button to Show if you want the button on the login page.
- Also Guest accounts can be logged - check the *Administration \> Site administration \> Plugins \> Logging \> Log guest access* setting.
- A site policy for guests may be set in *Site administration \> Security \> Site policies*. Guests then have to agree to the site policy before accessing a course with guest access.

### Default settings for guest access

- Clicking on *Administration \> Site administration \> Plugins \> Enrolments \> Guest access* brings up the screen where admin can set defaults for guest access in courses.
  - Clicking the 'Advanced' button next to 'Allow guest access' will hide this setting in a course and will instead display a 'Show more' link to click on to access the setting.
  - Guest access can be turned on by default in all new courses and you can also:
  - require each course with guest access to have a password for guests. (Note: this can confuse teachers who are not aware of the requirement.)
  - use or ignore your Moodle's standard password policy for guest access passwords
  - offer if needed the first letter of the password as a hint.

### Auto-login guests

- In *Administration \> Site administration \> Users \> Permissions \> User policies*, you can tick the box so that visitors are automatically logged in as guests when accessing a course with guest access (i.e. they don't have to click the "login as guest button").
- *Administration \> Site administration \> Plugins \> Authentication \> Manage Authentication*, you must have "Guest login button" set to "Show". **Note: For Moodle 4.2.2 and later, this is no longer necessary.**
- In *Administration \> Site administration \> Security \> Site policies* you can check "Open to Google" setting so that the Google search robot will be allowed to enter your site as a Guest. In addition, people coming in to your site via a Google search will automatically be logged in as a Guest.

## See also

- [Guest role](Guest_role.md "Guest role")
- <a href="https://moodle.org/mod/forum/discuss.php?d=347107#p1400235" class="external text" rel="nofollow">Re: Guest access to course sections!</a> forum post
