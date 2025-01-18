
# load stuff 

import pandas as pd


orders_df = pd.read_csv('orders.csv')

emails = orders_df['Email Address'].values.tolist()
phone_numbers = list(map(str, orders_df['Cell Phone'].values.tolist())) 
for pnidx in range(len(phone_numbers)): # assumes they're all in Singapore 
    phone_numbers[pnidx] = '65' + phone_numbers[pnidx] 
names = orders_df['First Name'].values.tolist()
#event_names = orders_df['Event Name'].values.tolist() # should be unnecessary 
num_ticketss = orders_df['Tickets'].values.tolist()

additional_event_details = """Date: 19 Jan 2025
Location:
NUS High School of Mathematics and Science
20 Clementi Avenue 1
Singapore 129957
"""




# setup whatsapp api

with open("wa_access_token.txt", 'r') as f:
    wa_access_token = f.readline().strip()
with open("wa_phone_number_id.txt", 'r') as f:
    phone_number_id = f.readline().strip() 


import requests
wa_url = 'https://graph.facebook.com/v21.0/{}/messages'.format(phone_number_id) 
wa_header = {'Authorization': 'Bearer {}'.format(wa_access_token),
          'Content-Type': 'application/json'}


def send_wa_msg(to, msg:str): 
    wa_data = { "messaging_product": "whatsapp",
         "to": str(to),
         "text": {"body": msg},
                }

    return requests.post(wa_url, json=wa_data, headers=wa_header) 


def send_wa_verify_attendance_msg(to, name:str, event_name:str, details:str , ): 
    wa_data = { "messaging_product": "whatsapp",
         "to": str(to),
         "type": "template",
         "template": { "name": 'verify_attendance',
                       "language": { "code": "en_US" },
                       "components": [{"type": "body",
                                       "parameters": [{"type": "text",
                                                       "parameter_name": "name",
                                                       "text": name},
                                                      {"type": "text",
                                                       "parameter_name": "event_name",
                                                       "text": event_name},
                                                      {"type": "text",
                                                       "parameter_name": "details",
                                                       "text": "details"}
                                                      ]
                                       }],
                       }
                }

    return requests.post(wa_url, json=wa_data, headers=wa_header) 


def send_email(to, name, details):
    email_body = """Dear {name},

TODO write email
{details}

Regards,
Merlion Project 
""".format(name=name, details=details)
    # TODO send email - requires credentials for email address used to send email
    print("EMAIL FEEATURE NOT IMPLEMENTED YET (no credentials for an email address have been set up yet)")
    print() 

    


# verify attendance
def send_verify_attendance_message(event_name, name, phone_number, email, details):
    # try sending whatsapp message first
    res = send_wa_verify_attendance_msg(phone_number, name, event_name, details)
    if res.status_code > 299: # means there's an error
        print("ERROR SENDING WHATSAPP MESSAGE TO {} ({}): {}".format(name, phone_number, res.content))
        print("EMAILING INSTEAD")
        print()
        # email
        return 1, send_email(email, name, details) # (1, ???) for email
    return 0, res # (0, Response) for whatsapp 

def details_from_num_tickets(num_tickets):
    # if there's any more details we want to add, this is to be modified 
    return "Number of tickets: {}".format(num_tickets)+'\n'+additional_event_details 





# functions used
def send_verify_attendance_message_to_all(event_name):
    ress = [] 
    for i in range(len(names)):
        ress.append(send_verify_attendance_message(event_name, names[i],
                                                   phone_numbers[i], emails[i],
                                                   details_from_num_tickets(num_ticketss[i])))
    return ress 




if __name__=='__main__':
    ress = send_verify_attendance_message_to_all("Test Event") 


'''
# testing 
ress = []
for pn in phone_numbers:
    #ress.append(send_wa_verify_attendance_msg(pn, "Simu", "test event", "details hehe"))
    ress.append(send_wa_msg(pn, "test message by simu to test whatsapp business api"))
'''




    
