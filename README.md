# PAN-card-credential-extraction-using-AZURE-Cognitive-Services-OCR
**Extracting PAN card extraction using OCR with the help of Microsoft Azure Cognitive services computer vision library and OCR functionality, and implementing this using Flask based development web-api.**

***Objective : To build a Web-Based API for extracting PAN/ID Credentials when the website visitor uploads PAN/ID Card image.
Manual:***

To run the webapi, go to anaconda prompt, install:
* a) i. azure.cognitiveservices.vision.computervision, ii. Flask, iii. Flask_uploads
* b) python upload.py, then automatically the automatically the webpage will be loaded through the gateway.
* c) Then, visitor uploads the image, press submit the get the result.

***Project workflow:***
* 1. The goal is to extract texts from images using OCR
* 2. To extract OCR “azure-cognitiveservices-vision-computervision” service is used.
* 3. The image is extracted using that service, where the key and endpoint of the resource group is used.
* 4. Flask app is used to create the development user interface.
* 5. The web page is created using html, when the user uploads the image, the form in the html gets the input using ‘GET’ method, then the input image is received from the      gateway to python backend(upload.py) from where the flask app was called.
* 6. Then, the file is saved to ‘/Image’ folder, that is shown in the video.
* 7. The, the OCR_text.extract_text(‘Image_file_name) is called.
* 8. So, the control is sent to OCR_text which deals with the entire text extraction process.
* 9. When, the extract_text() called, the PIL library loads the image of that passed file name as visitor(raw pan_card image), then it resizes the image based on following formulation

**factor = min(1, float(1024.0 / length_x))**
**final_image_size = int(factor * length_x), int(factor * width_y)**
  Then, image is overwritten over raw image with optimal resolution

* 10. Then, the image is sent to the Azure cognitive services computer vision service using recognize_printed_text_in_stream() method, where the method is called using a client   which uses the service using key and endpoint. Client sends user as request and on successful key and endpointverification, the region-based text is obtained as response from the server.

***Credential Detection:***
Each line on the pan card is stored individually in a list from region-based extracted text.
* 1. DOB detection: dateutil python library is used to check, whether any line contains a date or not.
* 2. **PAN No detection:** The program traverses through each of the line, and each line is further splitted
* into words, if any of that word lies within 
  **'(Number|umber|Account|ccount|count|Permanent|ermanent|manent)$', then the next line must contains the PAN id.**
* 3. **Name detection: There are two formats –a) Name should be under ‘NAME’ heading, or b) Under the line which contains any of the word
  **'(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$',
  **If condition == a: then, line+1 holds Name of person,**
  **Else: check if condition== b: then, line+1 holds the Name,** if any of the above does not satisfy,**
  then, we have to rely on database of person. Then, we also use the same method, but here we check whether line + 1, contains the any name from the database.
* **Name check: For checking ‘NAME’ word ‘difflib’ is used to predict, if the lie contains the word which is very similar to the referenced text(here ,’NAME’)
Thus, we have obtained the required credentials: Name, DOB, PAN id, and then, these are stored in a list, and send to the upload.py, from where it was called, and then it will be posted to through the flask route path using the same host, and the html template will be rendered again, and visitor will get the visible extracted credential in that webpage.

***Modification and improvement:***
* 1. In this work, the shear correction of the card in the image is not used, so using opencv if shear
  correction is done to rotate the image, and make it aligned with the frame,
* 2. Automatic exposure enhancement, will be implemented to increase the details
* 3. Remove the noise of the image.
* 4. The salt, pepper- and Gaussian noise can be removed, the image can be aligned
* 5. More effectively, if we use opencv to find the region of interest of the texts in the frame, or use Attention Network or transformer network to highlight the sections which contains the text, and by extracting the regions if we zoom-in and apply OCR on that regions, the accuracy and precision will be enhanced, and will help to make this web-app serverless.

***Application:***
The application is in banking or any sector where PAN based KYC is needed.
