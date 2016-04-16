# How to add IFTTT and Amazon Echo support for your Smarter Coffee machine 

This is an unofficial method to add IFTTT support for your Smarter Coffee 

**Demo:** https://youtu.be/xBiNRYtx880

Working with firmware 20 

**What you need:** 

 - Smarter Coffee Machine - http://smarter.am/coffee/  
 - A server to run node and python script. (I use a raspberry pi) 
 - Amazon Echo 
 - Know how to edit a file in linux

**Overview over the setup**

![Overview over the setup](https://lh3.googleusercontent.com/6hHJHuASlAYxphCfqVQxnh36pUBwgA0XO4cKyam4ej2dEqQ7PahzrJ5KnL4sVbECcZXp9w=s0 "Overview over the setup")


**How to set up the node server:** 

 1. Clone the repository: 

      git clone https://github.com/krsandvik/IFTTT-SmarterCoffee
      cd IFTTT-SmarterCoffee 
      apt-get install git (if git is not installed) 

 2. Find your IP for your coffee machine, You can logon to your router
    and check your DHCP lease for something like *ESP_F211F* or use `nmap -p 2081 192.168.x.x-255`
 3. Edit *pollingStatusMessage.py* and *sendcommand.py* with your favorit editing tool and add coffee machines IP in line 17 and 16
 4. Edit the app.js like you choose your coffee.   
 5. Run`python pollingStatusMessage.py` the respons should be something like this:
  

      {"cups": 2, "status": "Grinder, OK to start", "water" : "Half",
        "strength" : 2}

 6. Configure node and npm: 

	 sudo apt-get install nodejs
     sudo apt-get install npm 
     sudo ln -s /usr/bin/nodejs /usr/bin/node

	Verify install:  

	 node -v 
	 v4.2.1

	 npm -v 
     2.14.7

 
 7.  Run *sudo npm install* in where your app.js file is.
 8. run `sudo node app.js` and see if it starts response should be `"listening on port 3000"` 
 8. Configure node to run on startup 

     sudo mv smartercoffee_startconfig /etc/init.d/smartercoffee

 change the paths in */etc/init.d/smartercoffee* to your where your config are. Reboot to check that app.js has started `ps -aux | grep app.js`
 
 8. Test with postman if your node server works https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm 

	URL: yourip:3000/status 
	Type: GET 
	Response should be 
	
	  {"cups": 2, "status": "Grinder, OK to start", "water" : "Half",
	    "strength" : 2}

 
 
**How to connect IFTTT**

 1. Port forward  port 3000 to your coffee machine 
 2. Connect https://ifttt.com/amazon_alexa to your IFTTT account 
 In "What phrase?" you can put in whatever you want Alexa want to respond to. **Note:** you need to say **alexa trigger four cups of coffee**
 
 ![IFTTT Echo config](https://lh3.googleusercontent.com/71PSx4gccBjrCd0o02bCMnaDjDFKelqnjZ3O3J-6gOgggqlUWipQV-4m8j8ngK3jQpNNEQ=s0 "Screen Shot 2016-04-16 at 00.33.35.png")
 
 3. Connect https://ifttt.com/maker to your IFTTT account 
 
 ![Maker config](https://lh3.googleusercontent.com/Zg4tWCDK54iiAa3t2nv2NaFxffiDgdCsvB3c4M88M_5_qEXdLqv-0E3t8x5mhR9elqoSDw=s0 "Screen Shot 2016-04-15 at 23.58.45.png")
 

 **Configure get status** 
 

 1. Get your maker key from https://ifttt.com/maker ![enter image description here](https://lh3.googleusercontent.com/70CAG8qZdisw5GCUs3EMekkqwugOjab8JMTa5lUbYytroAy1tjXQHHq6NMXvxz6P2QP4cw=s0 "Screen Shot 2016-04-16 at 12.53.54.png")
 2. Add your key her in app.js "https://maker.ifttt.com/trigger/status/with/key/
 3. Then you can configure your custom push service on IFTTT to send you status on your coffee machine 

Thanks to nanab for the python script https://github.com/nanab/smartercoffee








