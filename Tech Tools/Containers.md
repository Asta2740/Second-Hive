## Docker

The Problem

Let's talk about the Open VPN problem , that you had to go for ubunutu 22 but if it was deployed in a container it was going to be isloated from all of these and works normally 

so the problem it fixes are

 1- installation : each OS kinda have its own quircks to install something , it standarizes it
 2- setup conflicts : some services might require python 13 other python 12 , so saves you from this hassle
 3- trouble shotting problems : it's isolated from the enviroment so the problem will be within the app


So lets say you want to upgrade a container , you kinda rebuild it through the docker file
and make sure to externalize your data always

and if it's a privilied container , you can pivot out of it