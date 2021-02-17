# MMG python tech 

### Installation

Python 3.7.7

pip 21.0.1

```pip install -r /path/to/requirements.txt```


The path to solve the proposed project, in my case was take one step at a time, so lets see each problem by it self.


### 1. Calculate the number of lines and the average of the field 'tip_amount':

First of all we need to connect with the AWS(Amazon) service, where the data is storaged. To be able to do that, we are going to use the native library Boto3. In this case, we need to extract the information relevant from the URL given, ie bucket and key. Then process the column we are asked for �tip_amount�, trying to have the file  processing as light as we can, since we cannot manage the download process. The first time we are asked for this information, we could keep it in the server, so we dont connect with Amazon again, but seems to be a must in the proyect. Afger we have the file and the data available, I've choosen pandas for the cals since it's a bast extended library, needing the data as dataframe, while is available as  botocore.response.StreamingBody. Once the data is readed (only the column we need), just use the methods panda gives us. 

Perhaps using an algorithm able to calculate mean iteratively, could be faster/lighter, but pandas is so extended that we trust it solution is more than sharped. Remember to hide the sensitive information (accounts/passwords).


### 2. The endpoint must receive the necessary values on which the model will work to make the prediction, must return this prediction and, in background, store it in a MongoDB:

This point is way bigger than the before one. In the beginning, we need to choose how to make the prediction, in this case the choosen is XGBoost, since it's the most used in kaggle. Having a copy of the date in locale will help us trying to achive a good params setup. For this purpose we are going to use Jupyter, being agile and visual makes the task easier and faster. Pandas, numpy and Xgboost among (us) others are required. Try to coock the data a little  at least, take care with long/lat missing (ie: others at NYC), take the year out of the field since we are not going to predict in the past... Looking at long/lat date hour can establish if its at night or day, that could be interesting in the future, as working day or not could be another option. Same as done with Amazon we are going to use the XGBoost structure so take care injectig the data as Dmatrix. Toons of validations can be done at this point, but lets trust the incoming data is well formatted.  If the requirements are met, we connect with the data base, (MongoDB), so we could check if the prediction is alredy done and serve the information at this point. In case is a new one, call the model and use the method XGBoost gives us to do this. After the response from the model is done, storage it in the data base as, we are aseked for.

The model could be more accurated, but being arround 90% is close enought to the purposewe are atrying to achive in this case. 

There are a lot of improvements that could be done, some of those are said in the text on top of this, but the proyect is brief and the time was spent on studying and trying to fit as close as posible while being solved straigforward. 
The file structure is not pointed so an small example of one that could be use is done but could be improved, just showing how to be done.