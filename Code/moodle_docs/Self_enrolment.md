# Self_enrolment

> Sumber: https://docs.moodle.org/502/en/Self_enrolment

**Note:** If you want your learners to create accounts on your site and have access to your courses, then you first need to enable <a href="Email-based_self_registration.md" class="mw-redirect" title="Email-based self registration">Email-based self registration</a> so they can create accounts, and then enable self enrolment within your course(s) so they can enrol. These are two separate steps.



Self enrolment is the method whereby users can choose to enrol themselves into a course, either immediately by clicking "Enrol me in this course" or by typing in an enrolment key they have been given. The enrolment plugin needs to be enabled by the site admin in [Enrolment plugins](Enrolment_plugins.md "Enrolment plugins") and has to be enabled within the course. The manual enrolment plugin has to be enabled in the same course as well.



## Enabling self-enrolment in a course



1.  In your course, go to *Course navigation \> Participants*.

2.  From the dropdown select Enrolment methods.

3.  Enable Self enrolment by clicking the eye icon.

4.  Access the settings by clicking the pencil icon.



### Enrolment key



If you wish only a certain group of users to self enrol (and not anyone) then you can set an enrolment key which you then tell them to use when they access the self-enrolment screen. See section 1 of [enrolment key](Enrolment_key.md "Enrolment key") for how to do this.



If you wish your users to enrol themselves directly into a group in the course then you can set a group enrolment key which you then tell them to use **instead of the course enrolment key you will have also set** when they access the self-enrolment screen. See section 2 on the [Enrolment key](Enrolment_key.md "Enrolment key") page for how to do this.



### Enrolment duration



Set the amount of time a user enrolment is valid, starting with the moment the user enrols themselves. If disabled, the enrolment duration will be unlimited.



### Notifying users when their enrolment expires



You can choose to notify students and/or teachers when enrolments expire. If there is more than one user with the role of teacher, then the notification is only sent to the first user to be assigned the role of teacher (or other user with the capability to manage self enrolment).



### Allowing only cohort members to self-enrol



If you have cohorts set up, then you can restrict self enrolment to particular cohorts by selecting the name of the cohort from the drop down box, A member of the cohort can self-enrol as normal; whereas a non-member gets a message telling them they are not able to self-enrol.



### Course welcome message



If enabled, users receive the following course welcome message via email when they self-enrol in a course:



*Hi {\$a-\>firstname}, you are enrolled in the course {\$a-\>coursename}.*



You can edit the text and change it as you wish.



An admin can customise the message for the whole site by editing the *welcometocoursetext* language string. See [Language customisation](Language_customisation.md "Language customisation") for further details. However, if the *welcometocoursetext* language string is used, only the placeholders coursename and profileurl may be used.



## Admin settings



The self enrolment plugin may be enabled or disabled for the site in *Site administration \> Plugins \> Enrolments \> Manage enrol plugins.*



### Shared settings for all courses



Location: *Site administration \> Plugins \> Enrolments \> Self enrolment*.



- Require an enrolment key - if this box is ticked then all courses with self-enrolment enabled will need to have an enrolment key. The setting won't save until the teacher adds a key - something to be aware of as this can cause confusion:)

- Use password policy - tick this box if you want enrolment keys set by teachers to follow the password policy of the site.

- Show hint - tick this box if you are prepared to allow the first letter of a key to be given as a "hint"

- Enrolment expiry action - specifies what happens when user enrolments reach expiration date. Please note that option "Unenrol user from course" purges grades, group memberships, preferences and other user related data from the courses.

- Hour to send enrolment expiry notifications - specify hour for sending expiration notifications.



### Default enrolment settings in new courses



- Add instance to new courses - if admin selects this, then any new course created will include the self enrolment plugin

- Enable self enrolments- if this is enabled then users by default can self enrol into a course.

- Use group enrolment keys - the setting for group enrolment keys in a course will be set to "yes" by default

- Default role assignment - normally, when users self enrol, they have the student role. If necessary that role can be changed by default here - for example - if your Moodle has a dedicated role you wish to use instead.

- Enrolment duration - this sets the default enrolment length for new courses (but again, may be altered by the course teacher.)

- Notify before enrolment expires - specifies if teacher or optionally students should be notified before the expiration.

- Notification threshold - specify how many days should be users notified before the enrolment expiration.

- Unenrol inactive after- this sets the default time after which a student will be unenrolled if they haven't accessed the courses. (Teachers may change this)

- Max enrolled users - adding a number here will specify the maximum number of users who can self-enrol into new courses. Teachers in the course can change this. If it is left at 0, there will be no maximum.

- Send course welcome message- if this box is checked then newly enrolled users will receive a welcome message by default.



## Self enrolment capabilities



- [Configure self enrol instances](Capabilities_enrol_self_config.md "Capabilities/enrol/self:config")

- [Manage enrolled users](Capabilities_enrol_self_manage.md "Capabilities/enrol/self:manage")

- [Unenrol users from course](Capabilities_enrol_self_unenrol.md "Capabilities/enrol/self:unenrol")

- [Unenrol self from the course](Capabilities_enrol_self_unenrolself.md "Capabilities/enrol/self:unenrolself")

