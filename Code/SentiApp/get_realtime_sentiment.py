from encoder import Model
import csv
import time
model=Model()
def get_activations(text):
	activations = []
	temp2 = []
	new_text = []
	for i in range(len(text)):
		new_text.append(text[i])
		temp_text = ''.join(new_text)
		temp2.append(temp_text)
	print ("Transforming")
	print ("Number of samples to transform " + str(len(temp2)))
	a = time.time()
	text_features = model.transform(temp2)
	b = time.time()
	c = b - a
	print ("Time taken to transform: " + str(c) + " secs")

	
	for i in range(len(temp2)):
		sentiment = text_features[i, 2388]
		activations.append(sentiment)
	list1 = []
	for i in range(len(text)):
		list1.append([text[i], activations[i]])


	return list1



text ="I had a meeting with Mark Wallace from Finance and he is really impressed with the performance of hedge fundsin the equity trading desk. Enron, California had reported great results over last couple of months. However, as per a new report by J P Morgan, wealthy investors are boosting bets on energy stocks and leaving hedge funds and equities due to concerns over bad valuations and geopolitical risk. So we are really worried about it all going downhill for hedge funds from here on. Let's meet on July 17th to discuss this issue."

print (get_activations(text))


