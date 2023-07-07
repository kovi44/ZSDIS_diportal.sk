# www.diportal.sk -> get useful data from ZSDIS portal. The API is not available yet for standard ZSDIS customers

The output of this script is JSON which can be used for future usage. It contains userdata, and interval and register values. So you can easily get hourly, daily, monthly power consumption.

The diportal is secured by Google reCaptcha. Due to that fact there exist two possible ways how to use the script<br/>
#1 - use 2captcha.com subsrciption (cheap and reliable service), then place your api key in script <br/>
#2 - collect diportal cookies manually and place it to file - cookie.txt. The way how to do it. Open Chrome browser, install plugin "Get cookies.txt locally". Then open diportal.sk, log in and then open plugin and save cookies to the file [netscape format]. As soon as script recognise a valid cookie, it will collect all your requested data.<br/>

With reCaptcha enabled the script runs for more then 30-40sec. 


OUTPUT of the script | 3 different types | you can define via variable<br/>
text - it will output some data in pure text form, fine for debuging<br/>
short - it's used like for my case where I just need to find the delta between production and consumption site [FVE powerplant production versus House consumption]<br/>
full - it's the complete output of diportal useful data such as register or interval data, you can used to built nice graph via grafana or do deeper analysis<br/>

Notes: this is just a proof of concept!

