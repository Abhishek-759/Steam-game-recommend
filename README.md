# Steam Recommender System
<h3> Web Application description </h3>
This code will give you access to code for steam game recommender system developed by Abhishek and his team. <br>
The system is built on a dataset comprising of total of 8183 games (All the datasets used are available in the links given below <br>
Within the application, You get recommendations based on 4 preferences/ game name search.<br>
The recommendation based on game name search is done using KNN model. The UI is built on streamlit Library in Python. 

<h3> Pre-requisites </h3>
1. Make sure git is installed in your system and added to your path variable.
   For more details follow: https://git-scm.com/download/win <br>
2. Install heroku.
   Follow the link for download and steps for installation: https://devcenter.heroku.com/articles/heroku-cli#download-and-install <br>
3. Download and extract the dataset in the same folder where the code and output files are stored. (Do not change any paths/file names) <br>
   Link: https://drive.google.com/file/d/1C9aigoVC9YIMWwkQEvevwIFm8Jlm47R8/view <br>
4. (For developers) All the steps mentioned below are done in PyCharm. It is advised to install the software in your laptop. Follow: https://www.jetbrains.com/pycharm/download/#section=windows <br> 
5. If you delete your output files/change the datasets to updated ones, you can open the python code (.py file) in PyCharm and run it again. This creates new set of output files.

<h3> Getting started </h3>
1. After completing all the Pre-requisites, Open terminal and change your directory to the folder where all the code, input & output files are stored. <br> 
2. Log in to your Heroku account. <b>Copy paste the code in terminal without the '$' </b><br>
&emsp;$ heroku login<br>
3. Create a remote git repository<br>
&emsp;$ git init<br>
4. commit and push your changes<br>
&emsp;$ git add .<br>
&emsp;$ git commit -am "make it better"<br>
5. Deploy the app<br>
&emsp;$ heroku create<br>
&emsp;$ git push heroku master<br>
6. Now, you can go to https://dashboard.heroku.com/apps and check your web application, change its name and have full control over it. <br>

<h4> There you go. Your website is deployed and completely functional! <br>
<h5> To check the working model of the app, go to: https://steam-recommendation.herokuapp.com/
