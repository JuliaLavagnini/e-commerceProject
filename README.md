# E-Commerce

[View Zing Gym website on Heroku](https://zing-gym-django-48223353ee17.herokuapp.com)

![GitHub last commit](https://img.shields.io/github/last-commit/JuliaLavagnini/e-commerceProject?color=red)
![GitHub contributors](https://img.shields.io/github/contributors/JuliaLavagnini/e-commerceProject?color=orange)
![GitHub language count](https://img.shields.io/github/languages/count/JuliaLavagnini/e-commerceProject?color=yellow)
![GitHub top language](https://img.shields.io/github/languages/top/JuliaLavagnini/e-commerceProject?color=green)

This Django e-commerce project is an online platform for purchasing gym memberships and training plans. It allows users to browse, purchase, and manage their subscriptions, and includes features for user authentication, profile management, and payment processing.

## Deign process

**Target Audience**

Zing gym is designed to cater to a diverse range of users, chidren to elders, and genders with flexible schedules to accommodate early morning, daytime, and late-night workouts. To provide specialized programs such as sessions for pregnant individuals, physiotherapy, and accessibility for those with disabilities.

**Imagery**

All media content was hold all rights reserved, to Unsplash.

**Wireframes**

![Wireframes of all pages](</media/documentation_images/Frame 1.png>)

**Accessibility**

* Responsive design ensures that our app adapts seamlessly to different screen sizes and devices, providing a consistent user experience.
* The app prioritizes a clear and intuitive layout to ensure ease of navigation for all users.
* Carefully selection of colours with high contrast to improve readability and usability.

## Technologies Stack

* `HTML`
* `CSS`
* `JavaScript`
* `Django`
* `Stripe`
* `Bootstrap`
* `Neon`
* `CloudFare`
* `Heroku`
  
## Features

Zing Gym offers a comprehensive fitness experience with the following features:

- **User Registration and Login**: New users can create an account, and existing users can log in to access their profiles.
  
- **Trainer Profiles**: Browse detailed profiles of available trainers, including their specialties and experience.
  
- **Pricing Options**: View and select from various membership plans and pricing options and make payments using Stripe
  
- **Personalized Profile**: Logged-in users can view and manage their membership, access and update their information.

## Process

The creation of this project was based on the e-commerce walk-through project. 
All files use base file template to easier load of content as all mandatory details are included on it. Main static files (media and css) are separated from the apps. 

**Trainers app**
  
Within the app, I've structured a robust Trainer model boasting essential fields like name, programs, availability, specialty, sessions, and image. To streamline data input, predefined choices using tuples are available for specific fields, enriching the storage of trainer information within the e-commerce platform and seamlessly integrating it into the database.

Additionally, the app defines meticulously crafted views, meticulously handling the management of trainers within the e-commerce platform. These views undertake various tasks, ranging from showcasing a comprehensive list of trainers to displaying intricate details of individual trainers. Moreover, they empower users to add new trainers, modify existing ones, or remove outdated entries directly from the database. Each view operates cohesively, aligning with user requests and ensuring smooth interaction with trainer data across the platform.

**Plans app**

I've developed a comprehensive plan management system within the Django application. It encompasses models tailored for storing essential plan attributes, including names, descriptions, monthly pricing, and yearly pricing. Moreover, the system integrates specialized forms to facilitate the addition and modification of plans, complemented by dedicated views responsible for rendering plan-related pages and managing CRUD operations seamlessly.

Users are empowered with full-fledged functionalities, allowing them to effortlessly navigate through plan options, add new plans, modify existing ones, and even remove outdated plans, all contingent upon their permissions. The user-friendly templates elegantly showcase plans, presenting users with the flexibility to choose between monthly or yearly pricing options. Administrators, equipped with enhanced privileges, can efficiently perform plan management tasks directly from the interface, streamlining the overall administrative workflow.

**Profile app**

I've implemented signals within the Django application to streamline the creation and updating of user profiles whenever a user registers or modifies their account details. This automated process ensures that user profiles remain synchronized with user information, including username, email, and address details. Additionally, I've developed forms and views to facilitate user interactions with their profiles, enabling them to view and modify their personal information conveniently.

Moreover, the system includes a purchase history section where users can access comprehensive details of their past transactions, such as plan specifics, prices, and purchase timestamps. This functionality enhances user transparency and empowers users to manage their subscription history effectively. Furthermore, users can cancel their payments directly from their profiles, offering a seamless experience and optimizing administrative efficiency within the application.

**Checkout app**

I've written JavaScript code that utilizes Stripe's client-side functionality for secure payment processing. It initializes Stripe elements, validates user inputs, and communicates payment details to the backend, ensuring a smooth and secure payment experience for users. Additionally, I've integrated Django forms and models seamlessly with the frontend, capturing essential payment information and storing it in the database for future reference.

Furthermore, I've developed Django views and webhook handling to provide robust backend support for payment processing. My views render the payment form, process payment data, and handle webhook events from Stripe, ensuring accurate recording and management of payment transactions. The webhook endpoint serves as a vital link between my Django application and Stripe, enabling real-time updates on payment statuses and ensuring the reliability and security of the payment system. Together, these components create a cohesive and efficient payment infrastructure within my Django project.

**External sources**

In my setup, I opted for the Neon database to handle all the project data. It acts as the backbone, securely storing everything I need for the project. As for media and static files, I'm using Cloudflare. It's like my digital storage space, organizing and serving up files as needed.

And when it comes to hosting, I've chosen Heroku. It's essentially the home base for my project in the online world. All the essential configurations, like secret keys and IDs, are stored there to keep things running smoothly. So, think of it as my project's control center, managing everything behind the scenes.

## Improvements

- Add more content to the website to be a richer website.
- Fix media location as it is instable from time to time.
- Improve the status function on purchase hisotry.

## Credits

I gave the credits to [Advanced Form Rendering with Django Crispy Forms article](https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html#custom-fields-placement-with-crispy-forms) that help me custom my forms on checkout and profile apps. 

Also, [How to create subscription payments with Django and Stripe(3D Secure) using dj-stripe article](https://medium.com/@surya.vijjeswarapu/how-to-create-subscription-payments-with-django-and-stripe-3d-secure-using-dj-stripe-a7b55a391196), gave my the snippet for the strip card element. 

## Tests

Look for the Tests.md file

## Running the Project

* To Folk this repository, click on the Folk button in the top right corner. 

* To clone, click to 'Code' green button (top right corner) and select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory. Type 'git clone' into the terminal and then paste the link you copied.

## Video
![gif](media/documentation_images/ezgif-2-fcdf9ff957.gif)