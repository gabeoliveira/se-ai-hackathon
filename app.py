# 2023 SE AI Hackathon
# Hosted by Rob Masson and Brian Mgrdichian. Special thanks to Pooja Srinath!

# Original code based on Lizzie Siegle's blog at https://www.twilio.com/blog/qa-over-docs-bot-langchain-python
# Unused code has been commented out, but left for context.


# import requests
import nltk
import ssl

# Added NLTK Punkt package for handling SSL with PDF retrieval
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt', quiet=True)

from flask import Flask, request#, redirect

import os
import openai

import json
from types import SimpleNamespace


# No longer using this function. Created a function for loading a PDF below instead
# def loadFileFromURL(text_file_url): #param: https://raw.githubusercontent.com/elizabethsiegle/qanda-langchain-sms-lougehrig/main/lougehrig.txt
#     output_file = "lougehrig.txt"
#     resp = requests.get(text_file_url)
#     with open(output_file, "w",  encoding='utf-8') as file:
#       file.write(resp.text)

#     # load text doc from URL w/ TextLoader
#     loader = TextLoader('./'+output_file)
#     txt_file_as_loaded_docs = loader.load()
#     return txt_file_as_loaded_docs

# No longer used- was taking WAY too long to download the PDF every time
# def loadPDFFromURL(pdf_doc):
#     loader = OnlinePDFLoader(pdf_doc)
#     pdf_file_as_loaded_docs = loader.load()
#     return pdf_file_as_loaded_docs


app = Flask(__name__)
# Adding a route for local testing without SMS: /local
@app.route('/local', methods=['GET', 'POST'])
def local():
    print(request.form)
    inb_msg = request.form['Body'].lower().strip()
    
    response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
        "role": "system",
        "content": "TASK:\nYou are a chatbot that answers FAQ questions about Twilio. Forget everything you knew about the world and Twilio. You MUST NOT provide any information unless it is in the list of FAQ. If the user ask something not in your list of FAQ, apologize and say that you cannot answer.\n\nFAQ:\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Business Continuity Plan\nANSWER: Twilio is a cloud-communication platform hosted on AWS. Twilio's voice and messaging infrastructure is distributed across multiple fault-independent regions and data centers served by our provider. Twilio maintains redundant inbound and outbound connectivity with multiple network carriers and real-time systems to dynamically route each call or message via the carrier with the best connectivity at any point in time responding automatically to carrier availability and reliability. Twilio's software redundant infrastructure can also detect and route around issues experienced by hosts or even whole data centers in real time.\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Business Continuity Plan\nANSWER: Link to download attachment: https://drive.google.com/file/d/1OV58HkarfgxgSuOK4eCUC7HDWe59N9ia/view https://drive.google.com/file/d/1OV58HkarfgxgSuOK4eCUC7HDWe59N9ia/view\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: High level BCDR Plan\nANSWER: Since Twilio is a cloud first company and no critical business process are tied to our physical offices all employees are able to work remotely at any time. If power / internet is still up in San Francisco after a disaster then no continuity plans would need to be enacted. Teams at Twilio can work remotely for up to 3 months and many longer without meeting in person. Additionally should an event happen in the Bay Area we have a Mountain View office (if not impacted) where the eTeam and key personnel could meet in person.   If an event happens in the Bay Area knocking out power and internet Twilio could move operations by transporting key San Francisco-based personnel to any location with an internet connection. This could be to any of our other offices or a temporary space closer to San Francisco depending on the severity and type of event that occurs.  Twilio's Support team is already our most geographically dispersed team so there would be no need to relocate our support operations. We do not have a traditional call center.\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Legal language for BCP\nANSWER: Twilio will maintain procedures for business continuity of the Twilio Services that will remain resilient in the event of most failure modes including natural disasters or system failures and will periodically review such procedures. Customer may subscribe to https://status.twilio.com/ for updates on Twilio’s operational status.\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Scheduled Maintenance Window\nANSWER: Twilio does not interrupt service to facilitate scheduled maintenance. Due to Twilio’s intelligent service-oriented architecture no maintenance affects customer uptime.\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Disaster Recovery Plan\nANSWER: Twilio will leverage AWS services and resiliency services as a part of our DR strategy\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: BCDR backup zones\nANSWER: Twilio Services Hosted in AWS (US East) Backups are located in AWS US West Region. Twilio product teams have historically been responsible for uptime and resiliency of their products. Twilio has architected our environment with availability and resiliency as the number one priority. Customers can always check on the operational status of all Twilio products at  https://status.twilio.com/.   Hosting our services on AWS gives Twilio the ability to remain resilient globally even if one location goes down. AWS spans multiple geographic regions and availability zones which allow Twilio servers to remain resilient in the event of most failure modes including natural disasters or system failures. Twilio maintains redundant inbound and outbound connectivity with multiple network carriers and real-time systems to dynamically route each call or message via the carrier with the best connectivity at any point in time responding automatically to carrier availability and reliability. Twilio's software redundant infrastructure can also detect and route around issues experienced by hosts or even whole data centers in real time.  All Twilio services operate several AWS Availability Zones within the US-East region. Twilio's software redundant infrastructure can also detect and route around issues experienced by hosts or even whole data centers in real time. Our orchestration tooling has the ability to regenerate hosts building them from the latest backup. Twilio performs regular backups of Twilio account information call records call recordings and other critical data using Amazon S3 cloud storage. All backups are encrypted in transit and at rest using strong encryption. Backup files are stored redundantly across multiple availability zones and are encrypted. Should there be an incident Twilio maintains an incident response program in accordance to NIST SP 800-61. The program defines conditions under which security incidents are classified and triaged. Twilio Security Incident Response Team or T-SIRT assesses the threat of all relevant vulnerabilities or security incidents and establishes remediation and mitigation actions for all events. \n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: DR \"\"Hard Down\"\" Scenarios\nANSWER: Twilio is hosted on AWS. We have assessed the risks around AWS having a \"\"hard down\"\" situation and concluded that this risk was both very low and acceptable.\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: RTO/RPO SLA Business Impact Analysis\nANSWER: Twilio for most use cases stores phone numbers and Voice Call/SMS metadata (timestamp etc). Please discuss specific use cases with the sales rep to determine exact data points that Twilio will transmit/process/store Currently we are in the process of pulling together our BCP/DR programs together into a formalized company-wide program. Once this is in place we will begin testing these plans and from this testing we will be able to determine our RTO/RPO times however we cannot commit to timelines as of yet.  However we will use commercially reasonable efforts to maintain our SLA of 99.95% uptime and rely on our service credits to maintain this (https://www.twilio.com/legal/service-level-agreement). Along with this our customers can monitor the real-time status of Twilio’s service using https://status.twilio.com/\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Insurance\nANSWER: We carry Technology Errors and Omissions Liability insurance under our cyber liability insurance program.\n\nTOPIC: Business Continuity and Disaster Recovery\nQUESTION: Novel Coronavirus (COVID-19)\nANSWER: Twilio is actively monitoring the dynamic situation of COVID-19 (Coronavirus). Top of mind and highest priority is the safety and well-being of our employees customers and partners. As trusted communication and customer engagement platform we understand the continued availability of our services is critically important to our customers and developers.  Twilio has updated policies and guidance regarding the Novel Coronavirus (COVID-19) to protect the health and safety of all employees. We currently prohibiting all non-essential business travel and all international travel until further notice have canceled all events for the month of March 2020 and are discouraging employee attendance at large events and gatherings. All employees have the ability to work from home. To help maintain a healthy and safe workplace and reduce the risk of infection we will continue to make changes and deploy basic hygiene products across all of our offices for employees to use and participate in helping to keep our workplaces clean and reduce the risk of infection. Our Business Continuity/Disaster Recovery and Emergency Preparedness teams have a business continuity plan associated with a global health crisis that is being used as a guideline to respond to situations such as the Coronavirus. Our team is actively monitoring and assessing this dynamic situation and updating our response strategy accordingly.   At this time we do not foresee any potential disruptions to our business operations or an inability to serve our customers. Twilio has a pandemic response element that is part of our overall crisis management plan included within this response framework is a trigger to let our customers know if we have to cease any critical activities that would impact the availability of Twilio products.   We will continue to act thoughtfully amidst the potential uncertainties introduced by COVID-19 into our daily lives and remain committed to providing the excellent service and uptime that our customers rely on. Customers can monitor the real-time status of Twilio’s services using https://status.twilio.com/. We may also send notifications via email to the owner of the Twilio account.   For more information on Twilio's response to the COVID-19 pandemic please see our blog:   https://www.twilio.com/blog/twilio-safety-response-covid-19  \n\nTOPIC: Cloud Security\nQUESTION: Customer data isolation / multi-tenancy\nANSWER: Twilio is hosted on AWS which is multi-tenant. Multi-tenancy is an integral component of Twilio's architecture as well. We make sure that one client's data is not shared with other clients using logical identifiers.\n\nTOPIC: Cloud Security\nQUESTION: Multi-tenancy Expanded\nANSWER: Twilio is hosted on AWS which is multi-tenant. Twilio has implemented logical separation between customers using logical identifiers tagging all communications data with the associated Customer ID to clearly identify ownership. Twilio applications are designed and built to honor these tags and enforce access controls to ensure the confidentiality and integrity requirements for each customer are appropriately addressed (similar to the way that traditional telephony or Internet traffic traverses a shared set of infrastructure). These controls are reviewed and vetted by our security engineering team as a part of their application security assessment process to ensure one customer's communications can not be accessed by a different customer. The specific way that tagging is implemented and enforced varies by product based on the nature of the data and storage but Twilio maintains strong segmentation between customers and our current implementation is effective across our product lines.\n\nTOPIC: Cloud Security\nQUESTION: Logical Identifiers Expanded\nANSWER: These logical identifiers aren't really tags but are values within a specific row within the database. These values indicate which account owns the data for a given row. As such these values are immutable and we don't provide a way through our API or services to update the ownership of a given record or row in the database once it has been written. When we are querying this data the owning account is always provided as a portion of the where clause. If the proper owning account is not provided then it is impossible for the data to be returned to the caller. While the customer does pass the account as part of the URL when fetching data that value is validated against the authentication token that is provided. This means someone can't just merely guess the resource sid and account sid in order to fetch the data from another account. They must also know the auth token for the account. This is generally what protects the records. In addition to this protection the data is encrypted at rest. Critical PII data that includes things like Message Bodies or the Audio recording of a phone call are additional field level encrypted with a unique key per account. This is to protect against a data breach or a situation where someone may have exfiltrated a single customers encryption key. As they would need the key that is specific to that account and product (different keys are used for each product's data). One other mechanism that is available to customers is to make use of Twilio Connect. It would provide a private network for the customer to use when accessing their Twilio account. Some of our more cautious customers choose to do this rather than making API accesses over the public internet.\n\nTOPIC: Cloud Security\nQUESTION: How AWS separates customer's environments\nANSWER: AWS has a very high level of security in all areas of the services it provides. Please refer to their whitepaper for further details: http://d0.awsstatic.com/whitepapers/Security/AWS%20Security%20Whitepaper.pdf  AWS also allows to provision EC2 instances on dedicated hardware to Twilio only. More info on this can be found here: http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/dedicated-instance.html  For more information on storage on EBS and the security features and encryption levels it provides please refer to the below links: http://aws.amazon.com/ebs/details/ http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html \n\nTOPIC: Cloud Security\nQUESTION: Whitelisting\nANSWER: We can provide static IPs for the customer to whitelist through support. Twilio will not whitelist customer&#x27;s IPs.\n\nTOPIC: Cloud Security\nQUESTION: Downtime / Maintenance windows\nANSWER: Twilio does not interrupt service to facilitate scheduled maintenance. Due to Twilio's intelligent service-oriented architecture no maintenance affects customer uptime.\n\nTOPIC: Cloud Security\nQUESTION: Outages\nANSWER: Customers can monitor find real-time updates here: http://status.twilio.com/. We also give 60 days notice for any major changes to our service as described in our TOS here: https://www.twilio.com/legal/tos \n\nTOPIC: Cloud Security\nQUESTION: Where are Twilio Data Centres located? (general includes SendGrid)\nANSWER: Twilio Services: AWS data centres in the United States.SendGrid Services: Co-location data centres in the United States.\n\n\nINSTRUCTION:\nA human enters the conversation and starts asking questions. Generate the reply based of FAQ list.\n_________________________\nHuman: Hello, who are you?\nAI: I am a chatbot that can answer questions about Twilio. I can provide you with answers as long as they are included into a list of frequently asked questions. Sorry, but I cannot answer any of your questions if they are not in the FAQ list."
    },
    {
        "role": "user",
        "content": ""
    },
    {
        "role": "assistant",
        "content": "AI: Hello! I am here to answer your questions about Twilio. However, I can only provide information that is included in the list of frequently asked questions. If your question is not in the FAQ list, I apologize, but I won't be able to answer it. How can I assist you today?"
    },
    {
        "role": "user",
        "content": inb_msg
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
    return str(response.choices[0].message.content)


if __name__ == "__main__":
    app.run(debug=True, port=8001)

