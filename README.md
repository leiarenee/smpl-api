# Assignment

Build an API that will use a string as input and does a find and replace for certain words and outputs the result. For example: replace ABN by ABN AMRO.
Example input: “The analysts of ABN did a great job!”
Expected output: “The analysts of ABN AMRO did a great job!”

The words that need to be replaced are provided on the right side of this slide.

Rules
1. Preferably the solution should be deployed on AWS, that will also be the platform you will be working on when you join TMNL. However, you may also deploy this solution on any other cloud (e.g. Azure, GCP, Heroku)
2. You are allowed to use every cloud service or technology you want. You can build it for example in Golang and deploy on AWS EKS, or build in .NET and deploy it as a Lambda. Bonus points if you’re able to surprise us 😉
3. It’s important that you are be able to explain the choices made during this assignment. Rather try to build something that doesn’t work a 100% and we have a good discussion on what you have learned then copying something of Google and not being able to explain the innerworkings or the choices made.

Deliverables
• Access to the version control system the sources are hosted (preferably Github or GitLab)
• The end-point of the API

List of word that need to be replaced:

* ABN -> ABN AMRO
* ING -> ING Bank
* Rabo -> Rabobank
* Triodos -> Triodos Bank
* Volksbank -> de Volksbank

The input can be a combination of lower and upper case, the output should be as specified
