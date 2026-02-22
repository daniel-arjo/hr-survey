# HR Process Automation: Onboarding & Offboarding Surveys

📌 The Problem
The process of contacting employees for critical HR lifecycle events—specifically the Onboarding (new hires) and Offboarding (departing employees) surveys—was 100% manual. The HR team had to read spreadsheets, search for contacts, type messages individually, and log the status of each message sent. This repetitive process consumed an average of 2 hours per cycle and was highly susceptible to human error.

💡 The Solution
I developed a versatile Python script using Selenium and Pandas to fully automate this workflow. Designed with reusability in mind, the bot can easily toggle between Onboarding and Offboarding contexts just by updating the input database. It automatically accesses WhatsApp Web, sends personalized messages to each employee, and generates an automated audit log showing the delivery status (Success/Error) of each message.

📈 Results Achieved

83% reduction in operational time: A process that used to take 2 hours is now executed in approximately 20 minutes.

Dual-Purpose Utility: The same codebase serves both the admission and termination sectors of HR, maximizing the ROI of the automation.

Zero human error: Complete standardization of the messages sent.

Governance: Automatic generation of Excel audit reports with delivery statuses.

🚀 Architecture and Scalability Vision
This script was designed as the initial trigger (Outbound) for communication. To scale the solution and turn it into a complete product, I mapped the following architectural evolutions:

Orchestration: The script can be easily encapsulated into a .bat or .cmd file and configured in the Windows Task Scheduler or via Cronjob to run 100% autonomously, without the need for a manual trigger.

NLP and Database Integration: To maintain a continuous flow and store the survey responses, the ideal architecture includes routing the contact to a conversational AI platform (like Dialogflow). This would parse the natural language responses and automatically save them into a relational database, completing the data pipeline.

🛠️ Technologies Used

Python (Core language)

Pandas (Reading, manipulating, and exporting DataFrames)

Selenium WebDriver (Web navigation automation and HTML/XPath element interaction)
