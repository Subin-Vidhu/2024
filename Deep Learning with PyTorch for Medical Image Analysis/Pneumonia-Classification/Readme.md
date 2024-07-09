### Identify signs of pneumonia in chest X-ray images

- Medical background

    - Pneumonia is an infection in one or both lungs. Bacteria, viruses, and other germs cause the lungs' air sacs to become inflamed and filled with fluid or pus. This can make it difficult for the patient to breathe. Pneumonia can range in seriousness from mild to life-threatening. It is most serious for infants and young children, people older than age 65, and people with health problems or weakened immune systems.
 
    - Common infectious disease

    - Symptoms: cough, fever, chills, and difficulty breathing

    - Diagnosis: chest X-ray, blood tests, and sputum tests

- Data

    - Will be using the data from RSNA Pneumonia Detection Challenge on Kaggle. 

    - 26684 chest X-ray images (JPEG) with 1 or more areas of pneumonia

        - 20672 images without pneumonia

        - 6012 images with pneumonia

- Preprocessing

    - Original image size: 1024 x 1024

        - Resized image size: 224 x 224

    - Standardize the pixel values into the interval [0, 1] by scaling with 1/255

    - Split dataset into 24000 training images and 2684 validation images

