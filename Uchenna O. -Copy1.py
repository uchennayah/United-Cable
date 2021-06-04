#!/usr/bin/env python
# coding: utf-8

# ## Library Import

# In[1]:


from datetime import datetime as dt
from requests.utils import requote_uri
import http.client
import json


# ## User Interface

# In[2]:


user_complain = {}


# In[3]:


# create signup and complaint page page
# create empty dictionary for collating unique ID of the person.


def complain():
    complaint_id = 1
    while True:
        name = input("Please enter your name: ")
        print("Welcome to our United Cables Complaint Management Unit, {}".format(name))
        product_id = input("Enter the ID of your service complaint: ")
        date = dt.now()
        issue = input("Please enter your complaint: ")

        if product_id in user_complain.keys() or name in user_complain.values() or date in user_complain.values() or issue in user_complain.values():
            print('==========================')
            yes_no = input("Your complaint has already been registered.\n Do you want to register another complaint?!\n Y for Yes and N for No: ")
            if yes_no.lower() == "y":
                continue
            elif yes_no.lower() == "n":
                print("Thank you very much. You will be contacted with feedback.")
                break
            else:
                print("Your response is invalid.")
                continue
        elif name == "" or product_id == "" or date == "" or issue == "":
            print("Your response is invalid. Please restart.")
            continue
        else:
          user_complain[complaint_id] = {"product_id": product_id, "name": name, "date": date, "complaint": issue}
          print('Complaint logged successfully!')
          complaint_id += 1
          yes_no = input("Do you want to register another complaint?!\n Y for Yes and N for No: ")

          if yes_no.lower() == "y":
                continue
          elif yes_no.lower() == "n":
                print("Thank you very much. You will be contacted with feedback.")
                break
          else:
                print("Your response is not valid.")
                continue


        


# In[4]:


complain()


# ## Backend- API

# In[5]:


def api_request(coded_complaint, output_language_code):
  conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")

  headers = {
      'content-type': "application/x-www-form-urlencoded",
      'accept-encoding': "application/gzip",
      'x-rapidapi-key': "390c37a65fmsh03237005c27868ep1a87c4jsnd56c83ef5e73",
      'x-rapidapi-host': "google-translate1.p.rapidapi.com"
      }

  payload = "q=" + coded_complaint + "&target=" + output_language_code
  print(payload)

  conn.request("POST", "/language/translate/v2", payload, headers)

  res = conn.getresponse()
  data = res.read().decode("utf-8")
  return data


def translateFunction(user_complain):
  complaint_choice_id = int(input("Please enter the complaint ID of choice you want to translate: "))

  complaint_choice = user_complain[complaint_choice_id]['complaint']
  print(complaint_choice)

  coded_complaint = requote_uri(complaint_choice)
  print(coded_complaint)

  output_language_code = input("Please enter the expected output language: ")
 
  print(output_language_code)

  api_call = api_request(coded_complaint, output_language_code)
  print(api_call)

  result_dict = json.loads(api_call)
  print("Translation dictionary: ", result_dict)

  complaint_language = result_dict["data"]["translations"][0]["detectedSourceLanguage"]
  print("The complaint you selected was entered in ", complaint_language)

  translated_result = result_dict["data"]["translations"][0]["translatedText"]
  print("This selected complaint, ", complaint_choice, " translated from ", complaint_language, " to ", output_language_code, " is ", translated_result)


# In[ ]:


print(user_complain)


translateFunction(user_complain)


while True: 
  proceed_target = input("Translate another complaint? ")
  if proceed_target.lower() == "yes":
    translateFunction(user_complain)

  elif proceed_target.lower() == "no":
    break
  else:
    print("This is not a supported entry. Supported entries are yes and no.")
    continue


# In[ ]:




