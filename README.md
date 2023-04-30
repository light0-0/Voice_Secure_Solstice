# Voice_Secure_Solstice
Voice biometrics can be used to authenticate the identity of an individual by using an individual’s voice.

Registration: At the time of registration, voice samples will be captured and mapped with customers account no and will be stored in a database using an API.

Authentication: Authentication will be done using a live voice feed match  done against the voice sample retrieved from the database using an API. Live  voice feed will vary with dynamic text and timestamp.

Instead of the verification code sent thru SMS or Email, the identity of  the individual can be verified using the voice of the account holder.

Proposed Solution:

    1. Voice based authentication works by analysing various aspects of a person's voice, including pitch, tone, and cadence.

    2. These characteristics are unique to each individual and can be used to verify their identity. To use voice based authentication, a user must first enroll their voice by recording a sample.
    
    3. Our System take five input samples at the time of registration so that each pitch, tone and frequency can detect and to get maximum accuracy to authenticate the person
    
    4. When a user attempts to access their account, they are prompted to read the sentences. The system then compares their voice to the stored reference to confirm their identity.



Technologies Used:

    Django: Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.

    Tensorflow: TensorFlow is an end-to-end open source platform for machine learning.
    
    Librosa: Librosa is a valuable Python music and sound investigation library.
    
    Html & CSS:  HTML and CSS are two of the core technologies for building Web pages.

    Keras :Keras is used for creating deep models which can be productized on smartphones.


Future Scope:
Two step verification:- 

	As voice recognition technology continues to improve, the future of voice based authentication looks bright. It is expected to become even more accurate and secure, with the potential for multi-factor authentication using both voice and other biometric factors such as facial recognition.

     At the time of voice recognition the site also detects the users face by which system is 100 percent sure that entering is the correct user so no one can enter in the system by making fake noise or by doing mimicry.

    By applying a face recognition system we can make the system more secure and efficient.


How to Run the project :

    pip install -r requirements.txt

    python manage.py runserver  

Working Module youtube Link: https://youtu.be/g3bvY4jJcRE

https://user-images.githubusercontent.com/126838490/235343083-ee54b270-71be-45dd-9b5e-b8dbc63e58b5.jpg

https://user-images.githubusercontent.com/126838490/235343059-e479ef9e-0c2b-4261-941b-ea1e777e90eb.jpg

https://user-images.githubusercontent.com/126838490/235343159-a188265e-993f-437a-b64c-3fea238933b8.jpg

https://user-images.githubusercontent.com/126838490/235343108-f216c95d-3f93-469a-b9f6-4d72fa66f28b.jpg
