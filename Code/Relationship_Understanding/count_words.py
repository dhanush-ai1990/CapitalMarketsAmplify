import sqlite3
import nltk
import pickle
file_out = '/Users/usr/Documents/Entity Recognition/'
Database = sqlite3.connect(file_out+'Enron_database.db')
c = Database.cursor()

def clean(text):

   text = text.replace('--','')
   text = text.replace('\\t',' ')
   text = text.replace('=','')
   text = text.replace('(','')
   text = text.replace(')','')
   text = text.replace('<','')
   text = text.replace('>','')
   text = text.replace('thankskh','')
   text = text.replace('Re:','')
   text = text.replace('RE:','')
   text = text.replace('re:','')
   text = text.replace('Fw:','')
   text = text.replace('FW:','')
   text = text.replace('fw:','')
   text = text.replace('kh:','')
   return text

SQL = "select distinct(msgid), raw_body,subject from `Enron Prime`"
#SQL = "select msgid, raw_body, s+ubject from 'Enron Prime' where msgid = 1335"

c.execute(SQL)

def average_num_chars():
  file_number = 0
  count = 0
  temp_org =[]
  temp_person = []
  temp_place = []
  temp_others = []
  temp_product = []
  proper_nouns =[]
  all_nouns =[]
  corrected_text ={}
  all_words = []

  dir1 ='/Users/usr/Documents/Entity\ Recognition'
  all_chars = []
  num_sentences = []
  temp = [117506,2207,121182]
  for data in c:
    all_sentences = []
    #print(data)
    data1= data[1].split('-----Original Message-----')[0]
    body = clean(data1)
    count +=1
    print ('Currently processing the email number: ' + str(count))

    #for sentence in nltk.sent_tokenize(body):
    #  all_sentences.append(sentence)
    
    all_chars.append(len(body))
    #num_sentences.append(len(all_sentences))

  return (sum(all_chars)/float(len(all_chars)))
  #print (sum(num_sentences)/float(len(num_sentences)))

def average_num_sentences():
  file_number = 0
  count = 0
  temp_org =[]
  temp_person = []
  temp_place = []
  temp_others = []
  temp_product = []
  proper_nouns =[]
  all_nouns =[]
  corrected_text ={}
  all_words = []

  dir1 ='/Users/AdaEne/Documents/Entity\ Recognition'
  all_chars = []
  num_sentences = []
  temp = [117506,2207,121182]
  for data in c:
    all_sentences = []
    #print(data)
    data1= data[1].split('-----Original Message-----')[0]
    body = clean(data1)
    count +=1
    print ('Currently processing the email number: ' + str(count))

    for sentence in nltk.sent_tokenize(body):
      all_sentences.append(sentence)
    
    #all_chars.append(len(body))
    num_sentences.append(len(all_sentences))

  #return (sum(all_chars)/float(len(all_chars)))
  return (sum(num_sentences)/float(len(num_sentences)))

def give_me_sentences():
  all_emails = []
  count = 0

  dir1 ='/Users/AdaEne/Documents/Entity\ Recognition'
  all_chars = []
  num_sentences = []
  temp = [117506,2207,121182]
  for data in c:
    #raise Exception("STOP")
    data1= data[1].split('-----Original Message-----')[0]
    body = clean(data1)
    count +=1
    print ('Currently processing the email number: ' + str(count))

    cc = 0
    per_email = []
    all_sentences = []
    for sentence in nltk.sent_tokenize(body):
      all_sentences.append(sentence)
      if cc >= 3:
        per_email.append(str(' '.join(all_sentences)))
        all_sentences = []
        cc = 0
      cc += 1
    per_email.append(' '.join(all_sentences))
    all_emails.append(per_email)
    #raise Exception("STOP")
  return all_emails

def give_me_emails():
  all_emails = []
  count = 0

  dir1 ='/Users/AdaEne/Documents/Entity\ Recognition'
  all_chars = []
  num_sentences = []
  for data in c:
    #raise Exception("STOP")
    data1= data[1].split('-----Original Message-----')[0]
    body = clean(data1)
    count +=1
    print ('Currently processing the email number: ' + str(count))

    cc = 0
    per_email = []
    all_sentences = []
    for sentence in nltk.sent_tokenize(body):
      all_sentences.append(sentence)
      if cc >= 3:
        per_email.append(str(' '.join(all_sentences)))
        all_sentences = []
        cc = 0
      cc += 1
    per_email.append(' '.join(all_sentences))
    all_emails.append(per_email)
    #raise Exception("STOP")
  return all_emails

if __name__ == "__main__":
  split_emails = give_me_sentences()
  #print split_emails
  with open('myPickles','w') as f:
    pickle.dump(split_emails,f)
  # pickles = pickle.load(open('myPickles', 'rb'))
  # These fuckers: 117506, 2207, 121182, ...
  # average number of sentences: 7.35443748406
  # average number of characters: 1204.7757873

