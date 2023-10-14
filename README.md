## EzyURl Shortner

![Weblook](app/static/images/ezy_icon.jpg)

## Introduction

### The project
In today's fast-paced digital world, every second counts. Long and cumbersome URLs can be a
hindrance to efficient online communication. That's where EzyUrl comes in, revolutionizing the
way you share and manage links.

EzyUrl is your ultimate solution to URL simplification. Our user-friendly web app transforms lengthy
web addresses into concise, easy-to-share links. With just a few clicks, you can turn this:

        https://www.examplewebsite.com/blog/article/how-to-use-ezyurl-for-link-management

into this: 

        https://ezyurl.tech/dfgdskt



## The Team

* Khaled Ibrahim [Github](https://github.com/KhaledIbrahemAbdelaziz)--[Twitter]()
    * ``Role``: Debugging and Testing
    * ``Why``: Khaled's debugging and testing skills are crucial for ensuring a smooth user experience and the reliability of the EzyURL Shortener.


* Isaac Ajibola [Github](https://github.com/Bigizic)--[Twitter](https://twitter.com/Big_izic)
    * ``Role``: Backend Development, Debugging, and Testing
    * ``Why``: Isaac’'s strong coding skills and expertise in backend development make him invaluable to our project. His role is crucial for ensuring the reliability and functionality of the EzyURL Shortener.


* Michael Chege [Github](https://github.com/mike-chege)--[Twitter]()
    * ``Role``: Documentation, Frontend Development, Debugging, 
    * ``Why``: Michael's creative approach to frontend development adds aesthetic value to our project. His skills in documentation ensure that our project is well-documented for users and developers alike, and his debugging skills contribute to a seamless user interface.


* Oluwaferanmi Ayodele [Twitter](https://twitter.com/Lonewolfux)--[Instagram](https://www.instagram.com/big_melatonin/)
    * ``Role``: User interface/User experience(UI/UX) designer
    * ``why``: Fernami's creative approach to elegant webdesign makes him invaluable to our project. His skills are webdesign with figma and xd

## Technologies
* Python -
* Javascript
* Html
* Css
* Mysql
* Flask

## Technology Choices
* Database Management: We chose MySQL for its robustness and reliability over alternatives like PostgreSQL. While both are excellent choices, MySQL aligns better with our project's scalability needs.
* Frontend Framework: Initially, we considered React and Vue.js for the frontend. We decided on plain JavaScript for a lightweight and fast user experience, allowing us to cater to a wider audience without sacrificing performance.


## Challenge
### Problem Statement
EzyURL Shortener addresses the issue of cumbersome and lengthy URLs, making online communication more efficient by transforming them into concise, easy-to-share links.

### What EzyURL Shortener Does Not Solve
* Offline Usage: EzyURL Shortener relies on an active internet connection and won't work in scenarios with limited or no internet access.
* Longevity: EzyURL is designed with a limited lifespan in mind. It may not be suitable for content that needs to remain accessible indefinitely.



## Risks
####  technical risks

- ``Service Reliability``: Our services can experience downtime. If a service goes offline, all the shortened links associated with it may become inaccessible.
    - ``What we're doing to solve this``? We've decided to keep backups of all services that allows Ezy to keep running to make it better and more reliable.

- ``Loss of Context``: Ezy links may not provide any context about the destination, making it challenging for users to decide whether to click on them.
    - ``What we're doing to solve this``? We make sure to check if a link is secured before processing requests, we do this by checking the ssl certificate of your link, if it's not secured we'd let you know
 
#### non-technical risks

- ``User Experience``: Most times shortened links aim to simplify URLs, they can sometimes lead to confusion or frustration if users cannot discern the destination easily
    - ``What are we doing to solve this``? We allow customised links making it easy to remember (This service will be available soon)
 
## Infrastructure
### Version Control
We use the GitHub flow for branching and merging in our team's repository. This workflow ensures that changes are well-documented and reviewed before merging into the main branch.

### Deployment Strategy
We deploy our project using a continuous integration and continuous deployment (CI/CD) pipeline, which automates the deployment process, ensuring smooth and efficient releases.

### Data Population
We populate our app with data using automated scripts and user-generated content. The data is stored securely in our MySQL database.

### Testing
We employ a comprehensive testing strategy, including unit, integration, and end-to-end testing. Automated testing tools and manual testing ensure the reliability and functionality of our application



## Existing Solutions
* [TinyUrls](https://tinyurl.com)
    * ``Similarities``: Both TinyURL and EzyURL aim to simplify and shorten long URLs.
    * ``Differences``: EzyURL offers branding and security features, which TinyURL does not.
*    ``Reason for Reimplementation``: EzyURL provides additional features that cater to a broader user base, making it a valuable alternative.

* [Bitly](https://bitly.com)

    * ``Similarities``: Both Bitly and EzyURL offer URL shortening services.
    * ``Differences``: EzyURL emphasizes simplicity, branding, and security, whereas Bitly focuses primarily on shortening URLs.
    * ``Reason for Reimplementation``: EzyURL offers a unique set of features that differentiate it from Bitly, catering to users with diverse needs.
