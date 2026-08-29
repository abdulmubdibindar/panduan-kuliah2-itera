# Authentication

> Sumber: https://docs.moodle.org/502/en/Authentication

**Authentication** is the process of allowing a user to log in to a Moodle site with a username and password.

## Authentication plugins

Moodle provides a number of ways of <a href="managing_authentication.md" class="mw-redirect" title="managing authentication">managing authentication</a>, called *authentication plugins*.

Standard authentication plugins are:

- [Manual accounts](Manual_accounts.md "Manual accounts") - accounts created manually by an administrator
- [No login](No_login.md "No login") - suspend particular user account
- [Email-based self-registration](Email-based_self-registration.md "Email-based self-registration") - for enabling users to create their own accounts
- [External database](External_database_authentication.md "External database authentication") - account details are located on an external database
- [LDAP server](LDAP_authentication.md "LDAP authentication") - account details are located on an external LDAP server
- <a href="LTI.md" class="mw-redirect" title="LTI">LTI</a> - works with the [Publish as LTI tool](Publish_as_LTI_tool.md "Publish as LTI tool") enrolment method to connect courses and activities
- [No authentication](No_authentication.md "No authentication") - for testing purposes or if the Moodle site is not available on the Internet. Do NOT use on public servers!
- [Shibboleth](Shibboleth.md "Shibboleth") - account details are located on an external Shibboleth server
- [OAuth 2](OAuth_2_authentication.md "OAuth 2 authentication") - authenticate with an OAuth 2 service
- [Web services](Web_services_authentication.md "Web services authentication") - for a dedicated account which integrates with your site via web services

There are also many <a href="https://moodle.org/plugins/?q=type:auth" class="external text" rel="nofollow">additional authentication plugins in the Moodle plugins directory</a>.

[Multi-factor authentication](Multi-factor_authentication.md "Multi-factor authentication") can be enabled and managed from Site administration \> Plugins \> Admin tools in order to increase site security by requiring additional steps before users can log in.

## Password visibility toggle

Specify whether the password field on the login screen can have the visibility of its contents toggled. This is useful in providing a way to check a password value is entered in correctly. Choose between enabling this setting for all logins, or for logins on small screens only (default). This can also be disabled if required.

For the new installs, Password visibility toggle is enabled (by default) while login.

You can access this feature from *Site administration \> General \> Login \> Login Settings*.

This setting is in sync with the redesigned 5.2 [Login page](Login_page.md "Login page") which includes a fresh look for authentication via Email, SMS, Security Key, and Authenticator App. It displays simplified default login settings to provide a more welcoming first impression for new users. [New feature  
in **Moodle 5.2**!](Category_New_features.md "Category:New features")

  

## See also

- [Multi-factor authentication](Multi-factor_authentication.md "Multi-factor authentication")
- [Authentication FAQ](Authentication_FAQ.md "Authentication FAQ")
