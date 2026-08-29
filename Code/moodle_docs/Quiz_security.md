# Quiz_security

> Sumber: https://docs.moodle.org/502/en/Quiz_security

Just starting this page. When I have done some more I'll link it to the quiz menu here: <a href="https://docs.moodle.org/502/en/Quiz_settings" class="external free" rel="nofollow">https://docs.moodle.org/502/en/Quiz_settings</a>. Please check for completeness and accuracy. --[Derek Chirnside](User_Derek_Chirnside.md) 08:52, 3 April 2013 (WST)

In Moodle, a quiz is served up by the Moodle server. If you want to have various options for security further to those in the quiz settings, these need to be implemented at the computer end.

It is not possible to lock down a browser via the internet by activity from a server. This is regarded as a bug, basically an exploitable function that could be used maliciously. What this means is that there is no way to set up remotely a "secure" browser where test takers cannot look at other Moodle and access other online material (etc.) when sitting a test.

There are some options if you have students sitting assessments in a controlled environment (like the classroom) but these can be difficult and time-consuming to implement, and they then take away from other flexibilities that online testing allows.

There is some advice about online testing options in the page on [Effective quiz practices](Effective_quiz_practices.md#Quiz_security_and_cheating "Effective quiz practices"). These generally include planning assessments a little differently.

## Built in security

Check out Administration\>Plugins\>Activities\>Quiz

*There are many posts in the forums on locking down browsers for security. A few points are summarised in the next section*

## Windows policies on the network

Essentially, by tweaking policies on a network you can lock a computer to only be able to access a browser, to disable Alt-Tab and to set the browser to go to only one domain (i.e. your test). here is a random URL: <a href="http://support.microsoft.com/kb/307882" class="external free" rel="nofollow">http://support.microsoft.com/kb/307882</a>

## Using a 'Safe Browser'

Tim has commented here: <a href="https://moodle.org/mod/forum/discuss.php?d=153953#p677304" class="external free" rel="nofollow">https://moodle.org/mod/forum/discuss.php?d=153953#p677304</a> There are many browser options. Two are

### 1. Exam Safe Browser

<a href="Safe_exam_browser.md" class="mw-redirect" title="Safe exam browser">Safe exam browser</a>

The home base: <a href="http://www.safeexambrowser.org/about_overview_en.html" class="external free" rel="nofollow">http://www.safeexambrowser.org/about_overview_en.html</a>

Latest tracker activity: <a href="https://tracker.moodle.org/browse/MDL-31365" class="external free" rel="nofollow">https://tracker.moodle.org/browse/MDL-31365</a>

### 2. Respondus option: locked down browser

<a href="http://www.respondus.com/products/lockdown-browser/index.shtml" class="external free" rel="nofollow">http://www.respondus.com/products/lockdown-browser/index.shtml</a>
